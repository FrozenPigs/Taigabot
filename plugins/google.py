import random
from util import hook, http, text, database, web
import re

def api_get(kind, query):
    """Use the RESTful Google Search API"""
    url = 'http://ajax.googleapis.com/ajax/services/search/%s?' \
          'v=1.0&safe=off'
    return http.get_json(url % kind, q=query)


@hook.command('search')
@hook.command('g')
@hook.command
def google(inp,db=None,chan=None):
    """google <query> -- Returns first google search result for <query>."""
    trimlength = database.get(db,'channels','trimlength','chan',chan)
    if not trimlength: trimlength = 9999 

    parsed = api_get('web', inp)
    if not 200 <= parsed['responseStatus'] < 300:
        raise IOError('error searching for pages: {}: {}'.format(parsed['responseStatus'], ''))
    if not parsed['responseData']['results']:
        return 'No results found.'

    result = parsed['responseData']['results'][0]
    title = http.unescape(result['titleNoFormatting'])
    content = http.unescape(result['content'])

    if not content: content = "No description available."
    else: content = http.html.fromstring(content.replace('\n', '')).text_content()

    return u'{} -- \x02{}\x02: "{}"'.format(result['unescapedUrl'], title, content)


# @hook.command('image')
@hook.command('gis')
@hook.command('gi')
@hook.command('image')
@hook.command
def googleimage(inp):
    """gis <query> -- Returns first Google Image result for <query>."""

    parsed = api_get('images', inp)
    if not 200 <= parsed['responseStatus'] < 300:
        raise IOError('error searching for images: {}: {}'.format(parsed['responseStatus'], ''))
    if not parsed['responseData']['results']:
        return 'no images found'
    return random.choice(parsed['responseData']['results'][:10])['unescapedUrl']


@hook.command
def gcalc(inp):
    "gcalc <term> -- Calculate <term> with Google Calc."
    soup = http.get_soup('http://www.google.com/search', q=inp)

    result = soup.find('span', {'class': 'cwcot'})
    formula = soup.find('span', {'class': 'cwclet'})
    if not result:
        return "Could not calculate '{}'".format(inp)

    return u"{} {}".format(formula.contents[0].strip(),result.contents[0].strip())


@hook.regex(r'^\>(.*\.(gif|GIF|jpg|JPG|jpeg|JPEG|png|PNG|tiff|TIFF|bmp|BMP))\s?(\d+)?')
@hook.command
def implying(inp):
    """>laughing girls.gif <num> -- Returns first Google Image result for <query>."""
    try: search = inp.group(1)
    except: search = inp
    try: num = int(inp.group(3))
    except: num = 0
    
    if 'http' in search: return

    parsed = api_get('images', search)
    if not 200 <= parsed['responseStatus'] < 300:
        raise IOError('error searching for images: {}: {}'.format(parsed['responseStatus'], ''))
    if not parsed['responseData']['results']:
        return 'no images found'
    try: return u'\x033\x02>{}\x02\x03 {}'.format(search, parsed['responseData']['results'][:10][num]['unescapedUrl'])
    except: return u'\x033\x02>{}\x02\x03 {}'.format(search, parsed['responseData']['results'][:10][0]['unescapedUrl'])
    #return random.choice(parsed['responseData']['results'][:10])['unescapedUrl']


@hook.command('nym')
@hook.command('littleanon')
@hook.command('gfy')
@hook.command
def lmgtfy(inp, bot=None):
    "lmgtfy [phrase] - Posts a google link for the specified phrase"

    link = "http://lmgtfy.com/?q=%s" % http.quote_plus(inp)

    try:
        return web.isgd(link)
    except (web.ShortenError, http.HTTPError):
        return link

