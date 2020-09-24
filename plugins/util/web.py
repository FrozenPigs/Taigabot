""" web.py - handy functions for web services """

import urlnorm
import requests


class ShortenError(Exception):
    def __init__(self, code, text):
        self.code = code
        self.text = text

    def __str__(self):
        return self.text


def isgd(url):
    """ shortens a URL with the is.gd API """
    url = urlnorm.normalize(url.encode('utf-8'), assume_scheme='http')
    req = requests.get("http://is.gd/create.php", params={'format': 'json', 'url': url})

    try:
        json = req.json()
    except ValueError:
        print "[!] ERROR: is.gd returned broken json"
        raise

    if "errorcode" in json:
        raise ShortenError(json["errorcode"], json["errormessage"])
    else:
        return json["shorturl"]


def try_isgd(url):
    return isgd(url)


def haste(text, ext='txt'):
    """ pastes text to a hastebin server """
    req = requests.post("https://hastebin.com/documents", data=text)

    if req.status_code >= 500 and req.status_code < 600:
        print "[!] ERROR: hastebin is down"
        return "(error: hastebin is down)"

    try:
        data = req.json()
        return "https://hastebin.com/raw/{}.{}".format(data['key'], ext)
    except ValueError:
        print "[!] ERROR: hastebin returned invalid json"
        return "(error: hastebin is broken)"


def query(query, params={}):
    print "[!] ERROR: yql is unavailable but being called"
    return None
