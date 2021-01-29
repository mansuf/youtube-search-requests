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

    def test_with_restricted_mode(self):
        y = YoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, safe_search=True)
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

    def test_all_user_agents_with_related_videos_and_restricted_mode(self):
        for ua in USER_AGENT_HEADERS.keys():
            session = YoutubeSession(ua)
            youtube = YoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, youtube_session=session, include_related_videos=True, safe_search=True)
            youtube.search()

# checking if python3 support asyncio test case
try:
    unittest.IsolatedAsyncioTestCase('test')
# For python 3.8 lower
except AttributeError:
    class TestAsyncYoutubeSearch(unittest.TestCase):
        def test_with_given_time(self):
            async def worker():
                y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, timeout=BASE_TIMEOUT)
                data = await y.search()
                await y.session.close()
                return data
            loop = asyncio.new_event_loop()
            data = loop.run_until_complete(worker())
            self.assertEqual(len(data), 10)
            self.assertIsInstance(data, list)
        
        def test_normal(self):
            async def worker():
                y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS)
                data = await y.search()
                await y.session.close()
                return data
            loop = asyncio.new_event_loop()
            data = loop.run_until_complete(worker())
            self.assertIsInstance(data, list)

        def test_with_restricted_mode(self):
            async def worker():
                y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, safe_search=True)
                data = await y.search()
                await y.session.close()
                return data
            loop = asyncio.new_event_loop()
            data = loop.run_until_complete(worker())
            self.assertIsInstance(data, list)

        def test_with_included_related_videos(self):
            async def worker():
                y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, include_related_videos=True)
                data = await y.search()
                await y.session.close()
                return data
            loop = asyncio.new_event_loop()
            data = loop.run_until_complete(worker())
            self.assertIsInstance(data, list)

        def test_all_user_agents(self):
            async def worker():
                for ua in USER_AGENT_HEADERS.keys():
                    session = AsyncYoutubeSession(ua)
                    await session.new_session()
                    youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session)
                    await youtube.search()
                    await youtube.session.close()
            loop = asyncio.new_event_loop()
            loop.run_until_complete(worker())
            

        def test_all_user_agents_with_related_videos(self):
            async def worker():
                for ua in USER_AGENT_HEADERS.keys():
                    session = AsyncYoutubeSession(ua)
                    await session.new_session()
                    youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session, include_related_videos=True)
                    await youtube.search()
                    await youtube.session.close()
            loop = asyncio.new_event_loop()
            loop.run_until_complete(worker())
        
        def test_all_user_agents_with_related_videos_and_restricted_mode(self):
            async def worker():
                for ua in USER_AGENT_HEADERS.keys():
                    session = AsyncYoutubeSession(ua)
                    await session.new_session()
                    youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session, include_related_videos=True, safe_search=True)
                    await youtube.search()
                    await youtube.session.close()
            loop = asyncio.new_event_loop()
            loop.run_until_complete(worker())
# For python3.8 upper
except ValueError:
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

        async def test_with_restricted_mode(self):
            y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, safe_search=True)
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

        async def test_all_user_agents_with_related_videos_and_restricted_mode(self):
            for ua in USER_AGENT_HEADERS.keys():
                session = AsyncYoutubeSession(ua)
                await session.new_session()
                youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session, include_related_videos=True, safe_search=True)
                await youtube.search()
                await youtube.session.close()

if __name__ == "__main__":
    unittest.main()