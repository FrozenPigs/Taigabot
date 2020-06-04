# fuck my life plugin by ine (2020)
from util import hook
from utilities import request
from bs4 import BeautifulSoup

cache = []


def refresh_cache():
    print "[+] refreshing fmylife cache"
    html = request.get('https://www.fmylife.com/random')
    soup = BeautifulSoup(html, 'lxml')
    posts = soup.find_all('a', attrs={'class': 'article-link'})

    for post in posts:
        id = post['href'].split('_')[1].split('.')[0]
        text = post.text.strip()
        cache.append((id, text))


@hook.command(autohelp=False)
def fml(inp):
    "fml -- Gets a random quote from fmyfife.com."

    if len(cache) < 2:
        refresh_cache()

    id, text = cache.pop()
    return '(#{}) {}'.format(id, text)


refresh_cache()
