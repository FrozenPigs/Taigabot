import md5
import re
import urllib
import urllib2
from urllib import FancyURLopener
from urlparse import urlparse

import requests
from lxml import html

import gelbooru
from bs4 import BeautifulSoup
from util import database, formatting, hook, http, urlnorm


class urlopener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'


opener = urlopener()

link_re = (r'((https?://([-\w\.]+)+(:\d+)?(/([\S/_\.]*(\?\S+)?)?)?))', re.I)


@hook.regex(*link_re)
def process_url(match, bot=None, input=None, chan=None, db=None, reply=None):
    global trimlength
    url = match.group(1).replace('https:', 'http:')

    parsed = urlparse(url)
    print parsed
    import ipaddress
    if ':' in parsed.netloc:
        return
    else:
        try:
            if ipaddress.ip_address(parsed.netloc).is_private:
                return
        except ValueError:
            if ':' not in parsed.netloc:
                pass
            else:
                return

    if 'localhost' in url.lower():
        return

    trimlength = database.get(db, 'channels', 'trimlength', 'chan', chan)
    if not trimlength: trimlength = 9999
    try:
        trimlength = int(trimlength)
    except:
        trimlength = trimlength

    if '.html' in url.lower(): return

    if '.onion' in url.lower():
        return
    elif 'youtube.com' in url.lower():
        return    #handled by youtube plugin: exiting
    elif 'youtu.be' in url.lower():
        return    #handled by youtube plugin: exiting
    elif 'yooouuutuuube' in url.lower():
        return    #handled by youtube plugin: exiting
    elif 'vimeo.com' in url.lower():
        return    #handled by vimeo plugin: exiting
    elif 'newegg.com' in url.lower():
        return    #handled by newegg plugin: exiting
    elif 'amazon.com' in url.lower():
        return    #handled by Amazon plugin: exiting
#    elif 'reddit.com/r' in url.lower():
#        return  #handled by Reddit plugin: exiting
    elif 'hulu.com' in url.lower():
        return    #handled by hulu plugin: exiting
    elif 'imdb.com' in url.lower():
        return    #handled by imbd plugin: exiting
    elif 'soundcloud.com' in url.lower():
        return    #handled by soundcloud plugin: exiting
    elif 'spotify.com' in url.lower():
        return    #handled by Spotify plugin: exiting
    elif 'twitch.tv' in url.lower():
        return    #handled by Twitch plugin: exiting
    elif 'twitter.com' in url.lower():
        return    #handled by Twitter plugin: exiting
    elif 'simg.gelbooru.com' in url.lower():
        return unmatched_url(url)    #handled by Gelbooru plugin: exiting
    elif 'gelbooru.com' in url.lower():
        return    #handled by Gelbooru plugin: exiting
    elif 'craigslist.org' in url.lower():
        return craigslist_url(url)    #Craigslist
    elif 'ebay.com' in url.lower():
        return ebay_url(url, bot)    #Ebay
    elif 'wikipedia.org' in url.lower():
        return wikipedia_url(url)    #Wikipedia
    elif 'hentai.org' in url.lower():
        return hentai_url(url, bot)    #Hentai
    elif 'boards.4chan.org' in url.lower():    #4chan
        if '4chan.org/b/' in url.lower(): reply('\x033>/b/\x03')
        if '#p' in url.lower():
            return fourchanquote_url(url)    #4chan Quoted Post
        if '/thread/' in url.lower():
            return fourchanthread_url(url)    #4chan Post
        if '/res/' in url.lower():
            return fourchanthread_url(url)    #4chan Post
        if '/src/' in url.lower(): return unmatched_url(url)    #4chan Image
        else: return fourchanboard_url(url)    #4chan Board
    else: return unmatched_url(url, chan, db)    #process other url


#@hook.regex(*fourchan_re)
def fourchanboard_url(match):
    soup = http.get_soup(match)
    title = soup.title.renderContents().strip()
    return http.process_text("\x02{}\x02".format(title[:trimlength]))


