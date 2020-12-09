import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
  name = 'youtube-search-requests',         
  packages = ['youtube_search_requests'],   
  version = '0.0.15',
  license='MIT',     
  description = 'Search Youtube videos using python requests without Youtube API',
  long_description= README,
  long_description_content_type= 'text/markdown',
  author = 'Rahman Yusuf',              
  author_email = 'danipart4@gmail.com',
  url = 'https://github.com/trollfist20/youtube-search-requests',  
  download_url = 'https://github.com/trollfist20/youtube-search-requests/archive/v0.0.15.tar.gz',
  keywords = ['youtube', 'youtube-search'], 
  install_requires=[           
          'requests',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',  
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)
