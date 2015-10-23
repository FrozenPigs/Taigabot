import re
import time

from util import hook, http, timeformat

youtube_re = (r'(?:youtube.*?(?:v=|/v/)|youtu\.be/|yooouuutuuube.*?id=)'
              '([-_a-zA-Z0-9]+)', re.I)

base_url = 'https://www.googleapis.com/youtube/v3/'
search_api_url = base_url + 'search?part=id,snippet'
api_url = base_url + 'videos?part=snippet,statistics,contentDetails'
video_url = "http://youtu.be/%s"


def plural(num=0, text=''):
    return "{:,} {}{}".format(num, text, "s"[num==1:])


def get_video_description(key,video_id):
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
        if   t[-1:] == 'D': seconds += 86400 * t_field
        elif t[-1:] == 'H': seconds += 3600 * t_field
        elif t[-1:] == 'M': seconds += 60 * t_field
        elif t[-1:] == 'S': seconds += t_field

    out += u' - length \x02{}\x02'.format(timeformat.format_time(seconds, simple=True))

    try:
        data['statistics']
    except KeyError:
        return out

    stats = data['statistics']
    try:
        likes = plural(int(stats['likeCount']), "like")
        dislikes = plural(int(stats['dislikeCount']), "dislike")
        try:
            percent = 100 * float(stats['likeCount'])/(int(stats['likeCount'])+int(stats['dislikeCount']))
        except ZeroDivisionError:
            percent = 0
    except KeyError:
        likes = 'likes disabled'
        dislikes = 'dislikes disabled'
        percent = 0

    out += u' - {}, {} (\x02{:.1f}\x02%)'.format(likes, dislikes, percent)

    views = int(stats['viewCount'])
    out += u' - \x02{:,}\x02 {}{}'.format(views, 'view', "s"[views==1:])

    uploader = data['snippet']['channelTitle']

    upload_time = time.strptime(data['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%S.000Z")
    out += u' - \x02{}\x02 on \x02{}\x02'.format(uploader, time.strftime("%Y.%m.%d", upload_time))

    try:
        data['contentDetails']['contentRating']
    except KeyError:
        return out

    out += u' - \x034NSFW\x02'

    return out


@hook.regex(*youtube_re)
def youtube_url(match,bot=None):
    key = bot.config.get("api_keys", {}).get("youtube")

    return get_video_description(key,match.group(1))


@hook.command('yt')
@hook.command
def youtube(inp, bot=None):
    """youtube <query> -- Returns the first YouTube search result for <query>."""
    key = bot.config.get("api_keys", {}).get("youtube")

    request = http.get_json(search_api_url, key=key, q=inp, type='video')

    if 'error' in request:
        return 'Error performing search.'

    if request['pageInfo']['totalResults'] == 0:
        return 'No results found.'

    video_id = request['items'][0]['id']['videoId']

    return get_video_description(key,video_id) + u" - " + video_url % video_id


@hook.command('ytime')
@hook.command
def youtime(inp, bot=None):
    """youtime <query> -- Gets the total run time of the first YouTube search result for <query>."""
    key = bot.config.get("api_keys", {}).get("youtube")
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
        if   t[-1:] == 'D': seconds += 86400 * t_field
        elif t[-1:] == 'H': seconds += 3600 * t_field
        elif t[-1:] == 'M': seconds += 60 * t_field
        elif t[-1:] == 'S': seconds += t_field

    views = int(data['statistics']['viewCount'])
    total = int(seconds * views)

    length_text = timeformat.format_time(seconds, simple=True)
    total_text = timeformat.format_time(total, accuracy=8)

    return u'The video \x02{}\x02 has a length of {} and has been viewed {:,} times for ' \
            'a total run time of {}!'.format(data['snippet']['title'], length_text, views, total_text)


ytpl_re = (r'(.*:)//(www.youtube.com/playlist|youtube.com/playlist)(:[0-9]+)?(.*)', re.I)

@hook.regex(*ytpl_re)
def youtubeplaylist_url(match):
    location = match.group(4).split("=")[-1]

    try:
        soup = http.get_soup("https://www.youtube.com/playlist?list=" + location)
    except Exception:
        return "\x034\x02Invalid response."

    title = soup.find('title').text.split('-')[0].strip()
    author = soup.find('img', {'class': 'channel-header-profile-image'})['title']
    numvideos = soup.find('ul', {'class': 'pl-header-details'}).findAll('li')[1].string
    numvideos = re.sub("\D", "", numvideos)
    views = soup.find('ul', {'class': 'pl-header-details'}).findAll('li')[2].string
    views = re.sub("\D", "", views)

    return u"\x02{}\x02 - \x02{}\x02 views - \x02{}\x02 videos - \x02{}\x02".format(title, views, numvideos, author)
