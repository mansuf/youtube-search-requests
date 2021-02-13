# youtube-search-requests
# parser/__init__.py

from youtube_search_requests.constants import (
    BASE_YOUTUBE_PLAYLIST_URL
)
from .constants import (
    PARSER_CONTINUATION_TOKEN_METHODS,
    PARSER_VIDEO_DATA_METHODS,
    PARSER_RELATED_VIDEO_DATA_METHODS,
    VIDEO_RENDERER_DATA_TYPES,
    PLAYLIST_RENDERER_DATA_TYPES
)
from .video_data import (
    get_video_info,
    parse_url_video,
    parse_watch_url_playlist
)

# Getting continuation token
def get_continuation_token(data):
    for method in PARSER_CONTINUATION_TOKEN_METHODS:
        result = method(data)
        if result is not None:
            return result

def _get_video_data(data):
    for method in PARSER_VIDEO_DATA_METHODS:
        result = method(data)
        if result is not None:
            return result

# Getting video data
def get_video_data(data, use_short_link=False):
    videos = []
    vid = _get_video_data(data)
    if vid is None:
        return None
    v = None
    for info in vid:
        for i in VIDEO_RENDERER_DATA_TYPES:
            try:
                v = info[i]
            except KeyError:
                continue
        if v is None:
            continue
        try:
            videos.append({
                'title': get_video_info(v, 'title'),
                'url': parse_url_video(v['videoId'], use_short_link),
                'thumbnails': v['thumbnail']['thumbnails'],
                'uploader': get_video_info(v, 'longBylineText'),
                'publishedSince': get_video_info(v, 'publishedTimeText'),
                'views': get_video_info(v, 'viewCountText'),
                'durations': get_video_info(v, 'lengthText'),
            })
        except KeyError:
            continue
    return videos

def _get_playlists_data(data):
    for method in PARSER_VIDEO_DATA_METHODS:
        result = method(data)
        if result is not None:
            return result

def get_playlists_thumbnails(data):
    for thumbnails in data['thumbnails']:
        return thumbnails['thumbnails']

# Getting playlists data
def get_playlists_data(data, use_short_link=False):
    playlists = []
    ps = _get_playlists_data(data)
    if ps is None:
        return None
    v = None
    for info in ps:
        for i in PLAYLIST_RENDERER_DATA_TYPES:
            try:
                v = info[i]
            except KeyError:
                continue
        if v is None:
            continue
        try:
            playlists.append({
                'title': get_video_info(v, 'title'),
                'playlist_url': BASE_YOUTUBE_PLAYLIST_URL + v['playlistId'],
                'watch_url': parse_watch_url_playlist(v['playlistId'], v, use_short_link),
                'thumbnails': get_playlists_thumbnails(v),
                'uploader': get_video_info(v, 'shortBylineText'),
                'totalVideos': v['videoCount']
            })
        except KeyError:
            continue
    return playlists

def _get_related_videos(data):
    for method in PARSER_RELATED_VIDEO_DATA_METHODS:
        results = method(data)
        if results is not None:
            return results

# Getting related videos data
def get_related_videos(data, use_short_link=False):
    d = _get_related_videos(data)
    if d is None:
        return None
    videos = []
    v = None
    for info in d:
        for i in VIDEO_RENDERER_DATA_TYPES:
            try:
                v = info[i]
            except KeyError:
                continue
        if v is None:
            continue
        try:
            videos.append({
                'title': get_video_info(v, 'title'),
                'url': parse_url_video(v['videoId'], use_short_link),
                'thumbnails': v['thumbnail']['thumbnails'],
                'uploader': get_video_info(v, 'longBylineText'),
                'publishedSince': get_video_info(v, 'publishedTimeText'),
                'views': get_video_info(v, 'viewCountText'),
                'durations': get_video_info(v, 'lengthText')
            })
        except KeyError:
            continue
    return videos