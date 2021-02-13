# youtube-search-requests
# async_search.py

import aiohttp
import json
import asyncio
import threading
from .async_session import AsyncYoutubeSession
from .utils.errors import InvalidArgument
from .constants import (
    BASE_YOUTUBE_SEARCH_INTERNAL_API_URL,
    ALL_VIDEOS_FILTERS
)
from concurrent.futures import Future
from .extractor import (
    VideoAsyncExtractor,
    PlaylistAsyncExtractor,
    VideoRelatedAsyncExtractor
)

class AsyncYoutubeSearch:
    """

    **Same as YoutubeSearch, but with async method**

    AsyncYoutubeSearch arguments

    async_youtube_session: :class:`AsyncYoutubeSession` (REQUIRED)
        a session for youtube.
        NOTE: AsyncYoutubeSearch require AsyncYoutubeSession in order to work !
    json_results: :class:`bool` (optional, default: False)
        if True, Return results in json format. If False return results in dict format
    """
    def __init__(
        self,
        async_youtube_session: AsyncYoutubeSession,
        json_results: bool=False,
    ):
        # Validate the arguments
        if not isinstance(json_results, bool):
            raise InvalidArgument('json_results expecting bool, got %s' % (json_results.__class__.__name__))
        if not isinstance(async_youtube_session, AsyncYoutubeSession):
            raise InvalidArgument('async_youtube_session expecting AsyncYoutubeSession, got %s' % (async_youtube_session.__class__.__name__))

        self.BASE_SEARCH_URL = BASE_YOUTUBE_SEARCH_INTERNAL_API_URL
        self.json_results = json_results
        self.session = async_youtube_session

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

    async def _search(
        self,
        extractor:  VideoAsyncExtractor or
                    PlaylistAsyncExtractor or
                    VideoRelatedAsyncExtractor,
        timeout=None
    ):
        """Search by giving extractor"""
        if timeout is None:
            legit_urls = []
            event_shutdown = asyncio.Event()
            return await extractor.extract(legit_urls, event_shutdown)
        else:
            legit_urls = []
            event_shutdown = threading.Event()
            future = asyncio.ensure_future(extractor.extract(legit_urls, event_shutdown))
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

    async def search_videos(
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
        **Coroutine/Async Function**

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
            await self._search(
                VideoAsyncExtractor(
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

    async def search_playlists(
        self,
        search_query: str,
        max_results: int=10,
        timeout: int or None=None,
        use_short_link: bool=False,
    ):
        """
        **Coroutine/Async Function**

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
            await self._search(
                PlaylistAsyncExtractor(
                    self.session,
                    search_query,
                    max_results,
                    use_short_link
                )
            , timeout=timeout)
        )
    
    async def search_related_videos(
        self,
        youtube_url: str,
        max_results: int=10,
        timeout: int or None=None,
        use_short_link: bool=False
    ):
        """
        **Coroutine/Async Function**

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
            await self._search(
                VideoRelatedAsyncExtractor(
                    self.session,
                    youtube_url,
                    max_results,
                    use_short_link
                )
            , timeout=timeout)
        )