# youtube-search-requests
# parser/constants.py

import youtube_search_requests.parser.continuation_token as ct
import youtube_search_requests.parser.video_data as vd
import youtube_search_requests.parser.related_video_data as rvd

# all methods for getting continuation token
PARSER_CONTINUATION_TOKEN_METHODS = [
    ct.parse_continuation_token1,
    ct.parse_continuation_token2,
    ct.parse_continuation_token3,
    ct.parse_continuation_token4,
    ct.parse_continuation_token5,
    ct.parse_continuation_token6,
    ct.parse_continuation_token7
]

# all methods for getting video data
# This can be used for getting playlists and channels
PARSER_VIDEO_DATA_METHODS = [
    vd.parse_video_data1,
    vd.parse_video_data2,
    vd.parse_video_data3
]

# all methods for getting related video data
PARSER_RELATED_VIDEO_DATA_METHODS = [
    rvd.parse_related_video_data2,
    rvd.parse_related_video_data1,
    rvd.parse_related_video_data3,
    rvd.parse_related_video_data4
]

# list of video types
# (mobile or desktop)
VIDEO_RENDERER_DATA_TYPES = [
    'compactVideoRenderer',
    'videoRenderer'
]

# list of playlist types
# (mobile or desktop)
PLAYLIST_RENDERER_DATA_TYPES = [
    'compactPlaylistRenderer',
    'playlistRenderer'
]