from util import hook, http
import random
import re

furry_cache = []
lastsearch = ''

def refresh_cache(inp):
    global furry_cache
    furry_cache = []
    num = 0
    search = inp.replace(' ','%20').replace('explicit','rating:explicit').replace('nsfw','rating:explicit').replace('safe','rating:safe').replace('sfw','rating:safe')
    if inp == '':
        postjson = http.get_json('http://e621.net/posts.json?limit=20')
    else:
        postjson = http.get_json('http://e621.net/posts.json?limit=20&tags={}'.format(search))
    posts = postjson.posts

    for i in range(len(posts)):
        post = posts[i]
        id = post.id.get_text()
        score = post.score.total.get_text()
        url = post.file.url
        rating = post.rating
        tags = post.tags.general.join(", ")
        furry_cache.append((id, score, url, rating, tags))

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
