# youtube-search-requests 
# __main__.py
import sys
import json
from argparse import ArgumentParser
from youtube_search_requests.utils.errors import InvalidArgument
from youtube_search_requests import YoutubeSearch
from youtube_search_requests import __VERSION__

def write_data(filename, data):
    w = open(filename, 'w')
    w.write(data)
    w.close()

def main():
    a = ArgumentParser(description='Search Youtube videos using python requests without Youtube API')
    a.add_argument('SEARCH_TERMS', help='a string terms want to search (if include space, you must use double quotes "")')
    a.add_argument('--max-results', type=int, help='maximum search results', metavar='NUMBER')
    a.add_argument('-t', '--timeout', type=int, help='give number of times to execute search, if times runs out, search stopped & returning results', metavar='NUMBER')
    a.add_argument('-v', '--version', help='show youtube-search-requests version', action='store_true')
    a.add_argument('--json', help='Return results in json format', action='store_true')
    a.add_argument('--json-output', help='Return results in output file based on json format', metavar='FILENAME')
    a.add_argument('--include-related-videos', help='include all related videos each url\'s', action='store_true')
    a.add_argument('--safe-search', help='This helps hide potentially mature videos.', action='store_true')
    args = a.parse_args()
    y = YoutubeSearch(
        args.SEARCH_TERMS,
        args.max_results or 10,
        args.timeout,
        args.json,
        args.include_related_videos,
        None,
        args.safe_search
    )
    data = y.search()
    if args.json_output is not None:
        if isinstance(data, str):
            write_data(args.json_output, data)
        else:
            write_data(args.json_output, json.dumps({'urls': data}))
    else:
        print(data)


if __name__ == "__main__":
    main()