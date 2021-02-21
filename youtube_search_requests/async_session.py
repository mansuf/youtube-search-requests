# youtube-search-requests
# async_session.py

import aiohttp
import random
import asyncio
import json
import warnings
from youtube_search_requests.constants import USER_AGENT_HEADERS, BASE_YOUTUBE_URL
from youtube_search_requests.utils import (
    parse_json_async_session_data,
    # check_valid_regions, # TODO: add this to next release
    check_valid_language,
    check_valid_user_agent,
    YoutubeCookies
)
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
    cookies: :class:`youtube_search_requests.utils.YoutubeCookies` (optional, default: None) 
        a Youtube cookies.
        You can set language and restricted mode
        and put additional cookies in YoutubeCookies.
    """
    # TODO: add this to next release on class comment
    # region: :class:`str` or :class:`NoneType` (optional: default: None)
    # set the results region, see constants.py to see all valid regions

    def __init__(
        self,
        preferred_user_agent='BOT',
        loop: asyncio.AbstractEventLoop=None,
        cookies: YoutubeCookies=None
    ):
        super().__init__(loop=loop or asyncio.get_event_loop())
        self.BASE_URL = BASE_YOUTUBE_URL

        # Check valid user-agent
        check_valid_user_agent(preferred_user_agent)
        self.preferred_user_agent = preferred_user_agent

        # set cookies
        _cookies = YoutubeCookies()
        _cookies.set_language('en')
        self._cookies = cookies or _cookies

        # TODO: add this to next release
        # if region is not None:
        #     check_valid_regions(region)
        #     self._region = region
        # else:
        #     self._region = None

    def get_user_agent(self, preferred_user_agent: str):
        if preferred_user_agent == 'RANDOM':
            return USER_AGENT_HEADERS[preferred_user_agent]()
        else:
            return random.choice(USER_AGENT_HEADERS[preferred_user_agent])

    # TODO: add this to next release
    # def _get_geolocation(self):
    #     if self._region is None:
    #         return ''
    #     else:
    #         return '?persist_gl=1&gl=' + self._region

    async def get_session_data(self, user_agent_header=None):
        """
        coroutine / async function

        get session data from youtube
        """
        if user_agent_header is None:
            r = await self.get(self.BASE_URL, cookies=self._cookies.get_cookies())
        else:
            r = await self.get(
                self.BASE_URL,
                headers={'User-Agent': user_agent_header},
                cookies=self._cookies.get_cookies()
            )
        return await parse_json_async_session_data(r)

    def _parse_session_data(self, data):
        self.data = data
        self.key = data['INNERTUBE_API_KEY']
        self.context = data['INNERTUBE_CONTEXT']
        self.client = data['INNERTUBE_CONTEXT']['client']
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
            super().__init__(loop= self.loop)
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
