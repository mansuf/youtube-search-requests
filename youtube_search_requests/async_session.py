# youtube-search-requests
# async_session.py

import threading
import aiohttp
import random
import asyncio
import json
import warnings
from youtube_search_requests.constants import USER_AGENT_HEADERS
from youtube_search_requests.utils import parse_json_async_session_data, YoutubePreferenceCookie
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
    loop: :class:`asyncio.AbstractEventLoop` (optional, default: None)
        a event loop to pass in session
    restricted_mode: :class:`bool` (optional, default: False)
        This helps hide potentially mature videos.
        No filter is 100% accurate.
    """
    def __init__(self, preferred_user_agent='BOT', loop: asyncio.AbstractEventLoop=None, restricted_mode: bool=False):
        super().__init__(loop=loop or asyncio.get_event_loop())
        self.BASE_URL = 'https://www.youtube.com/'
        self.BASE_SEARCH_URL = 'https://www.youtube.com/youtubei/v1/search?key='
        self.check_valid_user_agent(preferred_user_agent)
        self.preferred_user_agent = preferred_user_agent
        self.restricted_mode = restricted_mode
        self._RESTRICTED_MODE_PREFERENCE = 'f2=8000000'

    def check_valid_user_agent(self, user_agent: str):
        try:
            USER_AGENT_HEADERS[user_agent]
        except KeyError:
            raise InvalidArgument('invalid user-agent')

    def get_user_agent(self, preferred_user_agent: str):
        return random.choice(USER_AGENT_HEADERS[preferred_user_agent])

    def _parse_preference_cookies(self):
        c = YoutubePreferenceCookie()
        if self.restricted_mode:
            c.add_preference(self._RESTRICTED_MODE_PREFERENCE)
        return c.get_cookie()

    # TODO: add external cookies support
    def _parse_cookies(self):
        return self._parse_preference_cookies()

    async def get_session_data(self, user_agent_header=None):
        """
        coroutine / async function

        get session data from youtube
        """
        if user_agent_header is None:
            r = await self.get(self.BASE_URL, cookies=self._parse_cookies())
        else:
            r = await self.get(self.BASE_URL, headers={'User-Agent': user_agent_header}, cookies=self._parse_cookies())
        data = await r.text()
        return await parse_json_async_session_data(data)

    def _parse_session_data(self, data):
        self.data = data
        self.key = data['INNERTUBE_API_KEY']
        self.client = data['INNERTUBE_CONTEXT']
        try:
            self.id = data['INNERTUBE_CONTEXT']['request']['sessionId']
        except KeyError:
            # if error occured when getting session id
            # that mean, youtube doesn't give session id
            # it not a big problem, so its okay.
            self.id = None

    async def new_session(self):
        """
        coroutine / async function

        create a new session
        """
        while True:
            super().__init__()
            self.USER_AGENT = self.get_user_agent(self.preferred_user_agent)
            try:
                data = await self.get_session_data(self.USER_AGENT)
            except json.decoder.JSONDecodeError:
                warnings.warn('unsupported user-agent: %s' % (self.USER_AGENT))
                continue
            try:
                self._parse_session_data(data)
                break
            except KeyError:
                continue