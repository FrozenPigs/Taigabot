import random
from util import hook, http, text, database, web
import re
from urllib import urlencode
import random

api_url = "https://www.googleapis.com/customsearch/v1?"

@hook.command('search')
@hook.command('g')
@hook.command
def google(inp,db=None,chan=None, bot=None):
    """google <query> -- Returns first google search result for <query>."""
    key = bot.config.get("api_keys", {}).get("youtube")
    cx = bot.config.get("api_keys", {}).get("cx")

    data = http.get_json(api_url + urlencode({'q': inp, 'key': key, 'cx': cx, 'safe': 'off'}))


    return u'{} -- \x02{}\x02"'.format(data["items"][0]["link"], data["items"][0]["title"])


# @hook.command('image')
@hook.command('gis')
@hook.command('gi')
@hook.command('image')
@hook.command
def googleimage(inp, bot=None):
    """gis <query> -- Returns first Google Image result for <query>."""

    key = bot.config.get("api_keys", {}).get("youtube")
    cx = bot.config.get("api_keys", {}).get("cx")
    data = http.get_json(api_url + urlencode({'q': inp, 'key': key, 'cx': cx, 'searchType': 'image', 'safe': 'off'}))

    ran = random.randint(0, 10)

    return u'{}'.format(data["items"][ran]["link"])



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
@hook.command('gfy')
@hook.command
def lmgtfy(inp, bot=None):
    "lmgtfy [phrase] - Posts a google link for the specified phrase"

    link = "http://lmgtfy.com/?q=%s" % http.quote_plus(inp)

    try:
        return web.isgd(link)
    except (web.ShortenError, http.HTTPError):
        return link

