import requests
from json import loads as json_load
from urllib import quote
# TODO python 3: from urllib.parse import quote

# this needs to be kept updated (a few times a year is fine)
fake_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138'


def urlencode(inp):
    def force_decode(string):
        for i in ['utf8', 'cp1252']:
            try:
                return string.decode(i)
            except UnicodeDecodeError:
                pass

    if isinstance(inp, str):
        inp = force_decode(inp)

    return quote(inp.encode('utf8'))


def get_json(url, **kwargs):
    return json_load(get_text(url, **kwargs))


def get_html(url, **kwargs):
    return get(url, **kwargs)


def get_text(url, **kwargs):
    return get(url, **kwargs)


def get(url, **kwargs):
    # accept custom headers
    if 'headers' in kwargs:
        headers = kwargs.pop('headers')
        # set a default user-agent if none was set
        if 'User-Agent' not in headers:
            headers['User-Agent'] = fake_ua
    else:
        headers = {'User-Agent': fake_ua}

    r = requests.get(url, headers=headers, timeout=10, **kwargs)
    return r.text
