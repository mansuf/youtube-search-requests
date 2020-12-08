# youtube-search-requests
### Search Youtube videos using python requests without Youtube API.
### youtube-search-requests can search up to 120+ videos !

Normally youtube-search-requests only extract urls, you can extract additional information by installing youtube-dl, for more information check usage below.


Simple usage:

```python

from youtube_search_requests import YoutubeSearch

y = YoutubeSearch('fish', max_results=10)
videos = y.search()

print(videos)
```

### also, youtube-search-requests have ability to validate videos
this to prevent UNPLAYABLE or ERROR videos

Search and validating videos usage:
```python

from youtube_search_requests import YoutubeSearch

# by default, validate is set to True
y = YoutubeSearch('delicious fish', max_results=10, validate=True)
videos = y.search()

print(videos)
```

Extracting additional info videos usage:
```python

from youtube_search_requests import YoutubeSearch

# NOTE: this require youtube-dl module
y = YoutubeSearch('fish', max_results=10, validate=True, extract_info=True)
videos = y.search

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