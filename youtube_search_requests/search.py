# youtube-search-requests
# search.py

import threading
import json
from youtube_search_requests.utils.errors import InvalidArgument
from youtube_search_requests.session import YoutubeSession
from youtube_search_requests.utils import GetContinuationToken, GetVideosData
from concurrent.futures import Future

class YoutubeSearch:
    """
    YoutubeSearch arguments

    search_query: :class:`str`
        a string terms want to search
    max_results: :class:`int` (optional, default: 10)
        maximum search results
    timeout: :class:`int` or :class:`NoneType` (optional, default: None)
        give number of times to execute search, if times runs out, search stopped & returning results
    json_results: :class:`bool` (optional, default: False)
        if True, Return results in json format. If False return results in dict format
    include_related_videos: :class:`bool` (optional, default: False)
        include all related videos each url's
    youtube_session: :class:`YoutubeSession` (optional, default: None)
        a session for youtube.
        NOTE: YoutubeSearch require YoutubeSession in order to work !
    """
    def __init__(
        self,
        search_query: str,
        max_results=10,
        timeout=None,
        json_results=False,
        include_related_videos=False,
        youtube_session=None
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
        if youtube_session is not None:
            if not isinstance(youtube_session, YoutubeSession):
                raise InvalidArgument('youtube_session expecting YoutubeSession, got %s' % (youtube_session.__class__.__name__))

        self.search_query = search_query
        self.max_results = max_results
        self.BASE_SEARCH_URL = 'https://www.youtube.com/youtubei/v1/search?key='
        self.timeout = timeout
        self.json_results = json_results
        self.include_related_videos = include_related_videos
        self.session = youtube_session or YoutubeSession(preferred_user_agent='BOT')

    def _wrap_json(self, urls: list):
        if self.json_results:
            return json.dumps({'urls': urls})
        else:
            return urls

    def request_search(self, search_terms: str, continuation=None):
        json_data = {'context': {}}
        for i in self.session.client.keys():
            json_data['context'][i] = self.session.client[i]
        json_data['query'] = search_terms
        if continuation is not None:
            json_data['continuation'] = continuation
        r = self.session.post(self.BASE_SEARCH_URL + self.session.key, json=json_data, headers={'User-Agent': self.session.USER_AGENT})
        return json.loads(r.text)

    def main(self, legit_urls: list, event_shutdown: threading.Event):
        r = self.request_search(self.search_query)
        while True:
            # Force shutdown if True
            if event_shutdown.is_set():
                return legit_urls
            continuation = GetContinuationToken(r).get_token()
            if continuation is None:
                self.session.new_session()
                r = self.request_search(self.search_query)
                continue
            videos = GetVideosData(r, self.include_related_videos).get_videos()
            if videos is None:
                self.session.new_session()
                r = self.request_search(self.search_query)
                continue
            for i in videos:
                if i in legit_urls:
                    continue
                legit_urls.append(i)
                if len(legit_urls) > self.max_results or len(legit_urls) == self.max_results:
                    event_shutdown.set()
                    return legit_urls
            else:
                r = self.request_search(self.search_query, continuation=continuation)
                continue

    def _search(self, timeout=None):
        if timeout is None:
            legit_urls = []
            event_shutdown = threading.Event()
            return self.main(legit_urls, event_shutdown)
        else:
            legit_urls = []
            event_shutdown = threading.Event()
            f = Future()

            def internal_worker(self, f: Future, legit_urls: list, event_shutdown: threading.Event):
                f.set_running_or_notify_cancel()
                try:
                    result = self.main(legit_urls, event_shutdown)
                    f.set_result(result)
                except Exception as e:
                    f.set_exception(e)

            worker = threading.Thread(target=internal_worker, name='worker_youtube_search_requests', args=(self, f, legit_urls, event_shutdown), daemon=True)
            worker.start()
            event_shutdown.wait(timeout)
            event_shutdown.set()
            exception = f.exception()
            if exception:
                raise exception
            return legit_urls

    def search(self):
        return self._wrap_json(self._search(self.timeout))