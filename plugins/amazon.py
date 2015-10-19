from util import hook, http, text, web
import json
import re

## CONSTANTS
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
trans_table = ''.join( [chr(i) for i in range(128)] + ['?'] * 128 )

AMAZON_RE = (r"(http.*(www\.)?amazon\.com/[^ ]+)", re.I)

## HOOK FUNCTIONS

@hook.regex(*AMAZON_RE)
def amazon_url(match):
    item = http.get_html(match.group(1))
    title = item.xpath('//title/text()')[0]
    try: price = item.xpath("//span[@id='priceblock_ourprice']/text()")[0]
    except: price = "$?"
    rating = item.xpath("//div[@id='avgRating']/span/text()")[0].strip()

    star_count = round(float(rating.split(' ')[0]),0)
    stars=""
    for x in xrange(0,int(star_count)):
        stars = "{}{}".format(stars,'★')
    for y in xrange(int(star_count),5):
        stars = "{}{}".format(stars,'☆')

    try: return ('\x02{}\x02 - \x02{}\x02 - \x034{}\x034'.format(title, stars, price)).decode('utf-8')
    except: return http.process_text('\x02{}\x02 - \x02{}\x02 - \x034{}\x034'.format(title, stars, price))


@hook.command('az')
@hook.command
def amazon(inp):
    """az [query] -- Searches amazon for query"""
    href = "http://www.amazon.com/s/url=search-alias%3Daps&field-keywords={}".format(inp.replace(" ","%20"))
    results = http.get_html(href)
    # title = results.xpath('//title/text()')[0]
    try:
        title = results.xpath("//li[@id='result_0']/div/div/div/div/div/a/h2/text()")[0]
        url = results.xpath("//li[@id='result_0']/div/div/div/div/div/a/@href")[0]
        price = results.xpath("//li[@id='result_0']/div/div/div/div/div/div/div/a/span/text()")[0]
        rating = results.xpath("//li[@id='result_0']/div/div/div/div/div/div/div/span/span/a/i/span/text()")[0]
    except:
        title = results.xpath("//li[@id='result_1']/div/div/div/div/div/a/h2/text()")[0]
        url = results.xpath("//li[@id='result_1']/div/div/div/div/div/a/@href")[0]
        price = results.xpath("//li[@id='result_1']/div/div/div/div/div/div/div/a/span/text()")[0]
        rating = results.xpath("//li[@id='result_1']/div/div/div/div/div/div/div/span/span/a/i/span/text()")[0]

    azid = re.match(r'^.*\/dp\/([\w]+)\/.*',url).group(1)

    star_count = round(float(rating.split(' ')[0]),0)
    stars=""
    for x in xrange(0,int(star_count)):
        stars = "{}{}".format(stars,'★')
    for y in xrange(int(star_count),5):
        stars = "{}{}".format(stars,'☆')

    return '\x02{}\x02 - {} - \x034{}\x02 - http://amzn.com/{}'.format(title, stars, price, azid).decode('utf-8')