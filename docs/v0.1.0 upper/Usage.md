### Search videos

```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch()
videos = y.search_videos('fish', max_results=10)

print(videos)
```

### Search playlists

```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch()
playlists = y.search_playlists('fish', max_results=10)

print(playlists)
```

### Search related videos

```python
from youtube_search_requests import YoutubeSearch

y = YoutubeSearch()
related_videos = y.search_related_videos('https://www.youtube.com/watch?v=cC9r0jHF-Fw', max_results=10)

print(related_videos)
```

### Search with given time usage
```python

from youtube_search_requests import YoutubeSearch

# given time 60 seconds for searching videos
y = YoutubeSearch() 

# if search not complete after 60 seconds
# force it to return results
videos = y.search_videos('fish', max_results=10, timeout=60)

print(videos)
```

### Search with related videos usage
```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch() 
videos = y.search_videos('fish', max_results=10, include_related_videos=True)

print(videos)

```

### Search results json output

```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch(json_results=True)
videos = y.search_videos('fish', max_results=10)


print(videos)
```

### Search with different language

```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch(language='id')
videos = y.search_videos('fish', max_results=10)

print(videos)
```

### Search videos with filter

```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch()

# See youtube_search_requests/constants.py in ALL_VIDEOS_FILTERS
# to see all video filters
videos = y.search_videos('fish', filter_type='LEN>20MIN')

print(videos)
```


### youtube-search-requests support safe search !!!
### this helps to prevent mature videos in search results.

search with safe search usage
```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch(safe_search=True) 
videos = y.search_videos('fish', max_results=10)

print(videos)

```

### youtube-search-requests also support asynchronous method ! (using aiohttp module)

search with async usage
```python

import asyncio
from youtube_search_requests import AsyncYoutubeSearch

async def search():
  y = AsyncYoutubeSearch()
  results = await y.search_videos('fish', max_results=10)
  print(results)

asyncio.run(search())
```