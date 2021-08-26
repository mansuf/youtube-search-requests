# youtube-search-requests 
# constants.py

import random
from urllib.parse import quote

# all Youtube URLs
BASE_YOUTUBE_URL = 'https://www.youtube.com/'
BASE_YOUTUBE_SEARCH_INTERNAL_API_URL = 'https://www.youtube.com/youtubei/v1/search?key='
BASE_YOUTUBE_SEARCH_QUERY_URL = 'https://www.youtube.com/results?search_query='
BASE_YOUTUBE_SHORT_URL = 'https://youtu.be/'
BASE_YOUTUBE_CHANNEL_URL = 'https://www.youtube.com/channel/'
BASE_YOUTUBE_WATCH_URL = 'https://www.youtube.com/watch?v='
BASE_YOUTUBE_PLAYLIST_URL = 'https://www.youtube.com/playlist?list='
BASE_YOUTUBE_SEARCH_RELATED_VIDEOS_INTERNAL_API_URL = 'https://www.youtube.com/youtubei/v1/next?key='


# all types filters.
ALL_FILTERS = {
    'PLAYLISTS_FILTER': quote('EgIQAw=='),
    'CHANNELS_FILTER': quote('EgIQAg=='),
    'VIDEOS_FILTER': quote('EgIQAQ==')
}

# all videos filters.
# HD, 4K, live videos and etc.
ALL_VIDEOS_FILTERS = {
    'LEN<4MIN': 'EgQQARgB', # videos with length less than 4 minutes
    'LEN>20MIN': 'EgQQARgC', # videos with length more than 20 minutes
    'LIVE': 'EgQQAUAB', # live videos
    '4K': 'EgQQAXAB', # 4K videos
    'HD': 'EgQQASAB', # HD videos
    'WITH_SUBTITLES': 'EgQQASgB', # videos with subtitles
    'VR360': 'EgQQAXgB', # videos with VR 360 support
    'VR180': quote('EgUQAdABAQ=='), # videos with VR 180 support
    '3D': 'EgQQATgB', # videos with 3D support
    'HDR': quote('EgUQAcgBAQ=='), # videos with HDR support
    'NO_FILTER': ALL_FILTERS['VIDEOS_FILTER'] # videos with no filter
}

# NEED DOCUMENTATION !!!
# all valid languages in youtube
VALID_LANGUAGES = [
    'af', 
    'az',
    'id', 
    'ms',
    'bs',
    'ca',
    'cs',
    'da',
    'de',
    'et',
    'en-IN',
    'en-GB',
    'en',
    'es',
    'es-419',
    'es-US',
    'eu',
    'fil',
    'fr',
    'fr-CA',
    'gl',
    'hr',
    'zu',
    'is',
    'sw',
    'lv',
    'lt',
    'hu',
    'nl',
    'no',
    'uz',
    'sq',
    'vi',
    'tr',
    'be',
    'bg',
    'ky',
    'kk',
    'mn',
    'ru',
    'sr',
    'uk',
    'el',
    'hy',
    'iw',
    'ur',
    'ar',
    'fa',
    'ne',
    'mr',
    'as',
    'bn',
    'pa',
    'gu',
    'or',
    'ta',
    'te',
    'kn',
    'si',
    'th',
    'lo',
    'my',
    'ka',
    'am',
    'km',
    'zh-CN',
    'zh-TW',
    'zh-HK',
    'ja',
    'ko'
]

# TODO: Finish this !!!
VALID_REGIONS = [
    'ID',
    'US'
]