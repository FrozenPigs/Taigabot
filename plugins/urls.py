import re
import urllib2
from urlparse import urlparse

import requests
from bs4 import BeautifulSoup
from lxml import html

from util import database, formatting, hook, http

MAX_LENGTH = 200
trimlength = 320

IGNORED_HOSTS = [
    '.onion',
    'localhost',
    # these are handled by their respective plugin
    # more info on some other file
    'youtube.com',    # handled by youtube plugin
    'youtu.be',
    'music.youtube.com',
    'vimeo.com',
    'player.vimeo.com',
    'newegg.com',
    'amazon.com',
    # 'reddit.com',
    'hulu.com',
    'imdb.com',
    'soundcloud.com',
    'spotify.com',
    'twitch.tv',
    'twitter.com',

    # handled on mediawiki.py
    'en.wikipedia.org',
    'encyclopediadramatica.wiki',
]

# 'http' + s optional + ':// ' + anything + '.' + anything
LINK_RE = (r'(https?://\S+\.\S*)', re.I)


@hook.regex(*LINK_RE)
def process_url(match, bot=None, chan=None, db=None):
    url = match.group(0)
    parsed = urlparse(url)
    # parsed contains scheme, netloc, path, params, query, fragment

    # skip unwanted hosts
    # most of them are handled somewhere else anyway
    for ignored in IGNORED_HOSTS:
        if ignored in parsed.netloc:
            return

    if 'simg.gelbooru.com' in url.lower():
        return unmatched_url(url, parsed, bot, chan, db)    # handled by Gelbooru plugin: exiting
    elif 'gelbooru.com' in url.lower():
        return    # handled by Gelbooru plugin: exiting
    elif 'craigslist.org' in url.lower():
        return craigslist_url(url)    # Craigslist
    elif 'ebay.com' in url.lower():
        return ebay_url(url, bot)    # Ebay
    elif 'wikipedia.org' in url.lower():
        return wikipedia_url(url)    # Wikipedia
    elif 'hentai.org' in url.lower():
        return hentai_url(url, bot)    # Hentai
    elif 'boards.4chan.org' in url.lower():    # 4chan
        if '4chan.org/b/' in url.lower():
            return '\x033>/b/\x03'
        if '#p' in url.lower():
            return fourchanquote_url(url)    # 4chan Quoted Post
        if '/thread/' in url.lower():
            return fourchanthread_url(url)    # 4chan Post
        if '/res/' in url.lower():
            return fourchanthread_url(url)    # 4chan Post
        if '/src/' in url.lower():
            return unmatched_url(url, parsed, bot, chan, db)    # 4chan Image
        else:
            return fourchanboard_url(url)    # 4chan Board
    else:
        return unmatched_url(url, parsed, bot, chan, db)    # process other url


# @hook.regex(*fourchan_re)
def fourchanboard_url(match):
    soup = http.get_soup(match)
    title = soup.title.renderContents().strip()
    return http.process_text("\x02{}\x02".format(title[:trimlength]))


# fourchan_re = (r'.*((boards\.)?4chan\.org/[a-z]/res/[^ ]+)', re.I)
# @hook.regex(*fourchan_re)
def fourchanthread_url(match):
    soup = http.get_soup(match)
    title = soup.title.renderContents().strip()
    post = soup.find('div', {'class': 'opContainer'})
    comment = post.find('blockquote', {'class': 'postMessage'}).renderContents().strip()
    author = post.find_all('span', {'class': 'nameBlock'})[1]
    return http.process_text("\x02{}\x02 - posted by \x02{}\x02: {}".format(
        title, author, comment[:trimlength]))


# fourchan_quote_re = (r'>>(\D\/\d+)', re.I)
# fourchanquote_re = (r'.*((boards\.)?4chan\.org/[a-z]/res/(\d+)#p(\d+))', re.I)
# @hook.regex(*fourchanquote_re)
def fourchanquote_url(match):
    postid = match.split('#')[1]
    soup = http.get_soup(match)
    title = soup.title.renderContents().strip()
    post = soup.find('div', {'id': postid})
    comment = post.find('blockquote', {'class': 'postMessage'}).renderContents().strip()
    author = post.find_all('span', {'class': 'nameBlock'})[1].renderContents().strip()
    return http.process_text("\x02{}\x02 - posted by \x02{}\x02: {}".format(
        title, author, comment[:trimlength]))


def craigslist_url(match):
    soup = http.get_soup(match)
    title = soup.find('h2', {'class': 'postingtitle'}).renderContents().strip()
    post = soup.find('section', {'id': 'postingbody'}).renderContents().strip()
    return http.process_text("\x02Craigslist.org: {}\x02 - {}".format(title, post[:trimlength]))


# ebay_item_re = r'http:.+ebay.com/.+/(\d+).+'
def ebay_url(match, bot):
    item = http.get_html(match)
    title = item.xpath("//h1[@id='itemTitle']/text()")[0].strip()
    price = item.xpath("//span[@id='prcIsum_bidPrice']/text()")
    if not price:
        price = item.xpath("//span[@id='prcIsum']/text()")
    if not price:
        price = item.xpath("//span[@id='mm-saleDscPrc']/text()")
    if price:
        price = price[0].strip()
    else:
        price = '?'

    try:
        bids = item.xpath("//span[@id='qty-test']/text()")[0].strip()
    except:
        bids = "Buy It Now"

    feedback = item.xpath("//span[@class='w2b-head']/text()")
    if not feedback:
        feedback = item.xpath("//div[@id='si-fb']/text()")
    if feedback:
        feedback = feedback[0].strip()
    else:
        feedback = '?'

    return http.process_text("\x02{}\x02 - \x02\x033{}\x03\x02 - Bids: {} - Feedback: {}".format(
        title, price, bids, feedback))


