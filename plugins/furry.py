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
    if inp == '':
        soup = http.get_soup('http://e621.net/post/index.xml?limit=20&page=1')
    else:
        soup = http.get_soup('http://e621.net/post/index.xml?limit=20&page=1&tags={}'.format(inp))
    posts = soup.find_all('post')

    for post in posts:
        id = post.find_all('id')[0].get_text()
        score = post.find_all('score')[0].get_text()
        url = post.find_all('file_url')[0].get_text()
        rating = post.find_all('rating')[0].get_text()
        tags = post.find_all('tags')[0].get_text()
        furry_cache.append((id, score, url, rating,tags))

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

    if rating == 'e':
        rating = "\x02\x034NSFW\x03\x02"
    elif rating == 'q':
        rating = "\x02Questionable\x02"
    elif rating == 's':
        rating = "\x02\x033Safe\x03\x02"

    return u'\x02[{}]\x02 Score: \x02{}\x02 - Rating: {} - {}'.format(id, score, rating, url)
