import re

from util import hook, web
from utilities import formatting, request

API_URL = 'https://www.googleapis.com/customsearch/v1'


@hook.command('search')
@hook.command('g')
@hook.command
def google(inp, bot=None):
    """google <query> -- Returns first google search result for <query>."""
    inp = request.urlencode(inp)

    url = API_URL + u'?key={}&cx={}&num=1&safe=off&q={}'
    cx = bot.config['api_keys']['googleimage']
    search = '+'.join(inp.split())
    key = bot.config['api_keys']['google']
    result = request.get_json(url.format(key, cx, search.encode('utf-8')))['items'][0]

    title = result['title']
    content = formatting.remove_newlines(result['snippet'])
    link = result['link']

    try:
        return u'{} -- \x02{}\x02: "{}"'.format(web.isgd(link), title, content)
    except Exception:
        return u'{} -- \x02{}\x02: "{}"'.format(link, title, content)


@hook.regex(r'^\>(.*\.(gif|jpe?g|png|tiff|bmp))$', re.I)
@hook.command('gi')
def image(inp, bot=None):
    """image <query> -- Returns the first Google Image result for <query>."""
    if type(inp) is unicode:
        filetype = None
    else:
        inp, filetype = inp.string[1:].split('.')

    cx = bot.config['api_keys']['googleimage']
    search = '+'.join(inp.split())
    key = bot.config['api_keys']['google']

    if filetype:
        url = API_URL + u'?key={}&cx={}&searchType=image&num=1&safe=off&q={}&fileType={}'
        result = request.get_json(url.format(key, cx, search.encode('utf-8'),
                                             filetype))['items'][0]['link']
    else:
        url = API_URL + u'?key={}&cx={}&searchType=image&num=1&safe=off&q={}'
        result = request.get_json(url.format(key, cx, search.encode('utf-8')))['items'][0]['link']

    try:
        return web.isgd(result)
    except Exception as e:
        print '[!] Error while shortening:', e
        return result
