"""
youtube-search-requests

Search youtube videos using requests without Youtube API.
youtube-search-requests only extract urls.
To process another information in urls you need to install youtube-dl.
"""
import sys
import requests
import threading
import urllib
import json
from youtube_search_requests.constants import USER_AGENT_HEADERS
from youtube_search_requests.utils import *

__VERSION__ = 'v0.0.16'

try:
    import youtube_dl
    import_youtube_dl = True
except ImportError:
    import_youtube_dl = False

class YoutubeSearch:
    def __init__(
        self,
        search_query: str,
        max_results=10,
        validate=True,
        timeout=None,
        extract_info=False,
        json_results=False,
        include_related_videos=False,
    ):
        """
        YoutubeSearch arguments

        search_query: :class:`str`
            a string terms want to search
        max_results: :class:`int` (optional, default: 10)
            maximum search results
        validate: :class:`bool` (optional, default: True)
            validate url results, validating urls takes too much times but it worth to prevent UNPLAYABLE or ERROR videos
        timeout: :class:`int` or :class:`NoneType` (optional, default: None)
            give number of times to execute search, if times runs out, search stopped & returning results
        extract_info: :class:`bool` (optional, default: False)
            Extract additional info in urls, NOTE: you need to install youtube-dl module to extract additional info (pip install youtube-dl)
        json_results: :class:`bool` (optional, default: False)
            if True, Return results in json format. If False return results in dict format
        include_related_videos: :class:`bool` (optional, default: False)
            include all related videos each url's
        """

        # Validate the arguments
        if not isinstance(search_query, str):
            raise InvalidArgument('search_query expecting str, got %s' % (search_query.__class__.__name__))
        if not isinstance(max_results, int):
            raise InvalidArgument('max_results expecting int, got %s' % (max_results.__class__.__name__))
        if not isinstance(validate, bool):
            raise InvalidArgument('validate expecting bool, got %s' % (validate.__class__.__name__))
        if timeout is not None:
            if not isinstance(timeout, int):
                raise InvalidArgument('timeout expecting int or NoneType, got %s' % (timeout.__class__.__name__))
        if not isinstance(extract_info, bool):
            raise InvalidArgument('extract_info expecting bool, got %s' % (extract_info.__class__.__name__))
        if not isinstance(json_results, bool):
            raise InvalidArgument('json_results expecting bool, got %s' % (json_results.__class__.__name__))
        if not isinstance(include_related_videos, bool):
            raise InvalidArgument('include_related_videos expecting bool, got %s' % (include_related_videos.__class__.__name__))

        self.search_query = search_query
        self.max_results = max_results
        self.BASE_URL = 'https://www.youtube.com/results?search_query='
        self.validate = validate
        self.timeout = timeout
        self.extract_info = extract_info
        self.json_results = json_results
        self.include_related_videos = include_related_videos
        # wait event shutdown worker
        self._wait_event = None

        # Each headers give different results
        # this give advantages to query more results
        self.headers = [{'User-Agent': i} for i in USER_AGENT_HEADERS]

    def _parse_urls(self, r: requests.Response):
        pos = r.text.find('/watch?v=')
        list_videos = []
        while True:
            endpos = pos + 9 + 11 # columns "/watch?v=": 9, columns youtube video id: 11
            url = r.text[pos:endpos]
            pos = r.text.find('/watch?v=', endpos)
            if 'https://www.youtube.com%s' % (url) in list_videos:
                pass
            elif url == '':
                pass
            else:
                list_videos.append('https://www.youtube.com%s' % (url))
            if pos == -1:
                return list_videos

    def validate_url(self, url: str):
        """
        Validate a youtube url

        return True if valid,
        return False if not valid
        """
        if 'https://www.youtube.com/watch?v=' in url:
            pass
        elif 'https://youtu.be/' in url:
            pass
        else:
            raise InvalidURL('invalid url')
        r = requests.get(url).text
        # if video is Unavailable returning False
        if r.find('{"status":"ERROR","reason"') != -1:
            return False
        # if video is unlisted or private returning False
        elif r.find('{"status":"UNPLAYABLE","reason"') != -1:
            return False
        # if video is live stream but offline returning False
        elif r.find('LIVE_STREAM_OFFLINE') != -1:
            return False
        else:
            return True

    def _extract_thumbnail(self, info: dict):
        try:
            return info['thumbnails']
        except KeyError:
            return [info['thumbnail']]
        else:
            return None

    def _extract_related_videos(self, url):
        """
        extract all related videos in given url

        NOTE: with validate, extract_info options enabled, the search can be really-really slow

        """
        if not self.include_related_videos:
            return None
        legit_urls = []
        r = requests.get(url)
        urls = self._parse_urls(r)
        for i in urls:
            if i == url:
                continue
            if self.validate:
                if self.validate_url(i):
                    pass
                else:
                    continue
            else:
                pass
            if self.extract_info:
                if import_youtube_dl:
                    try:
                        y = youtube_dl.YoutubeDL(params={'quiet': True, 'no_warnings': True})
                        info = y.extract_info(i, download=False, process=False)
                        legit_urls.append({'title': info['title'], 'url': i, 'author': info['uploader'], 'thumbnails': self._extract_thumbnail(info)})
                    except youtube_dl.utils.DownloadError:
                        legit_urls.append({'title': None, 'url': i, 'author': None, 'thumbnails': None})
                else:
                    raise ModuleNotFoundError('youtube-dl module not found, please install it')
            else:
                legit_urls.append(i)
        return legit_urls
        
        

    def _extract_info(self, url: str):
        """
        if module youtube-dl is imported.
        Extract all information in that url.

        if not, just return the url.
        """
        if self.extract_info:
            if import_youtube_dl:
                try:
                    y = youtube_dl.YoutubeDL(params={'quiet': True, 'no_warnings': True})
                    info = y.extract_info(url, download=False, process=False)
                    return {'title': info['title'], 'url': url, 'author': info['uploader'], 'thumbnails': self._extract_thumbnail(info), 'related_videos': self._extract_related_videos(url)}
                except youtube_dl.utils.DownloadError:
                    return {'title': None, 'url': url, 'author': None, 'thumbnails': None, 'related_videos': None}
            else:
                raise ModuleNotFoundError('youtube-dl module not found, please install it')
        else:
            if self.include_related_videos:
                return {'url': url, 'related_videos': self._extract_related_videos(url)}
            else:
                return url

    def _wrap_json(self, urls: list):
        if self.json_results:
            return json.dumps({'urls': urls})
        else:
            return urls

    def _run_search(self, legit_urls=[], event_shutdown=threading.Event()):
        while True:
            for header in self.headers:
                # Force shutdown if True
                if event_shutdown.is_set():
                    return legit_urls
                r = requests.get(self.BASE_URL + urllib.parse.quote(self.search_query.replace(' ', '+')), headers=header)
                urls = self._parse_urls(r)
                for url in urls:
                    if url in legit_urls:
                        continue
                    if self.validate:
                        if self.validate_url(url):
                            legit_urls.append(self._extract_info(url))
                        else:
                            continue
                    else:
                        legit_urls.append(self._extract_info(url))
                    if len(legit_urls) == self.max_results or len(legit_urls) > self.max_results:
                        event_shutdown.set()
                        return legit_urls


    def _search(self, timeout=None):
        if timeout is None:
            urls = []
            event = threading.Event()
            return self._run_search(legit_urls=urls, event_shutdown=event)
        else:
            wait_event = threading.Event()
            legit_urls = []
            self._wait_event = wait_event
            worker = threading.Thread(target=self._run_search, name='worker_youtube_search_requests', args=(legit_urls, wait_event), daemon=True)
            worker.start()
            wait_event.wait(timeout)
            wait_event.set()
            return legit_urls

    def search(self):
        return self._wrap_json(self._search(self.timeout))
                
                


