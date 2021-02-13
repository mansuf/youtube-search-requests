# youtube-search-requests
# parser/continuation_token.py

# for bot or unknown user-agent maybe ?
def parse_continuation_token1(data):
    try:
        init = data['onResponseReceivedCommands']
    except KeyError:
        return None
    d = None
    for a in init:
        try:
            d = a['appendContinuationItemsAction']['continuationItems']
        except KeyError:
            continue
    if d is None:
        return None
    for i in d:
        try:
            return i['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
        except KeyError:
            continue
    return None

# for mobile web browser
def parse_continuation_token2(data):
    try:
        d = data['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents']
    except KeyError:
        return None
    for i in d:
        try:
            return i['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
        except KeyError:
            continue
    return None

# for desktop web browser
def parse_continuation_token3(data):
    try:
        d = data['contents']['sectionListRenderer']['contents']
    except KeyError:
        return None
    for i in d:
        try:
            return i['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
        except KeyError:
            continue
    return None

# for grabbing in watch youtube page
def parse_continuation_token4(data):
    try:
        d = data['contents']['singleColumnWatchNextResults']['results']['results']['continuations']
    except KeyError:
        return None
    for i in d:
        try:
            return i['reloadContinuationData']['continuation']
        except KeyError:
            return None

# for grabbing in watch youtube page
def parse_continuation_token5(data):
    try:
        d = data['onResponseReceivedEndpoints']
    except KeyError:
        return None
    a = None
    for i in d:
        try:
            a = i['appendContinuationItemsAction']['continuationItems']
        except KeyError:
            continue
    if a is None:
        return None
    else:
        for c in a:
            try:
                return c['continuationItemRenderer']['continuationEndpoint']['continuationCommand']['token']
            except KeyError:
                continue
        return None

# for grabbing in watch youtube page
def parse_continuation_token6(data):
    try:
        d = data['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults']['results']
    except KeyError:
        return None
    for key in d:
        try:
            init = key['continuationItemRenderer']
        except KeyError:
            continue
        try:
            return init['continuationEndpoint']['continuationCommand']['token']
        except KeyError:
            continue

# for grabbing in watch youtube page
def parse_continuation_token7(data):
    try:
        d = data['contents']['twoColumnWatchNextResults']['results']['results']['contents']
    except KeyError:
        return None
    for key in d:
        try:
            init = key['itemSectionRenderer']
            if init['sectionIdentifier'] == 'comment-item-section':
                continue
        except KeyError:
            continue
        try:
            _key = init['continuations']
        except KeyError:
            continue
        for token in _key:
            try:
                return token['nextContinuationData']['continuation']
            except KeyError:
                continue