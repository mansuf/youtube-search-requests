# youtube-search-requests 
# utils.__init__.py
import json
import requests

def parse_json_session_data(r: requests.Request):
    d = r.text[r.text.find('ytcfg.set({') + 10:]
    return json.loads(d[0:d.find(');')])

class GetVideosData:
    def __init__(self, dict_data: dict):
        self.data = dict_data

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

    def _get_videos(self):
        p1 = self._get_primary_videos_data(self.data)
        if p1 is not None:
            return p1
        p2 = self._get_primary_videos_data_post(self.data)
        if p2 is not None:
            return p2
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
                    'durations': v['lengthText']['runs'][0]['text']
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
        return None
