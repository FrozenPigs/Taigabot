from util import hook, http
import requests
import urllib


@hook.command('god')
@hook.command
def bible(inp):
    """.bible <passage> -- gets <passage> from the Bible (ESV)"""

    text = requests.get("https://api.esv.org/v3/passage/html/?q={}".format(urllib.quote(inp)), headers={"Authorization": "Token e1733632cb3a360e8d4db70b13da07f2df5c785d"})
    print(text.text)
    text = ' '.join(text.split())

    if len(text) > 400:
        text = text[:text.rfind(' ', 0, 400)] + '...'

    return text


@hook.command('allah')
@hook.command
def koran(inp):  # Koran look-up plugin by Ghetto Wizard
    ".koran <chapter.verse> -- gets <chapter.verse> from the Koran"

    url = 'http://quod.lib.umich.edu/cgi/k/koran/koran-idx?type=simple'

    results = http.get_html(url, q1=inp).xpath('//li')

    if not results:
        return 'No results for ' + inp

    return results[0].text_content()
