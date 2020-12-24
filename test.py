import unittest
from youtube_search_requests import YoutubeSearch, YoutubeSession, AsyncYoutubeSearch, AsyncYoutubeSession
import sys
import asyncio
from youtube_search_requests.constants import USER_AGENT_HEADERS

# For short results
BASE_TIMEOUT = 10
MAXIMUM_RESULTS = 10

# For long results
# BASE_TIMEOUT = 60
# MAXIMUM_RESULTS = 500

class InvalidReturnResults(Exception):
    pass

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

class TestAsyncYoutubeSearch(unittest.IsolatedAsyncioTestCase):

    async def test_with_given_time(self):
        y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, timeout=BASE_TIMEOUT)
        data = await y.search()
        await y.session.close()
        self.assertEqual(len(data), 10)
        self.assertIsInstance(data, list)
    
    async def test_normal(self):
        y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS)
        data = await y.search()
        await y.session.close()
        self.assertIsInstance(data, list)

    async def test_with_included_related_videos(self):
        y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, include_related_videos=True)
        data = await y.search()
        await y.session.close()
        self.assertIsInstance(data, list)

    async def test_all_user_agents(self):
        for ua in USER_AGENT_HEADERS.keys():
            session = AsyncYoutubeSession(ua)
            await session.new_session()
            youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session)
            await youtube.search()
            await youtube.session.close()

    async def test_all_user_agents_with_related_videos(self):
        for ua in USER_AGENT_HEADERS.keys():
            session = AsyncYoutubeSession(ua)
            await session.new_session()
            youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session, include_related_videos=True)
            await youtube.search()
            await youtube.session.close()


if __name__ == "__main__":
    unittest.main()