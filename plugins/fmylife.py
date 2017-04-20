from util import hook, http
<<<<<<< HEAD
import re
=======
>>>>>>> infinuguu/master

fml_cache = []

def refresh_cache():
    """ gets a page of random FMLs and puts them into a dictionary """
    soup = http.get_soup('http://www.fmylife.com/random/')

<<<<<<< HEAD
    for e in soup.find_all('a', attrs={'class': 'fmllink'}):
        id = int(e['href'].split('/')[-1])
        text = e.text
=======
    for e in soup.find_all('div', {'class': 'post article'}):
        id = int(e['id'])
        text = ''.join(e.find('p').find_all(text=True))
>>>>>>> infinuguu/master
        fml_cache.append((id, text))

# do an initial refresh of the cache
refresh_cache()

@hook.command(autohelp=False)
def fml(inp, reply=None):
    "fml -- Gets a random quote from fmyfife.com."

    # grab the last item in the fml cache and remove it
<<<<<<< HEAD
    try:
        id, text = fml_cache.pop()
    except IndexError:
        refresh_cache()
        id, text = fml_cache.pop()
=======
    id, text = fml_cache.pop()
>>>>>>> infinuguu/master
    # reply with the fml we grabbed
    reply('(#%d) %s' % (id, text))
    # refresh fml cache if its getting empty
    if len(fml_cache) < 3:
        refresh_cache()
