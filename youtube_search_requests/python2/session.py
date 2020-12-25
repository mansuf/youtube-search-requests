# youtube-search-requests
# python2/session.py

import json
import random
from requests import Session
from youtube_search_requests.constants import USER_AGENT_HEADERS
from youtube_search_requests.utils import parse_json_session_data
from youtube_search_requests.utils.errors import InvalidArgument

# Because i don't know how to subclass in python 2
# i will do it in old way
class YoutubeSession:
    """
    YoutubeSession arguments

    preferred_user_agent: :class:`str` (optional, default: 'BOT')
        a User-Agent header to pass in session, 
        see constants.py to see all supported user-agents

    """
    def __init__(self, preferred_user_agent='BOT'):
        self.BASE_URL = 'https://www.youtube.com/'
        self.BASE_SEARCH_URL = 'https://www.youtube.com/youtubei/v1/search?key='
        self.check_valid_user_agent(preferred_user_agent)
        self._subclass = Session()
        self.preferred_user_agent = preferred_user_agent
        self.new_session()

    def check_valid_user_agent(self, user_agent):
        try:
            USER_AGENT_HEADERS[user_agent]
        except KeyError:
            raise InvalidArgument('invalid user-agent')

    def get_user_agent(self, preferred_user_agent):
        return random.choice(USER_AGENT_HEADERS[preferred_user_agent])

    def get(self, url, **kwargs):
        return self._subclass.get(url, **kwargs)

    def post(self, url, **kwargs):
        return self._subclass.post(url, **kwargs)

    def get_session_data(self, user_agent_header=None):
        if user_agent_header is None:
            r = self.get(self.BASE_URL)
        else:
            r = self.get(self.BASE_URL, headers={'User-Agent': user_agent_header})
        return parse_json_session_data(r)

    def _parse_session_data(self, data):
        self.data = data
        self.key = data['INNERTUBE_API_KEY']
        self.client = data['INNERTUBE_CONTEXT']
        self.id = data['INNERTUBE_CONTEXT']['request']['sessionId']

    def new_session(self):
        while True:
            self._subclass = Session()
            self.USER_AGENT = self.get_user_agent(self.preferred_user_agent)
            data = self.get_session_data(self.USER_AGENT)
            try:
                self._parse_session_data(data)
                break
            except KeyError:
                continue


