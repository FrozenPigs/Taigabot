from util import hook, web
from utilities import request, formatting
import re

imp_reg = (r'^\>(.*\.(gif|jpe?g|png|tiff|bmp))$', re.I)
API_URL = 'https://www.googleapis.com/customsearch/v1'


def api_get(kind, query):
    """Use the RESTful Google Search API."""
    if kind == 'image':
        url = API_URL + u'?key={}&cx={}&searchType={}&num=1&safe=off&q={}'
        return request.get_json(url.format(query[0], query[1], kind, query[2]))
    elif kind == 'images':
        url = API_URL + u'?key={}&cx={}&searchType={}&num=1&safe=off&q={}&fileType="{}"'
        return request.get_json(url.format(query[0], query[1], 'image', query[2], query[3]))
    else:
        url = API_URL + u'?key={}&cx={}&num=1&safe=off&q={}'
        return request.get_json(url.format(query[0], query[1], query[2].encode('utf-8')))


@hook.command('search')
@hook.command('g')
@hook.command
def google(inp, bot=None):
    """google <query> -- Returns first google search result for <query>."""
    inp = request.urlencode(inp)

    # what the fuck
    try:
        cx = bot.config['api_keys']['googleimage']
        key = bot.config['api_keys']['google']
        query = [key, cx, '+'.join(inp.split())]
        result = api_get('None', query)['items'][0]
    except:
        cx = bot.config['api_keys']['googleimage']
        key = bot.config['api_keys']['google2']
        query = [key, cx, '+'.join(inp.split())]
        result = api_get('None', query)['items'][0]

    title = result['title']
    content = formatting.remove_newlines(result['snippet'])
    link = result['link']

    try:
        return u'{} -- \x02{}\x02: "{}"'.format(web.isgd(link), title, content)
    except Exception:
        return u'{} -- \x02{}\x02: "{}"'.format(link, title, content)


@hook.command('wiki')
def fake_wikipedia(inp, bot=None):
    """wiki <query> -- search wikipedia"""
    inp = u'site:wikipedia.org {}'.format(inp)
    return google(inp, bot)


@hook.command('gi')
def image(inp, bot=None):
    """image <query> -- Returns the first Google Image result for <query>."""
    try:
        cx = bot.config['api_keys']['googleimage']
        key = bot.config['api_keys']['google']
        query = [key, cx, '+'.join(inp.split())]
        image = api_get('image', query)['items'][0]['link']
    except Exception:
        cx = bot.config['api_keys']['googleimage']
        key = bot.config['api_keys']['google2']
        query = [key, cx, '+'.join(inp.split())]
        image = api_get('image', query)['items'][0]['link']

    print image

    try:
        return web.isgd(image)
    except Exception as e:
        print '[!] Error while shortening:', e
        return image


@hook.regex(*imp_reg)
def implying(inp, bot=None):
    """><query>.jpg -- Returns the first Google Image result for <query>.jpg"""
    inp = inp.string[1:].split('.')
    filetype = inp[1]
    cx = bot.config['api_keys']['googleimage']
    key = bot.config['api_keys']['google']
    query = [key, cx, '+'.join(inp[0].split()), filetype]
    image = api_get('images', query)['items'][0]['link']

    try:
        return web.isgd(image)
    except Exception as e:
        print '[!] Error while shortening:', e
        return image
