import unittest

BASE_TIMEOUT = 10
MAXIMUM_RESULTS = 10
from youtube_search_requests.constants import USER_AGENT_HEADERS

from youtube_search_requests import YoutubeSearch, YoutubeSession

class TestYoutubeSearch(unittest.TestCase):

    def test_with_given_time(self):
        y = YoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, timeout=BASE_TIMEOUT)
        data = y.search()
        self.assertIsInstance(data, list)
    
    def test_normal(self):
        y = YoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS)
        data = y.search()
        self.assertIsInstance(data, list)

    def test_with_included_related_videos(self):
        y = YoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, include_related_videos=True)
        data = y.search()
        self.assertIsInstance(data, list)

    def test_all_user_agents(self):
        for ua in USER_AGENT_HEADERS.keys():
            session = YoutubeSession(ua)
            youtube = YoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, youtube_session=session)
            youtube.search()

    def test_all_user_agents_with_related_videos(self):
        for ua in USER_AGENT_HEADERS.keys():
            session = YoutubeSession(ua)
            youtube = YoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, youtube_session=session, include_related_videos=True)
            youtube.search()
