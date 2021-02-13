# youtube-search-requests
# search.py

import threading
import json
from .utils.errors import InvalidArgument
from .session import YoutubeSession
from .constants import (
    BASE_YOUTUBE_SEARCH_INTERNAL_API_URL,
    ALL_VIDEOS_FILTERS
)
from .extractor import (
    VideoExtractor,
    VideoRelatedExtractor,
    PlaylistExtractor
)
from concurrent.futures import Future

class YoutubeSearch:
    """
    YoutubeSearch arguments

    json_results: :class:`bool` (optional, default: False)
        if True, Return results in json format. If False return results in dict format
    youtube_session: :class:`YoutubeSession` (optional, default: None)
        a session for youtube.
        NOTE: YoutubeSearch require YoutubeSession in order to work !
    safe_search: :class:`bool` (optional, default: False)
        This helps hide potentially mature videos.
        No filter is 100% accurate.
    language: :class:`str` (optional, default: 'en')
        set the results language, see constants.py to see all valid languages
    """
    def __init__(
        self,
        json_results: bool=False,
        youtube_session: YoutubeSession=None,
        safe_search: bool=False,
        language: str='en'
    ):
        # Validate the arguments
        if not isinstance(json_results, bool):
            raise InvalidArgument('json_results expecting bool, got %s' % (json_results.__class__.__name__))
        if youtube_session is not None:
            if not isinstance(youtube_session, YoutubeSession):
                raise InvalidArgument('youtube_session expecting YoutubeSession, got %s' % (youtube_session.__class__.__name__))
        if not isinstance(safe_search, bool):
            raise InvalidArgument('safe_search expecting bool, got %s' % (safe_search.__class__.__name__))
        if not isinstance(language, str):
            raise InvalidArgument('language expecting str, got %s' % (language.__class__.__name__))

        self.BASE_SEARCH_URL = BASE_YOUTUBE_SEARCH_INTERNAL_API_URL
        self.json_results = json_results
        self.session = youtube_session or YoutubeSession(
            preferred_user_agent='BOT',
            restricted_mode=safe_search,
            language=language,
        )

    def _wrap_json(self, urls: list):
        if self.json_results:
            return json.dumps({'urls': urls})
        else:
            return urls

    def toggle_safe_search(self, safe_mode=True):
        """toggle safe search and create new session"""
        if self.session.restricted_mode == safe_mode:
            return
        self.session.restricted_mode = safe_mode
        self.session.new_session()

    def _search(
        self,
        extractor:  VideoExtractor or
                    PlaylistExtractor or
                    VideoRelatedExtractor,
        timeout=None
    ):
        """Search by giving extractor"""
        if timeout is None:
            legit_urls = []
            event_shutdown = threading.Event()
            return extractor.extract(legit_urls, event_shutdown)
        else:
            legit_urls = []
            event_shutdown = threading.Event()
            f = Future()

            def internal_worker(f, legit_urls, event_shutdown, extractor):
                f.set_running_or_notify_cancel()
                try:
                    result = extractor.extract(legit_urls, event_shutdown)
                    f.set_result(result)
                except Exception as e:
                    f.set_exception(e)

            worker = threading.Thread(target=internal_worker, name='worker_youtube_search_requests', args=(f, legit_urls, event_shutdown, extractor), daemon=True)
            worker.start()
            event_shutdown.wait(timeout)
            event_shutdown.set()
            exception = f.exception()
            if exception:
                raise exception
            return legit_urls

    def search_videos(
        self,
        search_query: str,
        max_results: int=10,
        timeout: int or None=None,
        include_related_videos: bool=False,
        max_results_related_videos: int=10,
        use_short_link: bool=False,
        filter_type: ALL_VIDEOS_FILTERS='NO_FILTER'
    ):
        """
        Search all videos

        search_query: :class:`str`
            a string terms want to search
        max_results: :class:`int` (optional, default: 10)
            set maximum search results
        timeout: :class:`int` or :class:`NoneType` (optional, default: None)
            give number of times to execute search, if times runs out, search stopped & returning results
            if None, search until maximum results reached.
        include_related_videos: :class:`bool` (optional, default: False)
            include all related videos each url's
        max_results_related_videos: :class:`int` (optional, default: 10)
            set maximum related videos each video in search results
        use_short_link: :class:`bool` (optional, default: False)
            use shorted link instead of original url
        filter_type: :class:`str` (optional, default: NO_FILTER)
            search videos using filter.
            see ALL_VIDEOS_FILTERS in constants.py to see all supported filters.
        """
        return self._wrap_json(
            self._search(
                VideoExtractor(
                    self.session,
                    search_query,
                    max_results,
                    include_related_videos,
                    max_results_related_videos,
                    use_short_link,
                    filter_type
                )
            , timeout=timeout)
        )

    def search_playlists(
        self,
        search_query: str,
        max_results: int=10,
        timeout: int or None=None,
        use_short_link: bool=False,
    ):
        """
        Search all channels

        search_query: :class:`str`
            a string terms want to search
        max_results: :class:`int` (optional, default: 10)
            maximum search results
        timeout: :class:`int` or :class:`NoneType` (optional, default: None)
            give number of times to execute search, if times runs out, search stopped & returning results.
            if None, search until maximum results reached.
        use_short_link: :class:`bool` (optional, default: False)
            use shorted link instead of original url
        """
        return self._wrap_json(
            self._search(
                PlaylistExtractor(
                    self.session,
                    search_query,
                    max_results,
                    use_short_link
                )
            , timeout=timeout)
        )
    
    def search_related_videos(
        self,
        youtube_url: str,
        max_results: int=10,
        timeout: int or None=None,
        use_short_link: bool=False
    ):
        """
        Search all related videos

        youtube_url: :class:`str`
            Youtube watch link, short link is supported
        max_results: :class:`int` (optional, default: 10)
            maximum search results
        timeout: :class:`int` or :class:`NoneType` (optional, default: None)
            give number of times to execute search, if times runs out, search stopped & returning results.
            if None, search until maximum results reached.
        use_short_link: :class:`bool` (optional, default: False)
            use shorted link instead of original url
        """
        return self._wrap_json(
            self._search(
                VideoRelatedExtractor(
                    self.session,
                    youtube_url,
                    max_results,
                    use_short_link
                )
            , timeout=timeout)
        )