#fourchan_re = (r'.*((boards\.)?4chan\.org/[a-z]/res/[^ ]+)', re.I)
#@hook.regex(*fourchan_re)
def fourchanthread_url(match):
    soup = http.get_soup(match)
    title = soup.title.renderContents().strip()
    post = soup.find('div', {'class': 'opContainer'})
    comment = post.find('blockquote', {
        'class': 'postMessage'
    }).renderContents().strip()
    author = post.find_all('span', {'class': 'nameBlock'})[1]
    return http.process_text("\x02{}\x02 - posted by \x02{}\x02: {}".format(
        title, author, comment[:trimlength]))


#fourchan_quote_re = (r'>>(\D\/\d+)', re.I)
#fourchanquote_re = (r'.*((boards\.)?4chan\.org/[a-z]/res/(\d+)#p(\d+))', re.I)
#@hook.regex(*fourchanquote_re)
def fourchanquote_url(match):
    postid = match.split('#')[1]
    soup = http.get_soup(match)
    title = soup.title.renderContents().strip()
    post = soup.find('div', {'id': postid})
    comment = post.find('blockquote', {
        'class': 'postMessage'
    }).renderContents().strip()
    author = post.find_all('span', {'class': 'nameBlock'})[1].renderContents(
    ).strip()
    return http.process_text("\x02{}\x02 - posted by \x02{}\x02: {}".format(
        title, author, comment[:trimlength]))


def craigslist_url(match):
    soup = http.get_soup(match)
    title = soup.find('h2', {
        'class': 'postingtitle'
    }).renderContents().strip()
    post = soup.find('section', {
        'id': 'postingbody'
    }).renderContents().strip()
    return http.process_text("\x02Craigslist.org: {}\x02 - {}".format(
        title, post[:trimlength]))


# ebay_item_re = r'http:.+ebay.com/.+/(\d+).+'
def ebay_url(match, bot):
    apikey = bot.config.get("api_keys", {}).get("ebay")
    # if apikey:
    #     # ebay_item_re = (r'http:.+ebay.com/.+/(\d+).+', re.I)
    #     itemid = re.match('http:.+ebay.com/.+/(\d+).+',match, re.I)
    #     url = 'http://open.api.ebay.com/shopping?callname=GetSingleItem&responseencoding=JSON&appid={}&siteid=0&version=515&ItemID={}&IncludeSelector=Description,ItemSpecifics'.format(apikey,itemid.group(1))
    #     print url

    # else:
    print "No eBay api key set."
    item = http.get_html(match)
    title = item.xpath("//h1[@id='itemTitle']/text()")[0].strip()
    price = item.xpath("//span[@id='prcIsum_bidPrice']/text()")
    if not price: price = item.xpath("//span[@id='prcIsum']/text()")
    if not price: price = item.xpath("//span[@id='mm-saleDscPrc']/text()")
    if price: price = price[0].strip()
    else: price = '?'

    try:
        bids = item.xpath("//span[@id='qty-test']/text()")[0].strip()
    except:
        bids = "Buy It Now"

    feedback = item.xpath("//span[@class='w2b-head']/text()")
    if not feedback: feedback = item.xpath("//div[@id='si-fb']/text()")
    if feedback: feedback = feedback[0].strip()
    else: feedback = '?'

    return http.process_text(
        "\x02{}\x02 - \x02\x033{}\x03\x02 - Bids: {} - Feedback: {}".format(
            title, price, bids, feedback))

    # url = 'http://open.api.ebay.com/shopping?callname=GetSingleItem&responseencoding=JSON&appid=YourAppIDHere&siteid=0&version=515&ItemID={}&IncludeSelector=Description,ItemSpecifics'.format(itemid)

    #url = 'http://open.api.ebay.com/shopping?callname=GetSingleItem&responseencoding=JSON&appid=YourAppIDHere&siteid=0&version=515&ItemID={}'
    #timeleft = item.xpath("//span[@id='bb_tlft']/span/text()")[0].strip()
    #shipping = item.xpath("//span[@id='fshippingCost']/text()")[0].strip()


def wikipedia_url(match):
    soup = http.get_soup(match)
    title = soup.find('h1', {'id': 'firstHeading'}).renderContents().strip()
    post = soup.find('p').renderContents().strip().replace('\n', '').replace(
        '\r', '')
    return http.process_text("\x02Wikipedia.org: {}\x02 - {}...".format(
        title, post[:trimlength]))


