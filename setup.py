from distutils.core import setup
setup(
  name = 'youtube-search-requests',         
  packages = ['youtube-search-requests'],   
  version = '0.0.1',   
  license='MIT',     
  description = 'Search Youtube videos using python requests',
  author = 'Rahman Yusuf',              
  author_email = 'danipart4@gmail.com',
  url = 'https://github.com/trollfist20/youtube-search-requests',  
  download_url = 'https://github.com/trollfist20/youtube-search-requests/archive/v0.0.1.tar.gz',
  keywords = ['youtube', 'youtube-search'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
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