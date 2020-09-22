from util import hook, http, web
import random
import re
import urllib
import urllib2

gelbooru_cache = []
gb_lastsearch = ''


def gb_refresh_cache(inp):
    global gelbooru_cache
    gelbooru_cache = []
    num = 0
    search = (
        inp.replace(' ', '+')
        .replace('explicit', 'rating:explicit')
        .replace('nsfw', 'rating:explicit')
        .replace('safe', 'rating:safe')
        .replace('sfw', 'rating:safe')
    )
    # score:>100
    # print 'http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=20&tags={}'.format(search)
    # try:
    #     soup = http.get_soup(u'http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=20&tags={}'.format(search), cookies=True)
    #     posts = soup.find_all('post')
    # except:
    post_data = {'user': 'frozenpigs', 'pass': 'noscope90', 'submit': 'Log in'}
    data = urllib.urlencode(post_data)
    authurl = u'http://gelbooru.com/index.php?page=account&s=login&code=00'
    http.get_soup(authurl, post_data=data, cookies=True)
    soup = http.get_soup(
        u'http://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=20&tags={}'.format(search), cookies=True
    )
    posts = soup.find_all('post')

    while num < len(posts):
        gelbooru_cache.append(
            (
                posts[num].get('id'),
                posts[num].get('score'),
                posts[num].get('file_url'),
                posts[num].get('rating'),
                posts[num].get('tags'),
            )
        )
        num += 1

    random.shuffle(gelbooru_cache)
    return


# @hook.command('sb', autohelp=False)


@hook.command('gb', autohelp=False)
@hook.command('loli', autohelp=False)
@hook.command('shota', autohelp=False)
@hook.command('trap', autohelp=False)
@hook.command('futa', autohelp=False)
@hook.command('futanari', autohelp=False)
@hook.command(autohelp=False)
def gelbooru(inp, reply=None, input=None):
    "gelbooru <tags> -- Gets a random image from gelbooru.com"
    global gb_lastsearch
    global gelbooru_cache
    inp = inp.split(' ')
    filetype = inp[-1]
    filetypes = ['png', 'jpg', 'jpeg']
    if filetype not in filetypes:
        filetype = None
    try:
        inp.pop(inp.index(filetype))
    except ValueError:
        pass
    if len(inp) >= 2:
        inp = ' '.join(inp)
    else:
        inp = ''.join(inp)

    if input.trigger == u'loli':
        search = 'loli' + '+' + inp.lower()
    elif input.trigger == u'shota':
        search = 'shota' + '+' + inp.lower()
    elif input.trigger == u'futa' or input.trigger == u'futanari':
        search = 'futanari' + '+' + inp.lower()
    elif input.trigger == u'trap':
        search = 'trap' + '+' + inp.lower()
    else:
        search = inp.lower()
    search = search.split(' ')
    for i, n in enumerate(search):
        if n == u'gif':
            search[i] = 'animated_gif'
    if len(search) >= 2:
        search = ' '.join(search)
    else:
        search = ''.join(search)
    if not search in gb_lastsearch or len(gelbooru_cache) < 2:
        gb_refresh_cache(search)
    gb_lastsearch = search

    if len(gelbooru_cache) == 0:
        reply('No results')
        return

    id, score, url, rating, tags = gelbooru_cache.pop()
    if filetype:
        counter = 0
        while not url.endswith(filetype):
            try:
                if counter == 5:
                    reply('No results')
                    return
                id, score, url, rating, tags = gelbooru_cache.pop()
            except IndexError:
                counter += 1
                gb_refresh_cache(search)

    if rating is 'e':
        rating = "\x02\x034NSFW\x03\x02"
    elif rating is 'q':
        rating = "\x02\x037Questionable\x03\x02"
    elif rating is 's':
        rating = "\x02\x033Safe\x03\x02"

    try:
        return u'\x02[{}]\x02 Score: \x02{}\x02 - Rating: {} - {}'.format(id, score, rating, web.isgd(url))
    except:
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

    id, score, url, rating, tags = (
        posts[0].get('id'),
        posts[0].get('score'),
        posts[0].get('file_url'),
        posts[0].get('rating'),
        posts[0].get('tags'),
    )

    if rating is 'e':
        rating = "\x02\x034NSFW\x03\x02"
    elif rating is 'q':
        rating = "\x02\x037Questionable\x03\x02"
    elif rating is 's':
        rating = "\x02\x033Safe\x03\x02"

    return u'\x02[{}]\x02 Score: \x02{}\x02 - Rating: {} - {} - {}'.format(id, score, rating, url, tags[:75].strip())


# http://gelbooru.com/index.php?page=post&s=list&tags=%3D_%3D

danbooru_cache = []
db_lastsearch = ''


def db_refresh_cache(inp):
    global danbooru_cache
    danbooru_cache = []
    num = 0
    search = (
        inp.replace(' ', '+')
        .replace('explicit', 'rating:explicit')
        .replace('nsfw', 'rating:explicit')
        .replace('safe', 'rating:safe')
        .replace('sfw', 'rating:safe')
    )
    posts = http.get_json('http://danbooru.donmai.us/posts.json?tags={}&limit=20'.format(search))

    while num < len(posts):
        danbooru_cache.append(
            (
                posts[num].get('id'),
                posts[num].get('score'),
                posts[num].get('file_url'),
                posts[num].get('rating'),
                posts[num].get('tags'),
            )
        )
        num += 1

    random.shuffle(danbooru_cache)
    return


# @hook.command('sb', autohelp=False)


@hook.command('dan', autohelp=False)
@hook.command(autohelp=False)
def danbooru(inp, reply=None, input=None):
    "gelbooru <tags> -- Gets a random image from gelbooru.com"
    global db_lastsearch
    global danbooru_cache
    inp = inp.split(' ')
    filetype = inp[-1]
    filetypes = ['png', 'jpg', 'jpeg']
    if filetype not in filetypes:
        filetype = None
    try:
        inp.pop(inp.index(filetype))
    except ValueError:
        pass
    if len(inp) >= 2:
        inp = ' '.join(inp)
    else:
        inp = ''.join(inp)

    search = inp.lower().split()
    for i, n in enumerate(search):
        if n == u'gif':
            search[i] = 'animated_gif'
    if len(search) >= 2:
        search = ' '.join(search)
    else:
        search = ''.join(search)
    if not search in db_lastsearch or len(danbooru_cache) < 2:
        db_refresh_cache(search)
    db_lastsearch = search

    if len(danbooru_cache) == 0:
        reply('No results')
        return

    id, score, url, rating, tags = danbooru_cache.pop()
    if filetype:
        counter = 0
        while not url.endswith(filetype):
            try:
                if counter == 5:
                    reply('No results')
                    return
                id, score, url, rating, tags = danbooru_cache.pop()
            except IndexError:
                counter += 1
                db_refresh_cache(search)

    if rating == u'e':
        rating = "\x02\x034NSFW\x03\x02"
    elif rating == u'q':
        rating = "\x02\x037Questionable\x03\x02"
    elif rating == u's':
        rating = "\x02\x033Safe\x03\x02"
    url = 'http://danbooru.donmai.us' + url

    try:
        return u'\x02[{}]\x02 Score: \x02{}\x02 - Rating: {} - {}'.format(id, score, rating, web.isgd(url))
    except:
        return u'\x02[{}]\x02 Score: \x02{}\x02 - Rating: {} - {}'.format(id, score, rating, url)
    # return u'\x02[{}]\x02 Score: \x02{}\x02 - Rating: {} - {} - {}'.format(id, score, rating, url, tags[:75].strip())
