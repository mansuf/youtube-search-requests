from distutils.core import setup
setup(
  name = 'youtube-search-requests',         
  packages = ['youtube_search_requests'],   
  version = '0.0.1',
  license='MIT',     
  description = 'Search Youtube videos using python requests',
  long_description= 'This project still need documentation !!!',
  author = 'Rahman Yusuf',              
  author_email = 'danipart4@gmail.com',
  url = 'https://github.com/trollfist20/youtube-search-requests',  
  download_url = 'https://github.com/trollfist20/youtube-search-requests/archive/v0.0.1.tar.gz',
  keywords = ['youtube', 'youtube-search'], 
  install_requires=[           
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',  
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ],
)