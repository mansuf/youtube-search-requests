# youtube-search-requests 
# utils.__init__.py
import json
import requests
from youtube_search_requests.utils.errors import InvalidURL

def parse_json_session_data(r: requests.Request):
    d = r.text[r.text.find('ytcfg.set({') + 10:]
    return json.loads(d[0:d.find(');')])

async def parse_json_async_session_data(s: str):
    d = s[s.find('ytcfg.set({') + 10:]
    return json.loads(d[0:d.find(');')])

class SearchRelatedVideos:
    def __init__(self, url: str):
        if 'https://www.youtube.com/watch?v=' in url:
            pass
        elif 'https://youtu.be/' in url:
            pass
        else:
            raise InvalidURL('invalid url')
        self.url = url
        self._LIST_VIDEO_RENDERER_DATA_TYPE = [
            'compactVideoRenderer',
            'videoRenderer'
        ]

    def _wrap_dict_related_videos(self, data: str):
        startpos = data.find('var ytInitialData = ')
        text2 = data[startpos+20:]
        endpos = text2.find('"}};</script>') + 3
        return json.loads(text2[:endpos])

    def _get_info(self, data: dict, info: str):
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

    def _get_url(self, data):
        return 'https://www.youtube.com/watch?v=%s' % (data['videoId'])
    
    def _get_thumbnails(self, data):
        return data['thumbnail']['thumbnails']

    def _request_search(self, url: str):
        r = requests.get(url)
        return r.text

    def _get_related_videos(self, data: dict):
        d = data['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results']
        videos = []
        v = None
        for info in d:
            for i in self._LIST_VIDEO_RENDERER_DATA_TYPE:
                try:
                    v = info[i]
                except KeyError:
                    continue
            if v is None:
                continue
            try:
                videos.append({
                    'title': self._get_info(v, 'title'),
                    'url': self._get_url(v),
                    'thumbnails': self._get_thumbnails(v),
                    'uploader': self._get_info(v, 'longBylineText'),
                    'publishedSince': self._get_info(v, 'publishedTimeText'),
                    'views': self._get_info(v, 'viewCountText'),
                    'durations': self._get_info(v, 'lengthText')
                })
            except KeyError:
                continue
        return videos


    def get_related_videos(self):
        data = self._request_search(self.url)
        try:
            dict_data = self._wrap_dict_related_videos(data)
        except json.decoder.JSONDecodeError:
            return None
        try:
            return self._get_related_videos(dict_data)
        except KeyError:
            return None

class GetVideosData:
    def __init__(self, dict_data: dict, include_related_videos=False, use_short_link=False):
        self.data = dict_data
        self.include_related_videos = include_related_videos
        self.use_short_link = use_short_link
        self._LIST_VIDEO_RENDERER_DATA_TYPE = [
            'compactVideoRenderer',
            'videoRenderer'
        ]
        self._PARSE_METHODS = [
            self._parse_method1,
            self._parse_method2,
            self._parse_method3
        ]

    def _parse_method1(self, data):
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

    def _parse_method2(self, data):
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

    def _parse_method3(self, data):
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

    def _get_videos(self):
        for i in self._PARSE_METHODS:
            t1 = i(self.data)
            if t1 is not None:
                return t1
        return None

    def get_related_videos(self, url: str):
        if self.include_related_videos:
            s = SearchRelatedVideos(url)
            return s.get_related_videos()
        else:
            return None

    def _get_info(self, data: dict, info: str):
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

    def _get_url(self, data):
        if self.use_short_link:
            return 'https://youtu.be/%s' % (data['videoId'])
        else:
            return 'https://www.youtube.com/watch?v=%s' % (data['videoId'])
    
    def _get_thumbnails(self, data):
        return data['thumbnail']['thumbnails']

    def get_videos(self):
        videos = []
        data = self._get_videos()
        if data is None:
            return None
        v = None
        for info in data:
            for i in self._LIST_VIDEO_RENDERER_DATA_TYPE:
                try:
                    v = info[i]
                except KeyError:
                    continue
            if v is None:
                continue
            try:
                videos.append({
                    'title': self._get_info(v, 'title'),
                    'url': self._get_url(v),
                    'thumbnails': self._get_thumbnails(v),
                    'uploader': self._get_info(v, 'longBylineText'),
                    'publishedSince': self._get_info(v, 'publishedTimeText'),
                    'views': self._get_info(v, 'viewCountText'),
                    'durations': self._get_info(v, 'lengthText'),
                    'related_videos': self.get_related_videos('https://www.youtube.com/watch?v=%s' % (v['videoId']))
                })
            except KeyError:
                continue
        return videos


class GetContinuationToken:
    def __init__(self, dict_data: dict):
        self.data = dict_data
        self._PARSE_METHODS = [
            self._parse_method1,
            self._parse_method2,
            self._parse_method3
        ]

    def _parse_method1(self, data):
        try:
            init = data['onResponseReceivedCommands']
        except KeyError:
            return None
        d = None
        for a in init:
            try:
                d = a['appendContinuationItemsAction']['continuationItems']
            except KeyError:
                continue
        if d is None:
            return None
        for i in d:
            try:
                return i['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
            except KeyError:
                continue
        return None

    def _parse_method2(self, data):
        try:
            d = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
        except KeyError:
            return None
        for i in d:
            try:
                return i['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
            except KeyError:
                continue
        return None

    def _parse_method3(self, data):
        try:
            d = data['contents']['sectionListRenderer']['contents']
        except KeyError:
            return None
        for i in d:
            try:
                return i['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
            except KeyError:
                continue
        return None

    def get_token(self):
        for i in self._PARSE_METHODS:
            t1 = i(self.data)
            if t1 is not None:
                return t1
        return None
