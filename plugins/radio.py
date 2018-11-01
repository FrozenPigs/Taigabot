import re
from util import hook, http, web, text
import lxml.html
import lxml
import urllib2
import urllib
from bs4 import BeautifulSoup

@hook.command(autohelp=False)
def eden(inp, say=False):
    "eden [url]-- Returns current eden song"
    url = 'http://www.edenofthewest.com/'
    if 'url' in inp: return url+'edennew/'
    tree = lxml.html.parse(url)
    dj = tree.xpath("//div[@id='status-dj']/text()")[0]
    song = tree.xpath("//div[@id='status-current-song']/text()")[0]
    listeners = tree.xpath("//div[@id='status-listeners']/text()")[0]
    try: song_formatted = text.fix_bad_unicode(song)
    except: song_formatted = song
    return "[Eden] (%s) \x02%s\x02 : %s" % (listeners, dj, song_formatted)


@hook.command(autohelp=False)
def aradio(inp, say=False):
    "radio [url]-- Returns current r/a/dio song"
    url = 'http://r-a-d.io/'
    if 'url' in inp: return url
    tree = lxml.html.parse(url)
    dj = tree.xpath("//h4[@id='dj-name']/text()")[0]
    song = re.sub('\s+',' ',tree.xpath(".//h2[@id='current-song']/span/text()")[0])
    listeners = tree.xpath("//span[@id='listeners']/text()")[0]
    try: song_formatted = text.fix_bad_unicode(song)
    except: song_formatted = song
    return "[R/a/dio] (%s) \x02%s\x02 : %s" % (listeners, dj, song_formatted)


@hook.command(autohelp=False)
@hook.command('mutantradio', autohelp=False)
def muradio(inp, say=False):
    "radio [url]-- Returns current mutantradio song"
    url = 'https://chiru.no:8080/status.xsl'
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page, 'lxml')
    stats = soup.find_all('td', 'streamstats')
    for i in stats:
        print i
    print stats[2], stats[4], stats[5]
    listeners = stats[2].text
    genre = stats[4].text
    url = stats[5].text
    song = stats[6].text.encode('utf-8').strip()
    try:
        page2 = urllib2.urlopen('http://chiru.no:8080/live.mp3').read()
        return "[muradio] Playing: {}, Genre: {}, Listening: {}, URL: http://mutantradio.ga".format(song, genre, listeners)
    except:
        return "[muradio] Playing: {}, Genre: {}, Listening: {}, URL: {}".format(song, genre, listeners, url)
    #if 'url' in inp: return url
    #tree = lxml.html.parse(url)
    #print "hi"
    #print dir(tree.getroot())
    ##dj = tree.xpath("//h4[@id='dj-name']/text()")[0]
    #song = tree.getroot().find("//td[@class='streamstats']/text()")[0]
    ##listeners = tree.xpath("//span[@id='listeners']/text()")[0]
    #try: song_formatted = text.fix_bad_unicode(song)
    #except: song_formatted = song
    ##return "[R/a/dio] (%s) \x02%s\x02 : %s" % (listeners, dj, song_formatted)
    #return "[muradio] %s" % (song_formatted)


@hook.command(autohelp=False)
def radio(inp, conn=None, chan=None, say=False):
    eden_result = eden(inp)
    radio_result = aradio(inp)
    out = "PRIVMSG %s :%s" % (chan, eden_result)
    conn.send(out)
    out = "PRIVMSG %s :%s" % (chan, radio_result)
    conn.send(out)
