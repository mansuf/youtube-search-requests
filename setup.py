import pathlib
from setuptools import setup
import sys

__VERSION__ = 'v0.1.11'

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
  name = 'youtube-search-requests',         
  packages = [
    'youtube_search_requests',
    'youtube_search_requests/utils',
    'youtube_search_requests/extractor',
    'youtube_search_requests/parser'
  ],   
  version = __VERSION__,
  license='MIT',     
  description = 'Search Youtube videos using python requests without Youtube API',
  long_description= README,
  long_description_content_type= 'text/markdown',
  author = 'Rahman Yusuf',              
  author_email = 'danipart4@gmail.com',
  entry_points= {
    'console_scripts': [
      'youtube-search-requests=youtube_search_requests.__main__:main',
      'ysr=youtube_search_requests.__main__:main'
    ]
  },
  url = 'https://github.com/trollfist20/youtube-search-requests',  
  download_url = 'https://github.com/trollfist20/youtube-search-requests/archive/%s.tar.gz' % (__VERSION__),
  keywords = ['youtube', 'youtube-search'], 
  install_requires=[           
          'requests',
          'aiohttp'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',  
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
