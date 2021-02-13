"""
youtube-search-requests

Search youtube videos using requests without Youtube API.
"""
import sys

from youtube_search_requests.search import YoutubeSearch
from youtube_search_requests.session import YoutubeSession
from youtube_search_requests.async_session import AsyncYoutubeSession
from youtube_search_requests.async_search import AsyncYoutubeSearch

__VERSION__ = 'v0.1.11'