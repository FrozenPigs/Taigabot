# bible/koran plugin by ine (2020)
from util import hook
from utilities import request, iterable
from utilities.formatting import compress_whitespace
from bs4 import BeautifulSoup


@hook.command('god')
@hook.command
def bible(inp, bot=None):
    """bible <passage> -- gets <passage> from the Bible (ESV)"""

    API_KEY = bot.config['api_keys'].get('english_bible', None)

    if API_KEY is None:
        return 'Bible error: no API key configured'

    url = "https://api.esv.org/v3/passage/text/?q=" + request.urlencode(inp)
    json = request.get_json(url, headers={"Authorization": "Token " + API_KEY})

    if 'detail' in json:
        return 'Bible error (lol): ' + json['detail']

    if 'passages' in json and len(json['passages']) == 0:
        return '[Bible] Not found'

    output = '[Bible]'

    if 'canonical' in json:
        output = output + ' \x02' + json['canonical'] + '\x02:'

    if 'passages' in json:
        output = output + ' ' + compress_whitespace('. '.join(json['passages']))

    if len(output) > 320:
        output = output[:320] + '...'

    return output


@hook.command('allah')
@hook.command
def koran(inp):
    "koran <chapter.verse> -- gets <chapter.verse> from the Koran. it can also search any text."

    url = 'https://quod.lib.umich.edu/cgi/k/koran/koran-idx?type=simple&q1=' + request.urlencode(inp)
    html = request.get(url)
    soup = BeautifulSoup(html, 'lxml')
    query = soup.find_all('li')

    if not query or len(query) == 0:
        return 'No results for ' + inp

    output = '[Koran] '
    lines = []

    for li in iterable.limit(4, query):
        lines.append(compress_whitespace(li.text))

    output = output + ' '.join(lines)

    if len(output) > 320:
        output = output[:320] + '...'

    return output