# hentai_re = (r'(http.+hentai.org/.+)', re.I)
# @hook.regex(*hentai_re)
def hentai_url(match, bot):
    userpass = bot.config.get("api_keys", {}).get("exhentai")
    if "user:pass" in userpass:
        return
    else:
        username = userpass.split(':')[0]
        password = userpass.split(':')[1]
        if not username or not password:
            return    #"error: no username/password set"

    url = match
    loginurl = 'http://forums.e-hentai.org/index.php?act=Login&CODE=01'
    logindata = 'referer=http://forums.e-hentai.org/index.php&UserName={}&PassWord={}&CookieDate=1'.format(
        username, password)

    req = urllib2.Request(loginurl)
    resp = urllib2.urlopen(req, logindata)    #POST
    coo = resp.info().getheader('Set-Cookie')    #  cookie
    cooid = re.findall('ipb_member_id=(.*?);', coo)[0]
    coopw = re.findall('ipb_pass_hash=(.*?);', coo)[0]

    headers = {
        'Cookie':
        'ipb_member_id=' + cooid + ';ipb_pass_hash=' + coopw,
        'User-Agent':
        "User-Agent':'Mozilla/5.2 (compatible; MSIE 8.0; Windows NT 6.2;)"
    }

    request = urllib2.Request(url, None, headers)
    page = urllib2.urlopen(request).read()
    soup = BeautifulSoup(page)
    try:
        title = soup.find('h1', {'id': 'gn'}).string
        date = soup.find('td', {'class': 'gdt2'}).string
        rating = soup.find('td', {
            'id': 'rating_label'
        }).string.replace('Average: ', '')
        star_count = round(float(rating), 0)
        stars = ""
        for x in xrange(0, int(star_count)):
            stars = "{}{}".format(stars, ' ')
        for y in xrange(int(star_count), 5):
            stars = "{}{}".format(stars, ' ')

        return '\x02{}\x02 - \x02\x034{}\x03\x02 - {}'.format(
            title, stars, date).decode('utf-8')
    except:
        return u'{}'.format(soup.title.string)


# amiami, hobby search and nippon yasan

user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0'
# cookies = dict(cookies_are='working')
cookies = dict()
headers = {'User-Agent': user_agent, 'Cookie': ''}


def unmatched_url(match, chan, db):
    disabled_commands = database.get(db, 'channels', 'disabled', 'chan', chan)

    try:
        r = requests.get(
            match, headers=headers, allow_redirects=True, stream=True)
    except Exception as e:
        print e
        return formatting.output('URL', ['Error: {}'.format(e)])

    domain = urlparse(match).netloc

    if r.status_code != 404:
        content_type = r.headers['Content-Type']
        try:
            encoding = r.headers['content-encoding']
        except:
            encoding = ''

        if content_type.find(
                "html") != -1:    # and content_type is not 'gzip':
            data = ''
            for chunk in r.iter_content(chunk_size=1024):
                data += chunk
                if len(data) > 48336: break

            body = html.fromstring(data)
            try:
                title = body.xpath('//title/text()')[0]
            except:
                return formatting.output('URL', [
                    'No Title ({})'.format(domain)
                ])

            try:
                title_formatted = text.fix_bad_unicode(
                    body.xpath('//title/text()')[0])
            except:
                title_formatted = body.xpath('//title/text()')[0]
            return formatting.output('URL', [
                '{} ({})'.format(title_formatted.encode('utf-8'), domain)
            ]).strip()
        else:
            if disabled_commands:
                if 'filesize' in disabled_commands: return
            try:
                if r.headers['Content-Length']:
                    length = int(r.headers['Content-Length'])
                    if length < 0: length = 'Unknown size'
                    else: length = formatting.filesize(length)
                else:
                    length = "Unknown size"
            except:
                length = "Unknown size"
            if "503 B" in length: length = ""
            if length is None: length = ""
            return formatting.output('URL', [
                '{} Size: {} ({})'.format(content_type, length, domain)
            ])
    return
