from util import hook, http, database, urlnorm
from bs4 import BeautifulSoup
import re

from urllib import FancyURLopener
from bs4 import BeautifulSoup
class urlopener(FancyURLopener):
    version = "Mozilla/5.0 (X11; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1"

opener = urlopener()

link_re = (r'((https?://([-\w\.]+)+(:\d+)?(/([\S/_\.]*(\?\S+)?)?)?))', re.I)

@hook.regex(*link_re)
def process_url(match,bot=None,input=None,chan=None,db=None, say=None):
    global trimlength
    url = match.group(1).replace('https:','http:')
 
    #disabled_commands = database.get(db,'channels','disabled','chan',chan)
    #if disabled_commands and 'parsers' not in disabled_commands: return None

    # print disabled_commands
    # if not disabled_commands: disabled_commands = ''

    trimlength = database.get(db,'channels','trimlength','chan',chan)
    if not trimlength: trimlength = 9999
    try: trimlength = int(trimlength)
    except: trimlength = trimlength


    if   'youtube.com'       in url: return                         #handled by youtube plugin: exiting
    elif 'youtu.be'          in url: return                         #handled by youtube plugin: exiting
    elif 'yooouuutuuube'     in url: return                         #handled by youtube plugin: exiting
    elif 'vimeo.com'         in url: return                         #handled by vimeo plugin: exiting
    elif 'newegg.com'        in url: return                         #handled by newegg plugin: exiting
    elif 'amazon.com'        in url: return                         #handled by Amazon plugin: exiting
    elif 'reddit.com/r'      in url: return                         #handled by Reddit plugin: exiting
    elif 'hulu.com'          in url: return                         #handled by hulu plugin: exiting
    elif 'imdb.com'          in url: return                         #handled by imbd plugin: exiting
    elif 'soundcloud.com'    in url: return                         #handled by soundcloud plugin: exiting
    elif 'spotify.com'       in url: return                         #handled by Spotify plugin: exiting
    elif 'simg.gelbooru.com' in url: return unmatched_url(url)      #handled by Gelbooru plugin: exiting
    elif 'gelbooru.com'      in url: return                         #handled by Gelbooru plugin: exiting
    elif 'craigslist.org'    in url: return craigslist_url(url)     #Craigslist
    elif 'ebay.com'          in url: return ebay_url(url)           #Ebay
    elif 'wikipedia.org'     in url: return wikipedia_url(url)      #Wikipedia
    elif 'boards.4chan.org'  in url:                                #4chan
        if '4chan.org/b/'    in url: say('\x033>/b/\x03')
        if '#p'              in url: return fourchanquote_url(url)  #4chan Quoted Post
        if '/res/'           in url: return fourchanpost_url(url)   #4chan Post
        if '/src/'           in url: return unmatched_url(url)      #4chan Image
        else:                        return fourchanboard_url(url)  #4chan Board
    else:                            return unmatched_url(url)      #process other url


#@hook.regex(*fourchan_re)
def fourchanboard_url(match):
    soup = http.get_soup(match)
    title = soup.title.renderContents().strip()
    return http.process_text("\x02{}\x02".format(title[:trimlength]))


#fourchan_re = (r'.*((boards\.)?4chan\.org/[a-z]/res/[^ ]+)', re.I)
#@hook.regex(*fourchan_re)
def fourchanpost_url(match):
    soup = http.get_soup(match)
    title = soup.title.renderContents().strip()
    post = soup.find('div', {'class': 'opContainer'})
    comment = post.find('blockquote', {'class': 'postMessage'}).renderContents().strip()
    author = post.find_all('span', {'class': 'nameBlock'})[1]
    return http.process_text("\x02{}\x02 - posted by \x02{}\x02: {}".format(title, author, comment[:trimlength]))


