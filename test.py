import unittest
import sys
from youtube_search_requests.constants import USER_AGENT_HEADERS

if sys.version_info.major == 2:
    from youtube_search_requests import YoutubeSearch, YoutubeSession
else:
    from youtube_search_requests import YoutubeSearch, YoutubeSession, AsyncYoutubeSearch, AsyncYoutubeSession

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

# if python version is 2, this test won't be executed
if sys.version_info.major != 2:
    # For python3.8 upper
    script_py3 = """
    try:
        unittest.IsolatedAsyncioTestCase('test')
        import asyncio
        class TestAsyncYoutubeSearch(unittest.IsolatedAsyncioTestCase):
            @asyncio.coroutine
            def test_with_given_time(self):
                y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, timeout=BASE_TIMEOUT)
                data = await y.search()
                await y.session.close()
                self.assertEqual(len(data), 10)
                self.assertIsInstance(data, list)

            @asyncio.coroutine
            def test_normal(self):
                y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS)
                data = await y.search()
                await y.session.close()
                self.assertIsInstance(data, list)

            @asyncio.coroutine
            def test_with_included_related_videos(self):
                y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, include_related_videos=True)
                data = await y.search()
                await y.session.close()
                self.assertIsInstance(data, list)

            @asyncio.coroutine
            def test_all_user_agents(self):
                for ua in USER_AGENT_HEADERS.keys():
                    session = AsyncYoutubeSession(ua)
                    await session.new_session()
                    youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session)
                    await youtube.search()
                    await youtube.session.close()

            @asyncio.coroutine
            def test_all_user_agents_with_related_videos(self):
                for ua in USER_AGENT_HEADERS.keys():
                    session = AsyncYoutubeSession(ua)
                    await session.new_session()
                    youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session, include_related_videos=True)
                    await youtube.search()
                    await youtube.session.close()
    # For python 3.8 lower
    except AttributeError:
        class TestAsyncYoutubeSearch(unittest.TestCase):
            def test_with_given_time(self):
                @asyncio.coroutine
                def worker():
                    y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, timeout=BASE_TIMEOUT)
                    data = await y.search()
                    await y.session.close()
                    return data
                loop = asyncio.new_event_loop()
                data = loop.run_until_complete(worker())
                self.assertEqual(len(data), 10)
                self.assertIsInstance(data, list)
            
            def test_normal(self):
                @asyncio.coroutine
                def worker():
                    y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS)
                    data = await y.search()
                    await y.session.close()
                    return data
                loop = asyncio.new_event_loop()
                data = loop.run_until_complete(worker())
                self.assertIsInstance(data, list)

            def test_with_included_related_videos(self):
                @asyncio.coroutine
                def worker():
                    y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, include_related_videos=True)
                    data = await y.search()
                    await y.session.close()
                    return data
                loop = asyncio.new_event_loop()
                data = loop.run_until_complete(worker())
                self.assertIsInstance(data, list)

            def test_all_user_agents(self):
                @asyncio.coroutine
                def worker():
                    for ua in USER_AGENT_HEADERS.keys():
                        session = AsyncYoutubeSession(ua)
                        await session.new_session()
                        youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session)
                        await youtube.search()
                        await youtube.session.close()
                loop = asyncio.new_event_loop()
                loop.run_until_complete(worker())
                

            def test_all_user_agents_with_related_videos(self):
                @asyncio.coroutine
                def worker():
                    for ua in USER_AGENT_HEADERS.keys():
                        session = AsyncYoutubeSession(ua)
                        await session.new_session()
                        youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session, include_related_videos=True)
                        await youtube.search()
                        await youtube.session.close()
                loop = asyncio.new_event_loop()
                loop.run_until_complete(worker())
    except ValueError:
        class TestAsyncYoutubeSearch(unittest.IsolatedAsyncioTestCase):
            @asyncio.coroutine
            def test_with_given_time(self):
                y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, timeout=BASE_TIMEOUT)
                data = await y.search()
                await y.session.close()
                self.assertEqual(len(data), 10)
                self.assertIsInstance(data, list)
            
            @asyncio.coroutine
            def test_normal(self):
                y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS)
                data = await y.search()
                await y.session.close()
                self.assertIsInstance(data, list)

            @asyncio.coroutine
            def test_with_included_related_videos(self):
                y = AsyncYoutubeSearch('gordon ramsay', json_results=False, max_results=MAXIMUM_RESULTS, include_related_videos=True)
                data = await y.search()
                await y.session.close()
                self.assertIsInstance(data, list)

            @asyncio.coroutine
            def test_all_user_agents(self):
                for ua in USER_AGENT_HEADERS.keys():
                    session = AsyncYoutubeSession(ua)
                    await session.new_session()
                    youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session)
                    await youtube.search()
                    await youtube.session.close()

            @asyncio.coroutine
            def test_all_user_agents_with_related_videos(self):
                for ua in USER_AGENT_HEADERS.keys():
                    session = AsyncYoutubeSession(ua)
                    await session.new_session()
                    youtube = AsyncYoutubeSearch('gordon ramsay', max_results=MAXIMUM_RESULTS, json_results=False, async_youtube_session=session, include_related_videos=True)
                    await youtube.search()
                    await youtube.session.close()
    """
    exec(script_py3)

if __name__ == "__main__":
    unittest.main()