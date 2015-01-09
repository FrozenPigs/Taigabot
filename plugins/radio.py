import re
from util import hook, http, web, text
import lxml.html

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
def radio(inp, conn=None, chan=None, say=False):
    eden_result = eden(inp)
    radio_result = aradio(inp)
    out = "PRIVMSG %s :%s" % (chan, eden_result)
    conn.send(out)
    out = "PRIVMSG %s :%s" % (chan, radio_result)
    conn.send(out)
