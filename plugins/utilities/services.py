import requests

user = 'taigabot'

HEADERS = {'User-Agent': 'taigabot, python irc bot'}


def paste_taigalink(text, title='Paste'):
    data = {
        'title': title,
        'uploader': 'taigabot',
        'text': text
    }
    res = requests.post('https://taiga.link/p/upload', headers=HEADERS, data=data)
    return res.text


# leaving this one here in case taigalink dies
def paste_pastebin(text, title='Paste', config={}):
    # sadly we need to pass bot.config because of the api keys
    api_key = config.get('api_keys', {}).get('pastebin', False)

    if api_key is False:
        return "no api key found, pls fix config"

    data = {
        'api_dev_key': api_key,
        'api_option': 'paste',
        'api_paste_code': text,
        'api_paste_name': title,
        'api_paste_private': 1,
        'api_paste_expire_date': '1D',
    }

    response = requests.post('https://pastebin.com/api/api_post.php', headers={'User-Agent': fake_ua}, data=data, timeout=12, allow_redirects=True)
    return response.text


def shorten_taigalink(url):
    data = {
        'title': title,
        'uploader': 'taigabot',
        'text': text
    }
    res = requests.post('https://taiga.link/s/short', headers={'User-Agent': 'taigabot'}, data=data)
    return res.text


# upload any text to pastebin
# please use this function so you don't have to modify 40 plugins when the api changes
def paste(text, title='Paste'):  # paste(*args, **kwargs)?
    return paste_taigalink(text, title)


def shorten(url):
    return shorten_taigalink(url)
