from util import hook, http
import random
import re

gelbooru_cache = []
lastsearch = ''

def refresh_cache(inp):
    global gelbooru_cache
    gelbooru_cache = []
    num = 0
    search = inp.replace(' ','+').replace('explicit','rating:explicit').replace('nsfw','rating:explicit').replace('safe','rating:safe').replace('sfw','rating:safe')
    # score:>100
    #print 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=20&tags={}'.format(search)
    soup = http.get_soup(u'http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=20&tags={}'.format(search))
    posts = soup.find_all('post')

    while num < len(posts):
        gelbooru_cache.append((posts[num].get('id'), posts[num].get('score'), posts[num].get('file_url'),posts[num].get('rating'),posts[num].get('tags')))
        num += 1

    random.shuffle(gelbooru_cache)
    return


# @hook.command('sb', autohelp=False)

@hook.command('gb', autohelp=False)
@hook.command(autohelp=False)
def gelbooru(inp, reply=None):
    "gelbooru <tags> -- Gets a random image from gelbooru.com"
    global lastsearch
    global gelbooru_cache

    search = inp.lower()
    if not search in lastsearch or len(gelbooru_cache) < 2: refresh_cache(search)
    lastsearch = search

    if len(gelbooru_cache) == 0: return "No Results"

    id, score, url, rating, tags = gelbooru_cache.pop()
    
    if rating is 'e': rating = "\x02\x034NSFW\x03\x02"
    elif rating is 'q': rating = "\x02\x037Questionable\x03\x02"
    elif rating is 's': rating = "\x02\x033Safe\x03\x02"

    return u'\x02[{}]\x02 Score: \x02{}\x02 - Rating: {} - {}'.format(id, score, rating, url)
    # return u'\x02[{}]\x02 Score: \x02{}\x02 - Rating: {} - {} - {}'.format(id, score, rating, url, tags[:75].strip())



gelbooru_list_re = (r'(.+gelbooru.com/.+list&tags.+)', re.I)
@hook.regex(*gelbooru_list_re)
def gelbooru_list_url(match):
    soup = http.get_soup(match.group(1))
    return u'{}'.format(soup.find('title').text)


gelbooru_re = (r'(?:gelbooru.com.*?id=)([-_a-zA-Z0-9]+)', re.I)
@hook.regex(*gelbooru_re)
def gelbooru_url(match):
    soup = http.get_soup('http://gelbooru.com/index.php?page=dapi&s=post&q=index&id={}'.format(match.group(1)))
    posts = soup.find_all('post')

    id, score, url, rating, tags = (posts[0].get('id'), posts[0].get('score'), posts[0].get('file_url'),posts[0].get('rating'),posts[0].get('tags'))

    if rating is 'e': rating = "\x02\x034NSFW\x03\x02"
    elif rating is 'q': rating = "\x02\x037Questionable\x03\x02"
    elif rating is 's': rating = "\x02\x033Safe\x03\x02"

    return u'\x02[{}]\x02 Score: \x02{}\x02 - Rating: {} - {} - {}'.format(id, score, rating, url, tags[:75].strip())


# http://gelbooru.com/index.php?page=post&s=list&tags=%3D_%3D