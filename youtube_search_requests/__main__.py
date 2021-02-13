# youtube-search-requests 
# __main__.py
import sys
import json
import asyncio
from argparse import ArgumentParser, SUPPRESS
from youtube_search_requests.utils.errors import InvalidArgument
from youtube_search_requests import YoutubeSearch, AsyncYoutubeSearch, AsyncYoutubeSession
from youtube_search_requests.constants import ALL_VIDEOS_FILTERS
from youtube_search_requests import __VERSION__

async def async_search(args):
    session = AsyncYoutubeSession(
        language=args.language or 'en',
        restricted_mode=args.safe_search,
    )
    await session.new_session()
    ay = AsyncYoutubeSearch(
        session,
        args.json
    )
    if args.search_type == 'videos':
        data = await ay.search_videos(
            args.SEARCH_TERMS_OR_YOUTUBE_URL,
            args.max_results or 10,
            args.timeout,
            args.include_related_videos,
            args.max_results_related_videos or 10,
            args.use_short_link,
            args.vid_filter or 'NO_FILTER'
        )
        if args.json_output is not None:
            if args.json:
                write_data(args.json_output, data)
            else:
                write_data(
                    args.json_output,
                    json.dumps({'urls': data})
                )
        else:
            print(data)
    elif args.search_type == 'playlists':
        data = await ay.search_playlists(
            args.SEARCH_TERMS_OR_YOUTUBE_URL,
            args.max_results or 10,
            args.timeout,
            args.use_short_link
        )
        if args.json_output is not None:
            if args.json:
                write_data(args.json_output, data)
            else:
                write_data(
                    args.json_output,
                    json.dumps({'urls': data})
                )
        else:
            print(data)
    elif args.search_type == 'related-videos':
        data = await ay.search_related_videos(
            args.SEARCH_TERMS_OR_YOUTUBE_URL,
            args.max_results or 10,
            args.timeout,
            args.use_short_link
        )
        if args.json_output is not None:
            if args.json:
                write_data(args.json_output, data)
            else:
                write_data(
                    args.json_output,
                    json.dumps({'urls': data})
                )
        else:
            print(data)
    await session.close()

def search(args):
    y = YoutubeSearch(
        args.json,
        None,
        args.safe_search,
        args.language or 'en'
    )
    if args.search_type == 'videos':
        data = y.search_videos(
            args.SEARCH_TERMS_OR_YOUTUBE_URL,
            args.max_results or 10,
            args.timeout,
            args.include_related_videos,
            args.max_results_related_videos or 10,
            args.use_short_link,
            args.vid_filter or 'NO_FILTER'
        )
        if args.json_output is not None:
            if args.json:
                write_data(args.json_output, data)
            else:
                write_data(
                    args.json_output,
                    json.dumps({'urls': data})
                )
        else:
            return data
    elif args.search_type == 'playlists':
        data = y.search_playlists(
            args.SEARCH_TERMS_OR_YOUTUBE_URL,
            args.max_results or 10,
            args.timeout,
            args.use_short_link
        )
        if args.json_output is not None:
            if args.json:
                write_data(args.json_output, data)
            else:
                write_data(
                    args.json_output,
                    json.dumps({'urls': data})
                )
        else:
            return data
    elif args.search_type == 'related-videos':
        data = y.search_related_videos(
            args.SEARCH_TERMS_OR_YOUTUBE_URL,
            args.max_results or 10,
            args.timeout,
            args.use_short_link
        )
        if args.json_output is not None:
            if args.json:
                write_data(args.json_output, data)
            else:
                write_data(
                    args.json_output,
                    json.dumps({'urls': data})
                )
        else:
            return data

def write_data(filename, data):
    w = open(filename, 'w')
    w.write(data)
    w.close()

def main():
    a = ArgumentParser(description='Search Youtube videos using python requests without Youtube API')
    important = a.add_argument_group('REQUIRED arguments')
    important.add_argument('--search-type', help='Type of search, ex: videos, playlists, related_videos', metavar='TYPES', choices=[
        'videos',
        'playlists',
        'related-videos'
    ], required=True)
    important.add_argument('SEARCH_TERMS_OR_YOUTUBE_URL', help='a string terms want to search (if include space, you must use double quotes "")')
    vid = a.add_argument_group('Search videos optional arguments')
    vid.add_argument('--include-related-videos', help='include all related videos each url\'s', action='store_true')
    vid.add_argument('--max-results-related-videos', type=int, help='set maximum related videos each videos', metavar='NUMBER')
    vid.add_argument('--vid-filter', help='apply filter to search videos', metavar='TYPE_FILTER_VIDEOS', choices=ALL_VIDEOS_FILTERS.keys())
    a.add_argument('--safe-search', help='Enable restricted mode, This helps hide potentially mature videos.', action='store_true')
    a.add_argument('-lang', '--language', help='Set language results', metavar='LANGUAGE')
    a.add_argument('--use-short-link', help='Use shorted link', action='store_true')
    a.add_argument('--max-results', type=int, help='set maximum search results', metavar='NUMBER')
    a.add_argument('-t', '--timeout', type=int, help='give number of times to execute search, if times runs out, search stopped & returning results', metavar='NUMBER')
    a.add_argument('--json', help='Return results in json format', action='store_true')
    a.add_argument('--json-output', help='Return results in output file based on json format', metavar='FILENAME')
    a.add_argument('-v', '--version', help='show version', action='version', version=__VERSION__)
    a.add_argument('--async', help='use async process instead of sync process', action='store_true')
    args = a.parse_args()
    if getattr(args, 'async'):
        asyncio.run(async_search(args))
    else:
        print(search(args))


if __name__ == "__main__":
    main()