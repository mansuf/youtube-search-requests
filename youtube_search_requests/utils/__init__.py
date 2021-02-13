# youtube-search-requests 
# utils.__init__.py

import json
from youtube_search_requests.constants import (
    VALID_LANGUAGES,
    VALID_USER_AGENTS,
    USER_AGENT_HEADERS
)
from youtube_search_requests.utils.errors import InvalidArgument

def parse_json_session_data(r):
    d = r.text[r.text.find('ytcfg.set({') + 10:]
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