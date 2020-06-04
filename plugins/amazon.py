# amazon plugin by ine (2020)
from util import hook
from utilities import request
from bs4 import BeautifulSoup
import re


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    container = soup.find(attrs={'data-component-type': 's-search-results'})
    if container is None:
        return []

    results = container.find_all(attrs={'data-component-type': 's-search-result'})

    if len(results) == 0:
        return []

    links = []
    for result in results:
        title = result.find('h2')
        price = result.find('span', attrs={'class': 'a-offscreen'})

        if title is None or price is None:
            continue

        id = result['data-asin']
        title = title.text.strip()
        price = price.text.strip()
        url = 'https://www.amazon.com/dp/' + id + '/'

        # avoids spam if they change urls in the future
        if len(id) > 20:
            continue

        links.append((title, price, url))

    return links


def parse_product(html):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find(id='productTitle')
    price = soup.find(id='priceblock_ourprice')

    if title is None:
        title = soup.find('title')

        if title is None:
            title = 'Untitled'

        title = title.text.replace('Amazon.com: ', '')
    else:
        title = title.text.strip()

    if price is None:
        price = 'various prices'
    else:
        price = price.text.strip()

    return title, price


@hook.command
def amazon(inp):
    """amazon [query] -- Searches amazon for query"""
    if not inp:
        return "usage: amazon <search>"

    inp = request.urlencode(inp)
    html = request.get('https://www.amazon.com/s?k=' + inp)
    results = parse(html)

    if len(results) == 0:
        return 'No results found'

    title, price, url = results[0]

    if len(title) > 80:
        title = title[:80] + '...'

    # \x03 = color, 03 = green
    return u'[Amazon] {} \x0303{}\x03 {}'.format(title, price, url)


AMAZON_RE = (r"https?:\/\/(www\.)?amazon.com\/[^\s]*dp\/([A-Za-z0-9]+)[^\s]*", re.I)


@hook.regex(*AMAZON_RE)
def amazon_url(match):
    id = match.group(2).strip()
    url = 'https://www.amazon.com/dp/' + id + '/'
    html = request.get(url)
    title, price = parse_product(html)

    if len(title) > 80:
        title = title[:80] + '...'

    return u'[Amazon] {} \x0303{}\x03 {}'.format(title, price, url)
