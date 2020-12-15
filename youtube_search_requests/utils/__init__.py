# youtube-search-requests 
# utils.__init__.py
import json
import requests
from youtube_search_requests.utils.errors import InvalidURL

def parse_json_session_data(r: requests.Request):
    d = r.text[r.text.find('ytcfg.set({') + 10:]
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

    def _wrap_dict_related_videos(self, data: str):
        startpos = data.find('var ytInitialData = ')
        text2 = data[startpos+20:]
        endpos = text2.find('"}};</script>') + 3
        return json.loads(text2[:endpos])

    def _request_search(self, url: str):
        r = requests.get(url)
        return r.text

    def _get_related_videos(self, data: dict):
        vids = data['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results']
        videos = []
        for info in vids:
            try:
                v = info['compactVideoRenderer']
                videos.append({
                    'title': v['title']['runs'][0]['text'],
                    'url': 'https://www.youtube.com/watch?v=%s' % (v['videoId']),
                    'thumbnails': v['thumbnail']['thumbnails'],
                    'uploader': v['longBylineText']['runs'][0]['text'],
                    'publishedSince': v['publishedTimeText']['runs'][0]['text'],
                    'views': v['viewCountText']['runs'][0]['text'],
                    'durations': v['lengthText']['runs'][0]['text']
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
    def __init__(self, dict_data: dict, include_related_videos=False):
        self.data = dict_data
        self.include_related_videos = include_related_videos

    def _get_primary_videos_data(self, data):
        try:
            return data['contents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
        except KeyError:
            return None
        except IndexError:
            return None

    def _get_primary_videos_data_post(self, data):
        try:
            return data['onResponseReceivedCommands'][0]['appendContinuationItemsAction']['continuationItems'][0]['itemSectionRenderer']['contents']
        except KeyError:
            return None
        except IndexError:
            return None

    def _get_secondary_videos_data(self, data):
        try:
            return data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents']
        except KeyError:
            return None
        except IndexError:
            return None

    def _get_third_videos_data(self, data):
        try:
            return data['contents']['sectionListRenderer']['contents'][1]['itemSectionRenderer']['contents']
        except KeyError:
            return None
        except IndexError:
            return None

    def _get_videos(self):
        p1 = self._get_primary_videos_data(self.data)
        if p1 is not None:
            return p1
        p2 = self._get_primary_videos_data_post(self.data)
        if p2 is not None:
            return p2
        s1 = self._get_secondary_videos_data(self.data)
        if s1 is not None:
            return s1
        t1 = self._get_third_videos_data(self.data)
        if t1 is not None:
            return t1
        return None

    def get_related_videos(self, url: str):
        if self.include_related_videos:
            s = SearchRelatedVideos(url)
            return s.get_related_videos()
        else:
            return None

    def get_videos(self):
        videos = []
        data = self._get_videos()
        if data is None:
            return None
        for info in data:
            try:
                v = info['compactVideoRenderer']
                videos.append({
                    'title': v['title']['runs'][0]['text'],
                    'url': 'https://www.youtube.com/watch?v=%s' % (v['videoId']),
                    'thumbnails': v['thumbnail']['thumbnails'],
                    'uploader': v['longBylineText']['runs'][0]['text'],
                    'publishedSince': v['publishedTimeText']['runs'][0]['text'],
                    'views': v['viewCountText']['runs'][0]['text'],
                    'durations': v['lengthText']['runs'][0]['text'],
                    'related_videos': self.get_related_videos('https://www.youtube.com/watch?v=%s' % (v['videoId']))
                })
            except KeyError:
                continue
        return videos


class GetContinuationToken:
    def __init__(self, dict_data: dict):
        self.data = dict_data

    def _get_primary_continuation_token(self, data):
        try:
            return data['contents']['sectionListRenderer']['contents'][1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
        except KeyError:
            return None
        except IndexError:
            return None

    def _get_secondary_continuation_token(self, data):
        try:
            return data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
        except KeyError:
            return None
        except IndexError:
            return None

    def _get_primary_continuation_token_post(self, data):
        try:
            return data['onResponseReceivedCommands'][0]['appendContinuationItemsAction']['continuationItems'][1]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
        except KeyError:
            return None
        except IndexError:
            return None

    def _get_third_continuation_token(self, data):
        try:
            return data['contents']['sectionListRenderer']['contents'][2]['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
        except KeyError:
            return None
        except IndexError:
            return None


    def get_token(self):
        p1 = self._get_primary_continuation_token(self.data)
        if p1 is not None:
            return p1
        p2 = self._get_primary_continuation_token_post(self.data)
        if p2 is not None:
            return p2
        s1 = self._get_secondary_continuation_token(self.data)
        if s1 is not None:
            return s1
        t1 = self._get_third_continuation_token(self.data)
        if t1 is not None:
            return t1
        return None
