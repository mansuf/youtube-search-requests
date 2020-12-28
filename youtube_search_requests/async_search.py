# youtube-search-requests
# async_search.py

import aiohttp
import json
import asyncio
import threading
from youtube_search_requests.async_session import AsyncYoutubeSession
from youtube_search_requests.utils import GetContinuationToken, GetVideosData
from youtube_search_requests.utils.errors import InvalidArgument
from concurrent.futures import Future

class AsyncYoutubeSearch:
    """

    **Same as YoutubeSearch, but with async method**

    AsyncYoutubeSearch arguments

    search_query: :class:`str`
        a string terms want to search.
    max_results: :class:`int` (optional, default: 10)
        maximum search results.
    timeout: :class:`int` or :class:`NoneType` (optional, default: None)
        give number of times to execute search, if times runs out, search stopped & returning results.
    json_results: :class:`bool` (optional, default: False)
        if True, Return results in json format. If False return results in dict format.
    include_related_videos: :class:`bool` (optional, default: False)
        include all related videos each url's.
    async_youtube_session: :class:`AsyncYoutubeSession` (optional, default: None)
        a async session for youtube.
        NOTE: AsyncYoutubeSearch require AsyncYoutubeSession in order to work !.
    safe_search: :class:`bool` (optional, default: False)
        This helps hide potentially mature videos.
        No filter is 100% accurate.
    """
    def __init__(
        self,
        search_query: str,
        max_results: int=10,
        timeout: int=None,
        json_results: bool=False,
        include_related_videos: bool=False,
        async_youtube_session: AsyncYoutubeSession=None,
        safe_search: bool=False
    ):
        # Validate the arguments
        if not isinstance(search_query, str):
            raise InvalidArgument('search_query expecting str, got %s' % (search_query.__class__.__name__))
        if not isinstance(max_results, int):
            raise InvalidArgument('max_results expecting int, got %s' % (max_results.__class__.__name__))
        if timeout is not None:
            if not isinstance(timeout, int):
                raise InvalidArgument('timeout expecting int or NoneType, got %s' % (timeout.__class__.__name__))
        if not isinstance(json_results, bool):
            raise InvalidArgument('json_results expecting bool, got %s' % (json_results.__class__.__name__))
        if not isinstance(include_related_videos, bool):
            raise InvalidArgument('include_related_videos expecting bool, got %s' % (include_related_videos.__class__.__name__))
        if async_youtube_session is not None:
            if not isinstance(async_youtube_session, AsyncYoutubeSession):
                raise InvalidArgument('async_youtube_session expecting AsyncYoutubeSession, got %s' % (async_youtube_session.__class__.__name__))
        if not isinstance(safe_search, bool):
            raise InvalidArgument('safe_search expecting bool, got %s' % (safe_search.__class__.__name__))

        self.search_query = search_query
        self.max_results = max_results
        self.BASE_SEARCH_URL = 'https://www.youtube.com/youtubei/v1/search?key='
        self.timeout = timeout
        self.json_results = json_results
        self.include_related_videos = include_related_videos
        self.session = async_youtube_session or AsyncYoutubeSession(preferred_user_agent='BOT', restricted_mode=safe_search)

    def _wrap_json(self, urls: list):
        if self.json_results:
            return json.dumps({'urls': urls})
        else:
            return urls

    async def request_search(self, search_terms: str, continuation=None):
        json_data = {'context': {}}
        for i in self.session.client.keys():
            json_data['context'][i] = self.session.client[i]
        json_data['query'] = search_terms
        if continuation is not None:
            json_data['continuation'] = continuation
        r = await self.session.post(self.BASE_SEARCH_URL + self.session.key, json=json_data, headers={'User-Agent': self.session.USER_AGENT})
        return json.loads(await r.text())

    async def main(self, legit_urls: list, event_shutdown: asyncio.Event):
        r = await self.request_search(self.search_query)
        while True:
            # Force shutdown if True
            if event_shutdown.is_set():
                return legit_urls
            continuation = GetContinuationToken(r).get_token()
            if continuation is None:
                await self.session.new_session()
                r = await self.request_search(self.search_query)
                continue
            videos = GetVideosData(r, self.include_related_videos).get_videos()
            if videos is None:
                await self.session.new_session()
                r = await self.request_search(self.search_query)
                continue
            for i in videos:
                if i in legit_urls:
                    continue
                legit_urls.append(i)
                if len(legit_urls) > self.max_results or len(legit_urls) == self.max_results:
                    event_shutdown.set()
                    return legit_urls
            else:
                r = await self.request_search(self.search_query, continuation=continuation)
                continue

    async def _search(self, timeout=None):
        try:
            self.session.key
            self.session.data
            self.session.client
            self.session.id
            self.session.USER_AGENT
        except AttributeError:
            await self.session.new_session()
        if timeout is None:
            legit_urls = []
            event_shutdown = asyncio.Event()
            return await self.main(legit_urls, event_shutdown)
        else:
            legit_urls = []
            event_shutdown = threading.Event()
            future = asyncio.ensure_future(self.main(legit_urls, event_shutdown))
            t = int(timeout.__repr__())
            exception = None
            while t > 0:
                try:
                    exception = future.exception()
                    break
                except asyncio.InvalidStateError:
                    await asyncio.sleep(1)
                    t -= 1
                    continue
            if exception is not None:
                raise exception
            return legit_urls

    async def search(self):
        urls = await self._search(self.timeout)
        return self._wrap_json(urls)