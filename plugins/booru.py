from util import hook, formatting, web
from utilities import request

# coded around the danbooru and moebooru api.
# danbooru, moebooru, myimouto and all of their forks use the same api
boorus = {
    'yandere': {
        'name': 'yande.re',
        'url': 'https://yande.re',
        'api': '/post.json'
    },
    'danbooru': {
        'name': 'Danbooru',
        'url': 'https://danbooru.donmai.us',
        'api': '/posts.json'
    }
}

# i did some dumb cache system (which probably should be a class)
# it will store a list under a key and pop items from the list as they're read
# make sure the key is something unique like "booru name + search query"
CACHE = {}


def cache_key_exists(key):
    global CACHE
    # only return True if the cache has the key AND at least one entry
    if key in CACHE and len(CACHE[key]) > 0:
        return True
    else:
        return False


def cache_get_item(key):
    # check key_exists first, or this will throw
    global CACHE
    return CACHE[key].pop(0)


def cache_append_item(key, value):
    global CACHE

    if key not in CACHE:
        CACHE[key] = []

    CACHE[key].append(value)


def cache_debug():
    global CACHE
    for key in CACHE:
        print 'THE ENTRY {} HAS {} ITEMS'.format(key, len(CACHE[key]))


def get_post(booru_id, tags=''):
    if tags:
        cache_key = booru_id + ' ' + tags
    else:
        cache_key = booru_id + ' most recent'

    # if cache has data for this search, then just use that
    if cache_key_exists(cache_key):
        return cache_get_item(cache_key)

    # otherwise we need to download and fill the cache
    api = boorus[booru_id]['url'] + boorus[booru_id]['api']
    if tags:
        json = request.get_json(api, params={'limit': 20, 'tags': tags})
    else:
        json = request.get_json(api, params={'limit': 80})

    if len(json) == 0:
        return None

    images = []

    for item in json:
        # skip pixiv, all direct links are "403 denied"
        if 'pixiv_id' in item and 'file_url' not in item:
            continue

        image = {
            'id': item['id'],
            'created': item['created_at'],
            'file_url': item['file_url'],
            'file_size': item['file_size'],
            'rating': item.get('rating', 'e'),
            'score': item.get('score', 0),
            'tags': item.get('tags', item.get('tag_string', 'unknown'))
        }

        if not image['file_url'].startswith('http'):
            image['file_url'] = boorus[booru_id]['url'] + image['file_url']

        cache_append_item(cache_key, image)

    # yes, check again if we added anything at all
    if cache_key_exists(cache_key):
        return cache_get_item(cache_key)
    else:
        return None


@hook.command
def yandere(inp):
    post = get_post('yandere', inp)
    if post is None:
        return "nothing found"

    return message(post)


@hook.command
def danbooru(inp):
    post = get_post('danbooru', inp)
    if post is None:
        return "nothing found on those tags"

    return message(post)


def message(post):
    if post['rating'] == u'e':
        rating = '\x02\x034NSFW\x03\x02'
    elif post['rating'] == u'q':
        rating = '\x02\x037questionable\x03\x02'
    elif post['rating'] == u's':
        rating = '\x02\x033safe\x03\x02'
    else:
        rating = 'unknown'

    id = '\x02#{}\x02'.format(post['id'])
    score = post['score']
    url = web.isgd(post['file_url'])
    size = formatting.filesize(post['file_size'])
    tags = post['tags']
    if len(tags) > 80:
        tags = '{}... (and {} more)'.format(tags[:80], tags.count(' '))  # this count() is wrong lol, close enough

    return "[{}] Score: {} - Rating: {} - {} ({}) - Tags: {}".format(id, score, rating, url, size, tags)
