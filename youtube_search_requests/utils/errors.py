# youtube-search-requests 
# errors.py

# base exception
class YoutubeSearchBaseException(BaseException):
    pass

# raised when one of each argument is invalid
class InvalidArgument(YoutubeSearchBaseException):
    pass

# raised when url is invalid
class InvalidURL(YoutubeSearchBaseException):
    pass

# raised when specified python is no longer supported
class UnsupportedPython(YoutubeSearchBaseException):
    pass