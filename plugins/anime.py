from util import hook, http
#import urllib, urllib2
#import re
#from bs4 import BeautifulSoup

@hook.command
@hook.command('anime')
def animetake(inp):
    "anime [list|get] <anime name> - Searches Animetake for the latest updates"
    error = u'not so lucky today..'
    try:
        inp_array = inp.split(' ')
        command = inp_array[0]
        query = inp_array[1]
    except:
        pass

    url = "http://www.animetake.com/" #% (urllib.quote_plus(query))
    anime_updates = []
    response = "" 

    soup = http.get_soup(url)
    page = soup.find('div', id='mainContent').ul
 
    for li in page.findAll('li'):
      anime_link = li.find('div', 'updateinfo').h4.a
      anime_updates.append('%s : %s' % (anime_link['title'], anime_link['href']))

    if command == 'list':
      count = 1
      response = "Latest Anime Updates: "       
      for anime_title in anime_updates:
        response += ("%s | " % (anime_title.split(' : ')[0]))
        count+=1
        if count == 11:
          break
    elif command == 'get':
      indices = [i for i, x in enumerate(anime_updates) if query in x]
      for index in indices:
        response += ("%s " % (anime_updates[index]))
    return response



@hook.command
def nyaa(inp):
    "nyaa <query> - NYAA Search"
    search_url = 'http://nyaa.eu/?term=%s' % (inp.replace(' ','+'))
    return u'%s' % (search_url)

@hook.command
def manga(inp):
    "manga <query> - batoto Search"
    search_url = 'http://www.batoto.net/search?name=%s&name_cond=c&dosubmit=Search' % (inp.replace(' ','+'))
    results = http.get_html(search_url)
    try:
        result = results.xpath("//tbody//a/@href")[0]
        return u'%s' % (result)
    except IndexError:
        return u'No matches found.'


def GetInHMS(seconds):
    hours = seconds / 3600
    seconds -= 3600*hours
    minutes = seconds / 60
    seconds -= 60*minutes
    if hours == 0:
        return "%02d:%02d" % (minutes, seconds)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


@hook.command(autohelp=False)
def railgun(inp):
    from datetime import datetime, timedelta
    from pytz import timezone
    import pytz
    import time 
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    jp = timezone('Asia/Tokyo')
    # Current time in UTC
    jt = datetime.now(timezone('Asia/Tokyo'))
    now_jst = jt.strftime(fmt)

    jp_lt = jp.localize(datetime(2013, 04, 12, 23, 30, 0))
    #future_jst = jp_lt.strftime(fmt)    
    days_remaining = (jp_lt-jt).days
    seconds_remaining = (jp_lt-jt).seconds
    return '%s days %s remaining.' % (days_remaining, GetInHMS(seconds_remaining))