from util import hook, http
import random
import re

furry_cache = []
lastsearch = ''

def refresh_cache(inp):
    global furry_cache
    furry_cache = []
    num = 0
    search = inp.replace(' ','+').replace('explicit','rating:explicit').replace('nsfw','rating:explicit').replace('safe','rating:safe').replace('sfw','rating:safe')
    soup = http.get_soup('http://e621.net/post/index.xml?limit=20&page=1&tags={}'.format(inp))
    posts = soup.find_all('post')

    while num < len(posts):
        furry_cache.append((posts[num].get('id'), posts[num].get('score'), posts[num].get('file_url'),posts[num].get('rating'),posts[num].get('tags')))
        num += 1

    random.shuffle(furry_cache)
    return

@hook.command('e621', autohelp=False)
@hook.command(autohelp=False)
def furry(inp, reply=None):
    global lastsearch
    global furry_cache

    inp = inp.lower()
    if not inp in lastsearch or len(furry_cache) < 2: refresh_cache(inp)

    lastsearch = inp

    if len(furry_cache) == 0:
        return 'No Results'

    id, score, url, rating, tags = furry_cache.pop()
    
    if rating is 'e': rating = "\x02\x034NSFW\x03\x02"
    elif rating is 'q': rating = "\x02Questionable\x02"
    elif rating is 's': rating = "\x02\x033Safe\x03\x02"

    return u'\x02[{}]\x02 Score: \x02{}\x02 - Rating: {} - {}'.format(id, score, rating, url)