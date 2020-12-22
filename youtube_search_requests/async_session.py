# youtube-search-requests
# async_session.py

import threading
import aiohttp
import random
import asyncio
from youtube_search_requests.constants import USER_AGENT_HEADERS
from youtube_search_requests.utils import parse_json_async_session_data
from youtube_search_requests.utils.errors import InvalidArgument

class AsyncYoutubeSession(aiohttp.ClientSession):
    """
    **Same as YoutubeSession, but with async method**
    
    Normally, YoutubeSession class will automatically call new_session() when you call __init__().
    But, AsyncYoutubeSession doesn't do that, you have to call new_session()
    in order to get a new session from Youtube.

    AsyncYoutubeSession arguments

    preferred_user_agent: :class:`str` (optional, default: 'BOT')
        a User-Agent header to pass in session, 
        see constants.py to see all supported user-agents

    """
    def __init__(self, preferred_user_agent='BOT', loop: asyncio.AbstractEventLoop=None):
        super().__init__(loop=loop or asyncio.get_event_loop())
        self.BASE_URL = 'https://www.youtube.com/'
        self.BASE_SEARCH_URL = 'https://www.youtube.com/youtubei/v1/search?key='
        self.check_valid_user_agent(preferred_user_agent)
        self.preferred_user_agent = preferred_user_agent

    def check_valid_user_agent(self, user_agent: str):
        try:
            USER_AGENT_HEADERS[user_agent]
        except KeyError:
            raise InvalidArgument('invalid user-agent')

    def get_user_agent(self, preferred_user_agent: str):
        return random.choice(USER_AGENT_HEADERS[preferred_user_agent])

    async def get_session_data(self, user_agent_header=None):
        """
        coroutine / async function

        get session data from youtube
        """
        if user_agent_header is None:
            r = await self.get(self.BASE_URL)
        else:
            r = await self.get(self.BASE_URL, headers={'User-Agent': user_agent_header})
        data = await r.text()
        return await parse_json_async_session_data(data)

    def _parse_session_data(self, data):
        self.data = data
        self.key = data['INNERTUBE_API_KEY']
        self.client = data['INNERTUBE_CONTEXT']
        self.id = data['INNERTUBE_CONTEXT']['request']['sessionId']

    async def new_session(self):
        """
        coroutine / async function

        create a new session
        """
        while True:
            super().__init__()
            self.USER_AGENT = self.get_user_agent(self.preferred_user_agent)
            data = await self.get_session_data(self.USER_AGENT)
            try:
                self._parse_session_data(data)
                break
            except KeyError:
                continue