# youtube-search-requests
# parser/video_data.py

from youtube_search_requests.constants import (
    BASE_YOUTUBE_SHORT_URL,
    BASE_YOUTUBE_WATCH_URL,
    BASE_YOUTUBE_PLAYLIST_URL
)

# shorcut function for getting video info data
# commonly used for viewCountText, lengthText, etc.
def get_video_info(data, info):
    try:
        d = data[info]
    except KeyError:
        return None
    try:
        a = d['runs']
        for i in a:
            try:
                return i['text']
            except KeyError:
                continue
    except KeyError:
        pass
    try:
        return d['simpleText']
    except KeyError:
        pass
    return None

# for bot or unknown user-agent maybe ?
def parse_video_data1(data):
    try:
        init = data['onResponseReceivedCommands']
    except KeyError:
        return None
    for a in init:
        try:
            d = a['appendContinuationItemsAction']['continuationItems']
        except KeyError:
            continue
    if d is None:
        return None
    for i in d:
        try:
            return i['itemSectionRenderer']['contents']
        except KeyError:
            continue
    return None

# for mobile web browser
def parse_video_data2(data):
    try:
        d = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
    except KeyError:
        return None
    for i in d:
        try:
            return i['itemSectionRenderer']['contents']
        except KeyError:
            continue
    return None

# for desktop web browser
def parse_video_data3(data):
    try:
        d = data['contents']['sectionListRenderer']['contents']
    except KeyError:
        return None
    for i in d:
        try:
            return i['itemSectionRenderer']['contents']
        except KeyError:
            continue
    return None

# parse url video
def parse_url_video(video_id, use_short_link=False):
    if use_short_link:
        return BASE_YOUTUBE_SHORT_URL + video_id
    else:
        return BASE_YOUTUBE_WATCH_URL + video_id

# parse url playlist
def parse_watch_url_playlist(playlist_id, data, use_short_link=False):
    for i in data['videos']:
        videoId = i['childVideoRenderer']['videoId']
        break
    if use_short_link:
        return BASE_YOUTUBE_SHORT_URL + videoId + '?list=' + playlist_id
    else:
        return BASE_YOUTUBE_WATCH_URL + videoId + '?list=' + playlist_id
