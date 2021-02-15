# youtube-search-requests 
# utils.__init__.py

import json
from youtube_search_requests.constants import (
    VALID_LANGUAGES,
    VALID_USER_AGENTS,
    USER_AGENT_HEADERS
)
from youtube_search_requests.utils.errors import InvalidArgument

class YoutubePreferenceCookies:
    def __init__(self):
        self.cookie = {'PREF': {}}

    def _parse_preference(self, p: str):
        if '&' in p:
            pref = {}
            for i in p.split('&'):
                a = i.split('=')
                pref[a[0]] = a[1]
            return pref
        else:
            indexes = p.split('=')
            return indexes[0], indexes[1]

    def add_preference(self, name: str, value: str):
        self.cookie['PREF'][name] = value

    def add_preferences(self, preference: str):
        PREF = self._parse_preference(preference)
        if isinstance(PREF, dict):
            for key in PREF.keys():
                self.cookie['PREF'][key] = PREF[key]
        else:
            self.cookie['PREF'][PREF[0]] = PREF[1]

    def get_cookie(self):
        PREF = self.cookie['PREF']
        a = ''
        if len(PREF.keys()) == 1:
            for key in PREF.keys():
                a += key + '=' + PREF[key]
        elif len(PREF.keys()) == 0:
            return {}
        else:
            for key in PREF.keys():
                a += key + '=' + PREF[key] + '&'
        return {'PREF': a}

def parse_json_session_data(r):
    d = r.text[r.text.find('ytcfg.set({') + 10:]
    return json.loads(d[0:d.find(');')])

async def parse_json_async_session_data(r):
    data = await r.text()
    d = data[data.find('ytcfg.set({') + 10:]
    return json.loads(d[0:d.find(');')])


# TODO: add this to next release
# def check_valid_regions(region):
#     if region in VALID_REGIONS:
#         return
#     else:
#         raise InvalidArgument('invalid region')

def check_valid_language(lang):
    if lang in VALID_LANGUAGES:
        return
    else:
        raise InvalidArgument('invalid language')

def check_valid_user_agent(user_agent):
    try:
        USER_AGENT_HEADERS[user_agent]
    except KeyError:
        raise InvalidArgument('invalid user-agent')
