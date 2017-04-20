from util import hook, http
import re

fml_cache = []

def refresh_cache():
    """ gets a page of random FMLs and puts them into a dictionary """
    soup = http.get_soup('http://www.fmylife.com/random/')

    for e in soup.find_all('a', attrs={'class': 'fmllink'}):
        id = int(e['href'].split('/')[-1])
        text = e.text
        fml_cache.append((id, text))

# do an initial refresh of the cache
refresh_cache()

@hook.command(autohelp=False)
def fml(inp, reply=None):
    "fml -- Gets a random quote from fmyfife.com."

    # grab the last item in the fml cache and remove it
    try:
        id, text = fml_cache.pop()
    except IndexError:
        refresh_cache()
        id, text = fml_cache.pop()
    # reply with the fml we grabbed
    reply('(#%d) %s' % (id, text))
    # refresh fml cache if its getting empty
    if len(fml_cache) < 3:
        refresh_cache()
