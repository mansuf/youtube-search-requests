# youtube-search-requests 
# errors.py

# base exception
class YoutubeException(BaseException):
    """Base Youtube exception"""
    pass

# raised when url is invalid
class InvalidURL(YoutubeException):
    pass