[![pypi](https://img.shields.io/pypi/v/youtube-search-requests?style=plastic&logo=appveyor)](https://pypi.org/project/youtube-search-requests)
[![python-ver](https://img.shields.io/pypi/pyversions/youtube-search-requests?style=plastic&logo=appveyor)](https://pypi.org/project/youtube-search-requests)
[![github-release](https://img.shields.io/github/v/release/trollfist20/youtube-search-requests?style=plastic&logo=appveyor)](https://github.com/trollfist20/youtube-search-requests/releases)
[![pypi-total-downloads](https://img.shields.io/pypi/dm/youtube-search-requests?label=DOWNLOADS&style=plastic&logo=appveyor)](https://pypi.org/project/youtube-search-requests)


# youtube-search-requests
### Search Youtube videos using python requests without Youtube API.
### youtube-search-requests can search unlimited videos !!!

**NOTE:** youtube-search-requests is still in development. But, it should be stable for now.

## Installation
```
pip install youtube-search-requests
```

CLI (Command Line Interface) Usage:
```bash

ysr "fish" --json

# or

youtube-search-requests "fish" --json

# do this if "ysr" and "youtube_search_requests" didn't work
python3 -m youtube_search_requests "fish" --json

# Output: {"urls": {'title': ..., 'url': 'https://www.youtube.com/watch?v=0gT8Ty0ClHc', thumbnails: [...], ...}}

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
- First, youtube-search-requests create a session for Youtube. (every opened youtube page in browser have it own session)
- Second, youtube-search-requests search videos using "Public Search Youtube API" that have been used youtube for searching videos in browsers.
- There we go, done !!! :D.

