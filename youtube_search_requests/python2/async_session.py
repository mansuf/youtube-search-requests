# youtube-search-requests
# python2/async_session.py

from youtube_search_requests.utils.errors import UnsupportedPython

class AsyncYoutubeSession:
    """
    **Same as YoutubeSession, but with async method**
    
    Normally, YoutubeSession class will automatically call new_session() when you call __init__().
    But, AsyncYoutubeSession doesn't do that, you have to call new_session()
    in order to get a new session from Youtube.

    AsyncYoutubeSession arguments

    preferred_user_agent: :class:`str` (optional, default: 'BOT')
        a User-Agent header to pass in session, 
        see constants.py to see all supported user-agents
    loop: :class:`asyncio.AbstractEventLoop` (optional, default: None)
        a event loop to pass in session

    """
    def __init__(self, preferred_user_agent='BOT', loop=None):
        raise UnsupportedPython('python 2 is not support to use async method. Please Upgrade your python.')