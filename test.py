import sys
import requests
from youtube_dl import YoutubeDL
import threading
import time

from youtube_search import YoutubeSearch as YS
from youtube_search_requests import YoutubeSearch

def prevent_same_urls(urls):
    legit_urls = []
    for i in urls:
        if i in legit_urls:
            continue
        else:
            legit_urls.append(i)
    return legit_urls

validate = YoutubeDL()

# y = YoutubeSearch('gordon ramsay', 10)
# r = requests.get(y.BASE_URL + y.search_query)
# print(y._parse_urls(r))

def test1():
    time1 = time.monotonic()
    yi = YS('kizuna ai', 100)
    list_videos2 = yi.search()
    time2 = time.monotonic()
    print('module youtube_search finished with time: %s' % (time2 - time1))

def test2():
    time1 = time.monotonic()
    y = YoutubeSearch('美淫感猥菊花 塞入擴張覺醒穴', 10, False)
    list_videos = y.search()
    time2 = time.monotonic()
    print(list_videos)
    print('module youtube_search_requests finished with time: %s' % (time2 - time1))

t1 = threading.Thread(target=test1, name='test1', daemon=True)
t2 = threading.Thread(target=test2, name='test1', daemon=True)

t1.start()
t2.start()
time.sleep(99999)

# print(validate.extract_info('https://www.youtube.com/watch?v=NJGPF7t368E', download=False))