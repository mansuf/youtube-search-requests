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
        try:
            self.client = data['INNERTUBE_CONTEXT']
        except KeyError as e:
            print(data)
            raise e
        self.id = data['INNERTUBE_CONTEXT']['request']['sessionId']

    def new_session(self):
        self.USER_AGENT = random.choice(USER_AGENT_HEADERS)
        data = self.get_session_data(self.USER_AGENT)
        self.parse_session_data(data)

    def request_search(self, search_query: str):
        json_data = {'context': {}}
        for i in self.client.keys():
            json_data['context'][i] = self.client[i]
        json_data['query'] = search_query
        r = requests.post(self.BASE_SEARCH_URL + self.key, json=json_data, headers={'User-Agent': self.USER_AGENT})
        return r
