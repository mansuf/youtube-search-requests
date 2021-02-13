# youtube-search-requests
# extractor/async_extractors.py

import json
import threading
from youtube_search_requests.constants import (
    BASE_YOUTUBE_SEARCH_INTERNAL_API_URL,
    BASE_YOUTUBE_SEARCH_QUERY_URL,
    ALL_FILTERS,
    ALL_VIDEOS_FILTERS,
    BASE_YOUTUBE_SEARCH_RELATED_VIDEOS_INTERNAL_API_URL
)
from youtube_search_requests.async_session import AsyncYoutubeSession
from youtube_search_requests.utils.errors import InvalidArgument
from youtube_search_requests.parser import (
    get_continuation_token,
    get_video_data,
    get_playlists_data,
    get_related_videos
)
import urllib.parse


class BaseAsyncExtractor:
    """Base Youtube Async Extractor"""
    def __init__(self, base_url, session: AsyncYoutubeSession, no_query=False):
        self.session = session
        self.BASE_URL = base_url
        self.no_query = no_query

    async def request_search(self, search_terms: str=None, filter_value: str=None, continuation=None):
        json_data = {'context': {}}
        for i in self.session.context.keys():
            json_data['context'][i] = self.session.context[i]
        if continuation is None and self.no_query is True:
            raise InvalidArgument('continuation cannot be None, while no_query is True')
        elif self.no_query is False:
            json_data['query'] = search_terms
            json_data['params'] = filter_value
        if continuation is not None:
            json_data['continuation'] = continuation
        r = self.session.post(
            self.BASE_URL + self.session.key,
            json=json_data,
            headers={
                'User-Agent': self.session.USER_AGENT,
            }
        )
        return json.loads(await r.text())


class VideoAsyncExtractor(BaseAsyncExtractor):
    """Extract youtube videos based on search terms"""
    def __init__(
        self,
        session: AsyncYoutubeSession,
        search_terms: str,
        max_results: int=10,
        include_related_videos: bool=False,
        max_results_related_videos: int=10,
        use_short_link: bool=False,
        filter_type: ALL_VIDEOS_FILTERS='NO_FILTER'
    ):
        super().__init__(BASE_YOUTUBE_SEARCH_INTERNAL_API_URL, session)
        self.search_query = search_terms
        self.max_results = max_results
        self.include_related_videos = include_related_videos
        self.FILTER = ALL_VIDEOS_FILTERS[filter_type]
        self.use_short_link = use_short_link
        self.max_results_related_videos = max_results_related_videos

    async def extract(self, legit_urls: list, event_shutdown: threading.Event):
        r = await self.request_search(self.search_query, self.FILTER)
        while True:
            # Force shutdown if True
            if event_shutdown.is_set():
                return legit_urls
            continuation = get_continuation_token(r)
            if continuation is None:
                await self.session.new_session()
                r = await self.request_search(self.search_query, self.FILTER)
                continue
            videos = get_video_data(r, use_short_link=self.use_short_link)
            if videos is None:
                await self.session.new_session()
                r = await self.request_search(self.search_query, self.FILTER)
                continue
            for i in videos:
                related_vids = []
                if i in legit_urls:
                    continue
                if self.include_related_videos:
                    v = VideoRelatedAsyncExtractor(
                        self.session,
                        i['url'],
                        self.max_results_related_videos,
                        self.use_short_link,
                        no_event_shutdown=True
                    )
                    i['related_videos'] = await v.extract(
                        related_vids,
                        event_shutdown
                    )
                else:
                    i['related_videos'] = None
                legit_urls.append(i)
                if len(legit_urls) > self.max_results or len(legit_urls) == self.max_results:
                    event_shutdown.set()
                    return legit_urls
            else:
                r = await self.request_search(self.search_query, self.FILTER, continuation=continuation)
                continue