def wikipedia_url(match):
    soup = http.get_soup(match)
    title = soup.find('h1', {'id': 'firstHeading'}).renderContents().strip()
    post = soup.find('p').renderContents().strip().replace('\n', '').replace('\r', '')
    return http.process_text("\x02Wikipedia.org: {}\x02 - {}...".format(title, post[:trimlength]))


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
            return    # "error: no username/password set"

    url = match
    loginurl = 'http://forums.e-hentai.org/index.php?act=Login&CODE=01'
    logindata = 'referer=http://forums.e-hentai.org/index.php&UserName={}&PassWord={}&CookieDate=1'.format(
        username, password)

    req = urllib2.Request(loginurl)
    resp = urllib2.urlopen(req, logindata)    # POST
    coo = resp.info().getheader('Set-Cookie')    # cookie
    cooid = re.findall('ipb_member_id=(.*?);', coo)[0]
    coopw = re.findall('ipb_pass_hash=(.*?);', coo)[0]

    headers = {
        'Cookie': 'ipb_member_id=' + cooid + ';ipb_pass_hash=' + coopw,
        'User-Agent':
        "User-Agent':'Mozilla/5.2 (compatible; MSIE 8.0; Windows NT 6.2;)",    # wow this code is ass
    }

    request = urllib2.Request(url, None, headers)
    page = urllib2.urlopen(request).read()
    soup = BeautifulSoup(page)
    try:
        title = soup.find('h1', {'id': 'gn'}).string
        date = soup.find('td', {'class': 'gdt2'}).string
        rating = soup.find('td', {'id': 'rating_label'}).string.replace('Average: ', '')
        star_count = round(float(rating), 0)
        stars = ""
        for x in xrange(0, int(star_count)):
            stars = "{}{}".format(stars, ' ')
        for y in xrange(int(star_count), 5):
            stars = "{}{}".format(stars, ' ')

        return '\x02{}\x02 - \x02\x034{}\x03\x02 - {}'.format(title, stars, date).decode('utf-8')
    except:
        return u'{}'.format(soup.title.string)


user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138'
headers = {'User-Agent': user_agent}


def parse_html(stream):
    data = ''
    for chunk in stream.iter_content(chunk_size=256):
        data = data + chunk

        if len(data) > (1024 * 12):    # use only first 12 KiB
            break

    # try to quickly grab the content between <title> and </title>
    # should match most cases, if not just fall back to lxml
    if '<title>' in data and '</title>' in data:
        try:
            quick_title = data[data.find('<title>') + 7:data.find('</title>')]
            return quick_title.strip()
        except Exception as e:
            pass

    parser = html.fromstring(data)

    # try to use the <title> tag first
    title = parser.xpath('//title/text()')
    if not title:
        # fall back to <h1> elements
        title = parser.xpath('//h1/text()')

    if title:
        if type(title) is list and len(title) > 0:
            return title[0].strip()

        elif type(title) is str:
            return title.strip()

    # page definitely has no title
    return 'Untitled'


def unmatched_url(url, parsed, bot, chan, db):
    disabled_commands = database.get(db, 'channels', 'disabled', 'chan', chan) or []

    # don't bother if the channel has url titles disabled
    if 'urltitles' in disabled_commands:
        return

    # fetch, and hide all errors from the output
    try:
        req = requests.get(url, headers=headers, allow_redirects=True, stream=True, timeout=8)
    except Exception as e:
        print '[!] WARNING couldnt fetch url'
        print e
        return

    # parsing
    domain = parsed.netloc
    content_type = req.headers.get('Content-Type', '')
    size = req.headers.get('Content-Length', 0)
    output = ['[URL]']

    if 'html' in content_type:
        try:
            title = parse_html(req)
        except Exception as e:
            print '[!] WARNING the url caused a parser error'
            title = 'Untitled'

        # TODO handle titles with html entities
        if '&' in title and ';' in title:
            # pls fix
            title = title.replace('&quot;', '"')

        # fucking cloudflare
        if 'Attention Required! | Cloudflare' in title:
            return

        output.append(title)

    else:
        if 'filesize' in disabled_commands:
            return

        # very common mime types
        if 'image/' in content_type:
            output.append(content_type.replace('image/', '') + ' image,')
        elif 'video/' in content_type:
            output.append(content_type.replace('video/', '') + ' video,')
        elif 'text/' in content_type:
            output.append('text file,')
        elif 'application/octet-stream' == content_type:
            output.append('binary file,')
        elif 'audio/' in content_type:
            output.append('audio file,')

        # other mime types
        elif 'application/vnd.' in content_type:
            output.append('unknown binary file,')
        elif 'font/' in content_type:
            output.append('font,')

        # i dunno
        else:
            output.append(content_type + ' file,')

        try:
            size = int(size)
        except TypeError:
            size = 0

        # some pages send exactly 503 or 513 bytes of empty padding as an
        # internet explorer 5 and 6 workaround, but since that browser is
        # super dead this should probably be removed.
        # more at https://stackoverflow.com/a/11544049/4301778
        if size == 0 or size == 503 or size == 513:
            output.append('unknown size')
        else:
            output.append('size: ' + formatting.filesize(size))

    # output formatting
    output = ' '.join(output)

    if len(output) > MAX_LENGTH:
        output = output[:MAX_LENGTH] + '...'

    # add domain to the end
    output = "{} ({})".format(output, domain)

    # show error codes if they appear
    if req.status_code >= 400 and req.status_code < 600:
        output = '{} (error {})'.format(output, req.status_code)

    return output
