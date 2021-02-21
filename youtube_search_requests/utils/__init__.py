# youtube-search-requests 
# utils.__init__.py

import json
from youtube_search_requests.constants import (
    VALID_LANGUAGES,
    VALID_USER_AGENTS,
    USER_AGENT_HEADERS
)
from youtube_search_requests.utils.errors import InvalidArgument

class YoutubeCookies:
    def __init__(self):
        self.cookies = {'PREF': {}}

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

    def set_restricted_mode(self):
        try:
            self.cookies['PREF']['f2']
        except KeyError:
            self.add_preference('f2', '8000000')
        else:
            pass

    def unset_restricted_mode(self):
        try:
            del self.cookies['PREF']['f2']
        except KeyError:
            pass

    def set_language(self, lang='en'):
        try:
            self.cookies['PREF']['hl']
        except KeyError:
            self.add_preference('hl', lang)
        else:
            if self.cookies['PREF']['hl'] != lang:
                del self.cookies['PREF']['hl']
                self.add_preference('hl', lang)

    def add_preference(self, name: str, value: str):
        self.cookies['PREF'][name] = value

    def add_preferences(self, preference: str):
        PREF = self._parse_preference(preference)
        if isinstance(PREF, dict):
            for key in PREF.keys():
                self.cookies['PREF'][key] = PREF[key]
        else:
            self.cookies['PREF'][PREF[0]] = PREF[1]

    def add_cookie(self, name: str, value: str):
        self.cookies[name] = value

    def remove_cookie(self, name: str):
        del self.cookies[name]

    def get_cookies(self):
        PREF = self.cookies['PREF']
        a = ''
        cookies = {}
        for key in self.cookies:
            cookies[key] = self.cookies[key]
        if len(PREF.keys()) == 1:
            for key in PREF.keys():
                a += key + '=' + PREF[key]
        elif len(PREF.keys()) == 0:
            return cookies
        else:
            for key in PREF.keys():
                a += key + '=' + PREF[key] + '&'
        cookies['PREF'] = a
        return cookies

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
