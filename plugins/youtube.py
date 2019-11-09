import random
import re
import time
import urllib

from util import hook, http, timeformat

#youtube_re = (r'(?:youtube.*?(?:v=|/v/)|youtu\.be/|yooouuutuuube.*?id=)'
#              '([-_a-zA-Z0-9]+)', re.I)
youtube_re = (r'(?:youtube.*?(?:v=|/v/)|youtu\.be/)([-_a-zA-Z0-9]+)?(.*)',
              re.I)

base_url = 'https://www.googleapis.com/youtube/v3/'
search_api_url = base_url + 'search?part=id,snippet'
api_url = base_url + 'videos?part=snippet,statistics,contentDetails'
video_url = "http://youtu.be/%s"


def plural(num=0, text=''):
    return "{:,} {}{}".format(num, text, "s" [num == 1:])


def get_video_description(key, video_id):
    request = http.get_json(api_url, key=key, id=video_id)

    if request.get('error'):
        return

    data = request['items'][0]

    title = filter(None, data['snippet']['title'].split(' '))
    title = ' '.join(map(lambda s: s.strip(), title))
    out = u'\x02{}\x02'.format(title)

    try:
        data['contentDetails'].get('duration')
    except KeyError:
        return out

    length = data['contentDetails']['duration']
    timelist = re.findall('(\d+[DHMS])', length)

    seconds = 0
    for t in timelist:
        t_field = int(t[:-1])
        if t[-1:] == 'D': seconds += 86400 * t_field
        elif t[-1:] == 'H': seconds += 3600 * t_field
        elif t[-1:] == 'M': seconds += 60 * t_field
        elif t[-1:] == 'S': seconds += t_field

    out += u' - length \x02{}\x02'.format(
        timeformat.format_time(seconds, simple=True))

    try:
        data['statistics']
    except KeyError:
        return out

    stats = data['statistics']
    try:
        likes = u"\u2191{:,}".format(int(stats['likeCount']))
        dislikes = u"\u2193{:,}".format(int(stats['dislikeCount']))
        try:
            percent = 100 * float(stats['likeCount']) / (
                int(stats['likeCount']) + int(stats['dislikeCount']))
        except ZeroDivisionError:
            percent = 0
    except KeyError:
        likes = '\x0304likes disabled\x03'
        dislikes = '\x0304dislikes disabled\x03'
        percent = 0
    if percent >= 50:
        out += u' - \x0309{}\x03, \x0304{}\x03 (\x02\x0309{:.1f}\x03\x02%)'.format(
            likes, dislikes, percent)
    else:
        out += u' - \x0309{}\x03, \x0304{}\x03 (\x0304\x02{:.1f}\x02%\x03)'.format(
            likes, dislikes, percent)

    views = int(stats['viewCount'])
    out += u' - \x02{:,}\x02 {}{}'.format(views, 'view', "s" [views == 1:])

    uploader = data['snippet']['channelTitle']

    upload_time = time.strptime(data['snippet']['publishedAt'],
                                "%Y-%m-%dT%H:%M:%S.000Z")
    out += u' - \x02{}\x02 on \x02{}\x02'.format(
        uploader, time.strftime("%Y.%m.%d", upload_time))

    try:
        data['contentDetails']['contentRating']
    except KeyError:
        return out

    out += u' - \x034NSFW\x02'

    return out


@hook.command('ytr', autohelp=False)
def randomtube(inp, bot=None):
    """randomtube -- Returns random youtube link from old logs."""
    key = bot.config.get("api_keys", {}).get("google")
    with open('plugins/data/youtube.txt', 'r') as f:
        urllist = f.read().split('\n')
        length = len(urllist)
        url = urllist[random.randint(0, length - 1)]
        try:
            description = get_video_description(key, url.split('=')[1])
            f.close()
            return url + ' - ' + description
        except Exception as e:
            print url
            description = get_video_description(key, url.split('/')[-1])
            f.close()
            return url + ' - ' + description


@hook.regex(*youtube_re)
def youtube_url(match, bot=None, chan=None):
    key = bot.config.get("api_keys", {}).get("google")

    return get_video_description(key, match.group(1))


@hook.command('yt')
@hook.command('hooktube')
@hook.command('ht')
@hook.command
def youtube(inp, bot=None, input=None):
    """youtube <query> -- Returns the first YouTube search result for <query>."""
    key = bot.config.get("api_keys", {}).get("google")

    request = http.get_json(search_api_url, key=key, type='video', q=inp)

    if 'error' in request:
        return 'Error performing search.'

    if request['pageInfo']['totalResults'] == 0:
        return 'No results found.'

    video_id = request['items'][0]['id']['videoId']
    if input['trigger'] == u'hooktube' or input['trigger'] == u'ht':
        print "penis"
        return get_video_description(
            key, video_id) + u" - " + video_url.replace(
                'youtu.be', 'hooktube.com') % video_id
    else:
        return get_video_description(key,
                                     video_id) + u" - " + video_url % video_id


@hook.command('ytime')
@hook.command
def youtime(inp, bot=None):
    """youtime <query> -- Gets the total run time of the first YouTube search result for <query>."""
    key = bot.config.get("api_keys", {}).get("google")
    request = http.get_json(search_api_url, key=key, q=inp, type='video')

    if 'error' in request:
        return 'Error performing search.'

    if request['pageInfo']['totalResults'] == 0:
        return 'No results found.'

    video_id = request['items'][0]['id']['videoId']

    request = http.get_json(api_url, key=key, id=video_id)

    data = request['items'][0]

    length = data['contentDetails']['duration']
    timelist = re.findall('(\d+[DHMS])', length)

    seconds = 0
    for t in timelist:
        t_field = int(t[:-1])
        if t[-1:] == 'D': seconds += 86400 * t_field
        elif t[-1:] == 'H': seconds += 3600 * t_field
        elif t[-1:] == 'M': seconds += 60 * t_field
        elif t[-1:] == 'S': seconds += t_field

    views = int(data['statistics']['viewCount'])
    total = int(seconds * views)

    length_text = timeformat.format_time(seconds, simple=True)
    total_text = timeformat.format_time(total, accuracy=8)

    return u'The video \x02{}\x02 has a length of {} and has been viewed {:,} times for ' \
            'a total run time of {}!'.format(data['snippet']['title'], length_text, views, total_text)


ytpl_re = (
    r'(.*:)//(www.youtube.com/playlist|youtube.com/playlist)(:[0-9]+)?(.*)',
    re.I)


@hook.regex(*ytpl_re)
def youtubeplaylist_url(match):
    location = match.group(4).split("=")[-1]

    try:
        soup = http.get_soup(
            "https://www.youtube.com/playlist?list=" + location)
    except Exception:
        return "\x034\x02Invalid response."

    title = soup.find('title').text.split('-')[0].strip()
    author = soup.find('img',
                       {'class': 'channel-header-profile-image'})['title']
    numvideos = soup.find('ul', {
        'class': 'pl-header-details'
    }).findAll('li')[1].string
    numvideos = re.sub("\D", "", numvideos)
    views = soup.find('ul', {
        'class': 'pl-header-details'
    }).findAll('li')[2].string
    views = re.sub("\D", "", views)

    return u"\x02{}\x02 - \x02{}\x02 views - \x02{}\x02 videos - \x02{}\x02".format(
        title, views, numvideos, author)