# .replace('boards.4chan.org', 'a.4cdn.org')
# result = http.get_soup("http://m.hulu.com/search?dp_identifier=hulu&{}&items_per_page=1&page=1".format(urlencode({'query': inp})))
    # data = result.find('results').find('videos').find('video')
    # showname = data.find('show').find('name').text
    # title = data.find('title').text
    # duration = timeformat.format_time(int(float(data.find('duration').text)))
    # description = data.find('description').text
    # rating = data.find('rating').text
    # return "\x02{}:\x02 {} - {} - {} \x02({})\x02 {}".format(showname, title, description, duration, rating, "http://www.hulu.com/watch/" + str(data.find('id').text))


#fourchan_quote_re = (r'>>(\D\/\d+)', re.I)
#fourchanquote_re = (r'.*((boards\.)?4chan\.org/[a-z]/res/(\d+)#p(\d+))', re.I)
#@hook.regex(*fourchanquote_re)
def fourchanquote_url(match):
    postid = match.split('#')[1]
    soup = http.get_soup(match)
    title = soup.title.renderContents().strip()
    post = soup.find('div', {'id': postid})
    comment = post.find('blockquote', {'class': 'postMessage'}).renderContents().strip()
    author = post.find_all('span', {'class': 'nameBlock'})[1].renderContents().strip()
    return http.process_text("\x02{}\x02 - posted by \x02{}\x02: {}".format(title, author, comment[:trimlength]))


def craigslist_url(match):
    soup = http.get_soup(match)
    title = soup.find('h2', {'class': 'postingtitle'}).renderContents().strip()
    post = soup.find('section', {'id': 'postingbody'}).renderContents().strip()
    return http.process_text("\x02Craigslist.org: {}\x02 - {}".format(title, post[:trimlength]))


def ebay_url(match):
    item = http.get_html(match)
    title = item.xpath("//h1[@id='itemTitle']/text()")[0].strip()
    try: price = item.xpath("//span[@id='prcIsum_bidPrice']/text()")[0].strip()
    except: price = item.xpath("//span[@id='prcIsum']/text()")[0].strip()
    try: bids = item.xpath("//span[@id='qty-test']/text()")[0].strip()
    except: bids = "Buy It Now"
    feedback = item.xpath("//span[@class='w2b-head']/text()")[0].strip()

    return http.process_text("\x02{}\x02 - \x02{}\x02 - Bids: {} - Feedback: {}".format(title, price, bids, feedback))
    #url = 'http://open.api.ebay.com/shopping?callname=GetSingleItem&responseencoding=JSON&appid=YourAppIDHere&siteid=0&version=515&ItemID={}'
    #timeleft = item.xpath("//span[@id='bb_tlft']/span/text()")[0].strip()
    #shipping = item.xpath("//span[@id='fshippingCost']/text()")[0].strip()


def wikipedia_url(match):
    soup = http.get_soup(match)
    title = soup.find('h1', {'id': 'firstHeading'}).renderContents().strip()
    post = soup.find('p').renderContents().strip().replace('\n','').replace('\r','')
    return http.process_text("\x02Wikipedia.org: {}\x02 - {}...".format(title,post[:trimlength]))


def unmatched_url(match):
    content_type = None
    length = None
    title = None
    result = None
    page = opener.open(match) #urllib.urlopen(match)

    try: content_type = page.info()['Content-Type'].split(';')[0]
    except: return

    if content_type.find("html") != -1:
        soup = BeautifulSoup(page)
        try: title = soup.title.renderContents().strip()
        except: return
        #if len(title) > 300: title = soup.find('meta', {'name' : 'description'})['content']
        if not title: return #"Could not find title."
        return http.process_text("{}".format(title[:trimlength]))
    else:
        if page.info()['Content-Length']:
            length = int(page.info()['Content-Length'])
            if length > 1048576: length = str("{0:.2f}".format(round((float(length) / 1048576),2))) + ' MiB'
            elif length > 1024: length = str("{0:.2f}".format(round((float(length) / 1024),2))) + ' KiB'
            elif length < 0: length = 'Unknown size'
            else: length = str(length) + ' B'
        else: 
            length = "Unknown size"

        if length != None: return u"[{}] {}".format(content_type, length)

