import requests
import json
import random
from youtube_search_requests.constants import USER_AGENT_HEADERS
from youtube_search_requests.utils import parse_json_session_data

class YoutubeSession:
    def __init__(self):
        self.BASE_URL = 'https://www.youtube.com/'
        self.BASE_SEARCH_URL = 'https://www.youtube.com/youtubei/v1/search?key='
        self.new_session()

    def get_session_data(self, user_agent_header=None):
        if user_agent_header is None:
            r = requests.get(self.BASE_URL)
        else:
            r = requests.get(self.BASE_URL, headers={'User-Agent': user_agent_header})
        return parse_json_session_data(r)

    def parse_session_data(self, data):
        self.data = data
        self.key = data['INNERTUBE_API_KEY']
        self.client = data['INNERTUBE_CONTEXT']
        self.id = data['INNERTUBE_CONTEXT']['request']['sessionId']

    def new_session(self):
        while True:
            self.USER_AGENT = random.choice(USER_AGENT_HEADERS)
            data = self.get_session_data(self.USER_AGENT)
            try:
                self.parse_session_data(data)
                break
            except KeyError:
                continue


