# youtube-search-requests
# parser/related_video_data.py

# for mobile user-agent
def parse_related_video_data1(data):
    try:
        d = data['contents']['singleColumnWatchNextResults']['results']['results']['contents']
    except KeyError:
        return None
    for i in d:
        try:
            c = i['itemSectionRenderer']['contents']
        except KeyError:
            continue
        except TypeError:
            continue
        print(type(c))
        for v in c:
            try:
                v['compactVideoRenderer']
                return c
            except KeyError:
                continue

# for desktop user-agent
def parse_related_video_data2(data):
    try:
        return data['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results']
    except KeyError:
        return None

# for bot or unknown user-agent maybe ?
def parse_related_video_data3(data):
    try:
        d = data['contents']['singleColumnWatchNextResults']['results']['results']['contents']
    except KeyError:
        return None
    for i in d:
        try:
            c = i['itemSectionRenderer']['contents']
        except KeyError:
            continue
        except TypeError:
            continue
        for v in c:
            try:
                v['videoWithContextRenderer']
                return c
            except KeyError:
                continue

# for internal API 
def parse_related_video_data4(data):
    try:
        d = data['onResponseReceivedEndpoints']
    except KeyError:
        return None
    else:
        for key in d:
            try:
                return key['appendContinuationItemsAction']['continuationItems']
            except KeyError:
                continue

        