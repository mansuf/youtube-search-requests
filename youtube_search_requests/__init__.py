"""
youtube-search-requests v0.0.11

Search Videos in youtube using requests.
youtube-search-requests only extract urls.
To process another information in urls you need to install youtube-dl.
"""
import sys
import requests
import threading
from youtube_search_requests.constants import USER_AGENT_HEADERS

try:
    from youtube_dl import YoutubeDL
    import_youtube_dl = True
except ImportError:
    import_youtube_dl = False

class YoutubeSearch:
    def __init__(self, search_query: str, max_results=10, validate=True, timeout=None, extract_info=True):
        """
        YoutubeSearch arguments

        search_query: :class:`str`
            a string terms want to search
        max_results: :class:`int`
            maximum search results
        validate: :class:`bool`
            validate url results, validating urls takes too much times but it worth to prevent UNPLAYABLE or ERROR videos
        timeout: :class:`int` or :class:`NoneType`
            Need documentation !!!
        extract_info: :class:`bool`
            Need documentation !!!
        """

        self.search_query = search_query
        self.max_results = max_results
        self.BASE_URL = 'https://www.youtube.com/results?search_query='
        self.validate = validate
        self.timeout = timeout
        self.extract = extract_info

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
        r = requests.get(url).text
        if r.find('{"status":"ERROR","reason"') != -1:
            return False
        elif r.find('{"status":"UNPLAYABLE","reason"') != -1:
            return False
        else:
            return True

    def _extract_info(self, url: str):
        """
        if module youtube-dl is imported.
        Extract all information in that url.

        if not, just return the url.
        """
        if self.extract:
            if import_youtube_dl:
                y = YoutubeDL(params={'quiet': True, 'no_warnings': True})
                info = y.extract_info(url, download=False, process=False)
                return {'title': info['title'], 'url': url, 'author': info['uploader'], 'thumbnails': info['thumbnails']}
            else:
                return url


    def _run_search(self, legit_urls=[], event_shutdown=threading.Event()):
        while True:
            for header in self.headers:
                # Force return results if True
                if event_shutdown.is_set():
                    return legit_urls
                r = requests.get(self.BASE_URL + self.search_query.replace(' ', '+'), headers=header)
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
                    if len(legit_urls) == self.max_results:
                        return legit_urls

    def _search(self, timeout=None):
        if timeout is None:
            return self._run_search()
        else:
            wait_event = threading.Event()
            legit_urls = []
            worker = threading.Thread(target=self._run_search, name='worker_youtube_search_requests', args=(legit_urls, wait_event), daemon=True)
            worker.start()
            wait_event.wait(timeout)
            wait_event.set()
            return legit_urls

    def search(self):
        return self._search(self.timeout)
                
                


