from util import hook, request
from bs4 import BeautifulSoup

# TODO get a working api key
# u need like a church email to register or something idk
# also move it to the config file
API_KEY = "e1733632cb3a360e8d4db70b13da07f2df5c785d"

@hook.command('god')
@hook.command
def bible(inp):
    """.bible <passage> -- gets <passage> from the Bible (ESV)"""

    url = "https://api.esv.org/v3/passage/text/?q=" + request.urlencode(inp)
    json = request.get_json(url, headers={"Authorization": "Token " + API_KEY})

    if 'detail' in json:
        return 'Bible error (lol): ' + json['detail']

    output = '[Bible]'

    if 'canonical' in json:
        output = output + '\x02' + json['canonical'] + '\x02:'

    if 'passages' in json:
        output = output + '. '.join(json['passages'])

    if len(output) > 320:
        output = output[:320] + '...'

    return output


@hook.command('allah')
@hook.command
def koran(inp):  # Koran look-up plugin by Ghetto Wizard
    ".koran <chapter.verse> -- gets <chapter.verse> from the Koran. it can also search any text."

    url = 'https://quod.lib.umich.edu/cgi/k/koran/koran-idx?type=simple&q1='

    html = request.get_html(url + request.urlencode(inp))
    soup = BeautifulSoup(html, 'lxml')
    query = soup.find_all('li')

    if not query or len(query) == 0:
        return 'No results for ' + inp

    output = '[Koran] '

    for li in query:
        output = output + ' ' + li.text

    if len(output) > 320:
        output = output[:320] + '...'

    return output
