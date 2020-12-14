# youtube-search-requests 
# __main__.py
import sys
from argparse import ArgumentParser
from youtube_search_requests.utils.errors import InvalidArgument
from youtube_search_requests import YoutubeSearch
from youtube_search_requests import __VERSION__

def help_arguments():
    a = ArgumentParser(description='Search Youtube videos using python requests without Youtube API')
    a.add_argument('Search terms', metavar='Search terms', help='a string terms want to search (if include space, you must use double quotes "")')
    a.add_argument('--max-results={Number}', help='maximum search results', metavar='')
    a.add_argument('-t={Number}', '--timeout={Number}', help='give number of times to execute search, if times runs out, search stopped & returning results', metavar='')
    a.add_argument('-v', '--version', help='show youtube-search-requests version', metavar='')
    a.add_argument('--json', help='Return results in json format', metavar='')
    print(a.print_help())

def main(argv):
    max_results = 10
    timeout = None
    search_terms = ''
    json_format = False
    for i in argv:
        if i.startswith('--max-results='):
            try:
                max_results = int(i.replace('--max-results=', ''))
            except ValueError:
                raise InvalidArgument('invalid number for --max-results')
        elif i.startswith('--timeout=') or i.startswith('-t='):
            try:
                timeout = int(i.replace('--timeout=', '').replace('-t=', ''))
            except ValueError:
                raise InvalidArgument('invalid number for --timeout / -t')
        elif i == '--json':
            json_format = True
        elif i == '--version' or i == '-v':
            return print(__VERSION__)
        else:
            search_terms = i
    if search_terms == '':
        raise InvalidArgument('search_terms is empty')
    yt_search = YoutubeSearch(search_terms, max_results, timeout, json_format)
    print(yt_search.search())
        


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Exception as e:
        print('ERROR: %s' % (e))
        help_arguments()