class PlaylistAsyncExtractor(BaseAsyncExtractor):
    """Search youtube playlists based on search terms"""
    def __init__(
        self,
        session: AsyncYoutubeSession,
        search_terms: str,
        max_results: int=10,
        use_short_link: bool=False
    ):
        super().__init__(BASE_YOUTUBE_SEARCH_INTERNAL_API_URL, session)
        self.search_query = search_terms
        self.max_results = max_results
        self.FILTER = ALL_FILTERS['PLAYLISTS_FILTER']
        self.use_short_link = use_short_link
    
    async def extract(self, legit_urls: list, event_shutdown: threading.Event):
        r = await self.request_search(self.search_query, self.FILTER)
        while True:
            # Force shutdown if True
            if event_shutdown.is_set():
                return legit_urls
            continuation = get_continuation_token(r)
            if continuation is None:
                await self.session.new_session()
                r = await self.request_search(self.search_query, self.FILTER)
                continue
            playlists = get_playlists_data(r, self.use_short_link)
            if playlists is None:
                await self.session.new_session()
                r = await self.request_search(self.search_query, self.FILTER)
                continue
            for i in playlists:
                if i in legit_urls:
                    continue
                legit_urls.append(i)
                if len(legit_urls) > self.max_results or len(legit_urls) == self.max_results:
                    event_shutdown.set()
                    return legit_urls
            else:
                r = await self.request_search(self.search_query, self.FILTER, continuation=continuation)
                continue

class VideoRelatedAsyncExtractor(BaseAsyncExtractor):
    """Search youtube related videos based on youtube watch url"""
    def __init__(
        self,
        session: AsyncYoutubeSession,
        youtube_url: str,
        max_results: int=10,
        use_short_link: bool=False,
        **kwargs
    ):
        super().__init__(
            BASE_YOUTUBE_SEARCH_RELATED_VIDEOS_INTERNAL_API_URL,
            session,
            no_query=True
        )
        self.session = session
        self.url = youtube_url
        self.max_results = max_results
        self.use_short_link = use_short_link
        try:
            nes = kwargs['no_event_shutdown']
        except KeyError:
            self._no_event_shutdown = False
        else:
            if nes:
                self._no_event_shutdown = True
            elif not nes:
                self._no_event_shutdown = False

    def _wrap_dict_related_videos(self, data):
        startpos = data.find('var ytInitialData = ')
        text2 = data[startpos+20:]
        endpos = text2.find('"}};</script>') + 3
        try:
            return json.loads(text2[:endpos])
        except json.decoder.JSONDecodeError:
            # for newest android browsers
            pos1 = text2.find(';</script><script nonce')
            # for oldest android browsers
            pos2 = text2.find(';</script><script>')
            if pos1 == -1:
                parsed_text = text2[1:pos2 - 1]
            else:
                parsed_text = text2[1:pos1 - 1]
            compiled_text = compile('text = """%s"""' % (parsed_text), '<string>', 'single')
            return json.loads(compiled_text.co_consts[0])

    async def _extract_from_scrapping(self):
        unparsed_data = await self.session.get(self.url).text()
        parsed_data = self._wrap_dict_related_videos(unparsed_data)
        open('scrap_rel_vid_extractor_errors.json', 'w').write(json.dumps(parsed_data))
        return [
            get_related_videos(parsed_data, self.use_short_link),
            get_continuation_token(parsed_data)
        ]

    async def extract(self, legit_urls: list, event_shutdown: threading.Event):
        while True:
            parsed_data = await self._extract_from_scrapping()
            # extract from scrapping
            result = parsed_data[0]
            token = parsed_data[1]
            if result is not None:
                for vid in result:
                    if vid in legit_urls:
                        continue
                    legit_urls.append(vid)
                    if len(legit_urls) > self.max_results or len(legit_urls) == self.max_results:
                        if not self._no_event_shutdown:
                            event_shutdown.set()
                        return legit_urls
            # if we failed to extract continuation token
            # and if requested length urls doesn't match with current length urls
            # return current urls.
            # Why ?, to prevent useless loop request to youtube.
            if token is None:
                if not self._no_event_shutdown:
                    event_shutdown.set()
                return legit_urls
            else:
                break
        # extract from internal API using continuation token 
        r = await self.request_search(continuation=token)
        open('rel_vid_extractor_errors.json', 'w').write(json.dumps(r))
        while True:
            # Force shutdown if True
            if event_shutdown.is_set():
                return legit_urls
            continuation = get_continuation_token(r)
            if continuation is None:
                await self.session.new_session()
                r = await self.request_search(continuation=token)
                continue
            videos = get_related_videos(r, self.use_short_link)
            if videos is None:
                await self.session.new_session()
                r = await self.request_search(continuation=token)
                continue
            for i in videos:
                if i in legit_urls:
                    continue
                legit_urls.append(i)
                if len(legit_urls) > self.max_results or len(legit_urls) == self.max_results:
                    if not self._no_event_shutdown:
                        event_shutdown.set()
                    return legit_urls
            else:
                r = await self.request_search(continuation=continuation)
                continue