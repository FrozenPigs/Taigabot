from util import hook, http
import re
import requests
import lxml
from lxml.html import parse 

import urllib, urllib2
import HTMLParser
from bs4 import BeautifulSoup

processed = False

link_re = (r'((https?://([-\w\.]+)+(:\d+)?(/([\S/_\.]*(\?\S+)?)?)?))', re.I)
fourchan_quote_re = (r'>>(\D\/\d+)', re.I)
#reddit_re = (r'.*((www\.)?reddit\.com/r[^ ]+)', re.I)
#fourchan_re = (r'.*((boards\.)?4chan\.org/[a-z]/res/[^ ]+)', re.I)
#fourchanquote_re = (r'.*((boards\.)?4chan\.org/[a-z]/res/(\d+)#p(\d+))', re.I)

@hook.regex(*link_re)
def process_url(match,bot=None):
    url = match.group(1)
    try: disabled_channel_commands = bot.channelconfig[input.chan.lower()]['disabled_commands']
    except: disabled_channel_commands = " "
    if 'parsers' in bot.config.get('disabled_commands', []): return None

    if   'youtube.com'      in url: return                         #handled by youtube plugin: exiting
    elif 'youtu.be'         in url: return                         #handled by youtube plugin: exiting
    elif 'yooouuutuuube'    in url: return                         #handled by youtube plugin: exiting
    elif 'vimeo.com'        in url: return                         #handled by vimeo plugin: exiting
    elif 'reddit.com/r'     in url: return reddit_url(url)         #Reddit
    elif 'craigslist.org'   in url: return craigslist_url(url)     #Craigslist
    elif 'boards.4chan.org' in url:                                #4chan
        if '4chan.org/b/'   in url: return '\x033>/b/\x03'
        if '#p'             in url: return fourchanquote_url(url)  #4chan Quoted Post
        else:                       return fourchan_url(url)       #4chan OP
    else:                           return unmatched_url(url)      #process other url


@hook.regex(*fourchan_quote_re)
def process_fourchan_quote(inp):
    url = 'http://boards.4chan.org/%s/res/%s' % (inp.group(0).split('/')[0].replace('>>',''),inp.group(0).split('/')[1])
    if '#p' in url: return fourchanquote_url(url)  #4chan Quoted Post
    else: return fourchan_url(url)
    

#@hook.regex(*reddit_re)
def reddit_url(match):
    # match.group(0)
    thread = http.get_html(match)
    title = thread.xpath('//title/text()')[0]
    upvotes = thread.xpath("//span[@class='upvotes']/span[@class='number']/text()")[0]
    downvotes = thread.xpath("//span[@class='downvotes']/span[@class='number']/text()")[0]
    author = thread.xpath("//div[@id='siteTable']//a[contains(@class,'author')]/text()")[0]
    timeago = thread.xpath("//div[@id='siteTable']//p[@class='tagline']/time/text()")[0]
    comments = thread.xpath("//div[@id='siteTable']//a[@class='comments']/text()")[0]

    return '\x02%s\x02 - posted by \x02%s\x02 %s ago - %s upvotes, %s downvotes - %s' % (
            title, author, timeago, upvotes, downvotes, comments)

#@hook.regex(*fourchan_re)
def fourchan_url(match):
    soup = http.get_soup(match)
    title = soup.title.renderContents().strip()
    post = soup.find('div', {'class': 'opContainer'})
    comment = post.find('blockquote', {'class': 'postMessage'})
    author = post.find_all('span', {'class': 'nameBlock'})[1]
    return http.process_text('\x02%s\x02 - posted by \x02%s\x02: %s' % (title, author, comment[:150]))


#@hook.regex(*fourchanquote_re)
def fourchanquote_url(match):
    postid = match.split('#')[1]
    soup = http.get_soup(match)
    title = soup.title.renderContents().strip()
    post = soup.find('div', {'id': postid})
    comment = post.find('blockquote', {'class': 'postMessage'}).renderContents().strip()
    #comment = re.sub('&gt;&gt;\d*[\s]','',comment) #remove quoted posts
    #comment = re.sub('(&gt;&gt;\d*)','',comment)
    #comment = re.sub('[\|\s]{2,50}','',comment) #remove multiple | | | |
    #comment = re.sub('[\s]{3,}','  ',comment) #remove multiple spaces
    author = post.find_all('span', {'class': 'nameBlock'})[1].renderContents().strip()
    return http.process_text('\x02%s\x02 - posted by \x02%s\x02: %s' % (title, author, comment[:150]))


def craigslist_url(match):
    soup = http.get_soup(match)
    title = soup.find('h2', {'class': 'postingtitle'}).renderContents().strip()
    post = soup.find('section', {'id': 'postingbody'}).renderContents().strip()
    return http.process_text('\x02Craigslist.org: %s\x02 - %s' % (title, post[:150]))


def unmatched_url(match):
    content_type = None
    length = None
    title = None
    result = None
    page = urllib.urlopen(match)
    content_type = page.info()['Content-Type'].split(';')[0]
    if content_type.find("html") != -1:
      soup = BeautifulSoup(page)
      title = soup.title.renderContents().strip()
      if len(title) > 300: title = soup.find('meta', {'name' : 'description'})['content']
    elif content_type.find("image") != -1:
      if page.info()['Content-Length']:
        length = int(page.info()['Content-Length'])
        if length > 1048576: length = str(length / 1048576) + ' MiB'
        elif length > 1024: length = str(length / 1024) + ' KiB'
        elif length < 0: length = 'Unknown size'
        else: length = str(length) + ' B'
      else: length = "Unknown size"
    else: title = "I messed up. Bad."

    result = ''
    if length != None:
      result += ('[%s] %s ' % (content_type, length))
    if title != None:
      result += ('%s' % (title)) 

    return ('%s' % (http.process_text(result)))