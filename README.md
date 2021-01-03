# youtube-search-requests
### Search Youtube videos using python requests without Youtube API.
### youtube-search-requests can search unlimited videos !!!

CLI (Command Line Interface) Usage:
```

usage: python3 -m youtube_search_requests [-h] [--max-results={Number}] [-t={Number}] [-v] [--json]
                                          [--json-output={Filename}] [--include-related-videos]
                                          [--safe-search]
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
  -v , --version        show youtube-search-requests version
  --json                Return results in json format
  --json-output={Filename} 
                        Return results in output file based on json format
  --include-related-videos 
                        include all related videos each url's
  --safe-search         This helps hide potentially mature videos.
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

Search with related videos usage:
```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch('fish', max_results=10, include_related_videos=True) 
videos = y.search()

print(videos)

```

### youtube-search-requests support safe search !!!
### this helps to prevent mature videos in search results.

search with safe search usage:
```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch('fish', max_results=10, safe_search=True) 
videos = y.search()

print(videos)

```

### youtube-search-requests also support asynchronous method ! (using aiohttp module)

search with async usage:
```python

import asyncio
from youtube_search_requests import AsyncYoutubeSearch

async def search():
  y = AsyncYoutubeSearch('fish', max_results=10)
  results = await y.search()
  print(results)

asyncio.run(search())
```

## You might be wonder, how youtube-search-requests work ?

### in-short-word:
youtube-search-requests work like Youtube in browsers (playing with POST and GET method).

### in-long-word:
- First, youtube-search-requests create a session for Youtube. (every opened youtube page in browser have it own session id)
- Second, youtube-search-requests search videos using "internal Youtube API" that have been used youtube for searching videos in browsers.
- There we go, done !!! :D.
