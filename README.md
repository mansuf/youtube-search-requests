# youtube-search-requests
### Search Youtube videos using python requests without Youtube API.
~~youtube-search-requests can search up to 120+ videos !~~
### youtube-search-requests v0.0.2 can search unlimited videos !!!


~~Normally youtube-search-requests only extract urls, you can extract additional information by installing youtube-dl, for more information check usage below.~~.

in v0.0.2, features like "validate", "extract_info", "include_related_videos" is gone,
but dont worry "include_related_videos" will be back in future updates.

also, you don't need youtube-dl module anymore, 
youtube-search-requests now extract info by itself.
And provide a very fast search rather than old version (v0.0.1)

CLI (Command Line Interface) Usage:
```python

usage: python3 -m youtube_search_requests [-h] [-v] [--max-results={Number}] [-t={Number}] [-ei]
                                          [--json]
 			                   Search terms

Search Youtube videos using python requests without Youtube API

positional arguments:
  Search terms          a string terms want to search (if include space, you
                        must use double quotes "")

optional arguments:
  -h, --help            show this help message and exit
  --max-results={Number} 
                        maximum search results
  -t={Number} , --timeout={Number} 
                        give number of times to execute search, if times runs
                        out, search stopped & returning results
  --json                Return results in json format

example usage:

python3 -m youtube_search_requests "fish" --json

# {"urls": {'title': ..., 'url': 'https://www.youtube.com/watch?v=0gT8Ty0ClHc', thumbnails: [...], ...}}


```

Simple usage:

```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch('fish', max_results=10)
videos = y.search()

print(videos)
```

Search with given time usage:
```python

from youtube_search_requests import YoutubeSearch

# given time 60 seconds for searching videos
y = YoutubeSearch('fish', max_results=10, timeout=60) 

# if search not complete after 60 seconds
# force it to return results
videos = y.search()

print(videos)
```

## You might be wonder, how youtube-search-requests work ?

### in-short-word:
youtube-search-requests work like Youtube in browsers (playing with POST and GET method).

### in-long-word:
- First, youtube-search-requests create a session for Youtube. (every opened youtube page in browser have it own session id)
- Second, youtube-search-requests search videos using "internal Youtube API" that have been used youtube for searching videos in browsers.
- There we go, done !!! :D.
