### Simple usage:

```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch('fish', max_results=10)
videos = y.search()

print(videos)
```

### Search with given time usage:
```python

from youtube_search_requests import YoutubeSearch

# given time 60 seconds for searching videos
y = YoutubeSearch('fish', max_results=10, timeout=60) 

# if search not complete after 60 seconds
# force it to return results
videos = y.search()

print(videos)
```

### Search with related videos usage:
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