from urllib import quote
import requests
from json import loads as json_load

fake_ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3745.0 Safari/537.36'


def urlencode(inp):
    def force_decode(string, codecs=['utf8', 'cp1252']):
        for i in codecs:
            try:
                return string.decode(i)
            except UnicodeDecodeError:
                pass

    if isinstance(inp, str):
        inp = force_decode(inp)

    return quote(inp.encode('utf8'))


def get_json(url):
    return json_load(get_text(url))


def get_html(url):
    return get_text(url)


def get_text(url):
    headers = {'User-Agent': fake_ua}
    r = requests.get(url, headers=headers)
    return r.text
