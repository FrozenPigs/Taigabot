from util import hook, http, web
import re
import random

yandere_cache = []

def refresh_cache():
    "gets a page of random yande.re posts and puts them into a dictionary "
    url = 'https://yande.re/post?page=%s' % random.randint(1,11000)
    soup = http.get_soup(url)

    for result in soup.findAll('li'):
        title = result.find('img', {'class': re.compile(r'\bpreview\b')}) #['title']
        img = result.find('a', {'class': re.compile(r'\bdirectlink\b')}) #['href']
        if img and title:
            yandere_cache.append((result['id'].replace('p','') ,title['title'].split(' User')[0], img['href']))

def get_yandere_tags(inp):
    url = 'https://yande.re/post?tags=%s' % inp.replace(' ','_')
    soup = http.get_soup(url)
    imagelist = soup.find('ul', {'id': 'post-list-posts'}).findAll('li')
    image = imagelist[random.randint(0,len(imagelist)-1)]
    imageid = image["id"].replace('p','')
    title = image.find('img')['title']
    src = image.find('a', {'class': 'directlink'})["href"]
    return u"\x034NSFW\x03: \x02({})\x02 {}: {}".format(imageid, title, web.isgd(http.unquote(src)))

#do an initial refresh of the cache
refresh_cache()

@hook.command(autohelp=False)
def yandere(inp, reply=None):
    "tandere [tags] -- Yande.re -- Gets a random image from Yande.re."

    if inp: return get_yandere_tags(inp)

    id, title, image = yandere_cache.pop()
    reply(u'\x034NSFW\x03: \x02(%s)\x02 %s: %s' % (id, title[:75], web.isgd(image)))
    if len(yandere_cache) < 3:
        refresh_cache()