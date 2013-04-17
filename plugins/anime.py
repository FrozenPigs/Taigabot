from util import hook, http
#import urllib, urllib2
import re
#from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import time


@hook.command('anime')
@hook.command
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
def vndb(inp):
    "vndb <query> - Visual Novel Search"
    search_url = 'http://vndb.org/v/all?sq=%s' % (inp.replace(' ','+'))
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


@hook.command
def mal(inp):
    "mal <query> - MyAnimeList anime result"
    url = "http://myanimelist.net/anime.php?q=%s" % inp.replace(' ','%20').strip()
    return url


def parse_dayname(inp):
    days = {'auto': '',
        'sunday': 0,
        'monday': 1,
        'tuesday': 2,
        'wednesday': 3,
        'thursday': 4,
        'friday': 5,
        'saturday': 6
        }
	
    now = datetime.now(timezone('Asia/Tokyo'))
    today = days[now.strftime("%A").lower()]
    destday = days[inp.lower()]
    print today
    print destday
    if destday < today: destday = destday + 7
    days_between = destday - today
    return days_between
    #days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']


def get_releases():
    print 'running'

@hook.command()
def release(inp, notice=None):
    "release <input> - Returns the next airdate & time for an anime -- "\
    "Input can be: today, tomorrow, monday-sunday, or show name"
    url = "http://www.animecalendar.net/"
    days = []
    curday = datetime.now(timezone('Asia/Tokyo')).day - 1
    soup = http.get_soup(url)
    days = soup.findAll('div', {"class":re.compile(r'^da.+')})
    if inp.lower() in 'sunday monday tuesday wednesday thursday friday saturday':
        curday = curday + parse_dayname(inp)
        show_date = days[curday].thead.h2.a['href'].replace('/','',1)
        result = ''
        shows = days[curday].table.tbody.findAll('div', {'class': 'tooltip'})
        for show in shows:
            show_name = show.find('td', {'class': 'tooltip_title'}).h4.text.strip()
            show_time =  show.find('td', {'class': 'tooltip_info'}).h4.text.split(' on')[0].strip()
            air_time = show_time.split('at ')[1].split(' ')[0].strip() + ':00'
            air_date = show_date.replace('/','-')
            time_until = get_time_until('%s %s' % (air_date,air_time))
            notice('%s\x02%s\x02: %s [%s]\n' % (result, show_name, show_time,time_until))
    elif inp == 'today':
        curday = curday 
        show_date = days[curday].thead.h2.a['href'].replace('/','',1)
        result = ''
        shows = days[curday].table.tbody.findAll('div', {'class': 'tooltip'})
        for show in shows:
            show_name = show.find('td', {'class': 'tooltip_title'}).h4.text.strip()
            show_time =  show.find('td', {'class': 'tooltip_info'}).h4.text.split(' on')[0].strip()
            air_time = show_time.split('at ')[1].split(' ')[0].strip() + ':00'
            air_date = show_date.replace('/','-')
            time_until = get_time_until('%s %s' % (air_date,air_time))
            notice('%s\x02%s\x02: %s [%s]\n' % (result, show_name, show_time,time_until))
    if inp == 'tomorrow':
        curday = curday + 1
        show_date = days[curday].thead.h2.a['href'].replace('/','',1)
        result = ''
        shows = days[curday].table.tbody.findAll('div', {'class': 'tooltip'})
        for show in shows:
            show_name = show.find('td', {'class': 'tooltip_title'}).h4.text.strip()
            show_time =  show.find('td', {'class': 'tooltip_info'}).h4.text.split(' on')[0].strip()
            air_time = show_time.split('at ')[1].split(' ')[0].strip() + ':00'
            air_date = show_date.replace('/','-')
            time_until = get_time_until('%s %s' % (air_date,air_time))
            notice('%s\x02%s\x02: %s [%s]\n' % (result, show_name, show_time,time_until))
    else:
        while curday is not len(days):
            if days[curday].find(text=re.compile(".*"+inp+".*",re.IGNORECASE)):
                show_date = days[curday].thead.h2.a['href'].replace('/','',1)
                shows = days[curday].findAll('tr')
                for show in shows:
                    if show.find(text=re.compile(".*"+inp+".*",re.IGNORECASE)):
                        show_name =  http.strip_html(str(show.find('td', {'class': 'tooltip_title'}))).strip()
                        show_time =  http.strip_html(str(show.find('td', {'class': 'tooltip_info'}))).strip()
                        air_time = show_time.split('at ')[1].split(' ')[0].strip() + ':00'
                        air_date = show_date.replace('/','-')
                        time_until = get_time_until('%s %s' % (air_date,air_time))
                        return '\x02%s\x02: %s (%s) [%s]' % (show_name, show_time, show_date,time_until)
                        break
            curday = curday + 1

def GetInHMS(seconds):
    hours = seconds / 3600
    seconds -= 3600*hours
    minutes = seconds / 60
    seconds -= 60*minutes
    if hours == 0:
        return "%02d:%02d" % (minutes, seconds)
    return "%02d:%02d:%02d" % (hours, minutes, seconds)

@hook.command(autohelp=False)
def get_time_until(inp):
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    jp = timezone('Asia/Tokyo')
    jt = datetime.now(timezone('Asia/Tokyo'))
    now_jst = jt.strftime(fmt)
    jp_lt = jp.localize(datetime.strptime(inp,'%Y-%m-%d %H:%M:%S')) 
    days_remaining = (jp_lt-jt).days
    seconds_remaining = (jp_lt-jt).seconds
    if days_remaining < 0: 
        diff=datetime.strptime('23:59:59','%H:%M:%S')-datetime.strptime(GetInHMS(seconds_remaining),'%H:%M:%S')
        return 'Aired %s ago' % (diff)
    else:
        return ('%s days %s' % (days_remaining, GetInHMS(seconds_remaining))).replace('0 days ','')













    #print days[curday]
    #print curday
    

    # days = soup.findAll(text="Karneval")
    # for day in days:
    #     print day.findParent('h2')
            #print day.thead.h2.a[@href]
            
    
    

    #html = http.get_html(url)
    #link = html.xpath("//table[@class='images_table']//a/@href")[num]
    #days = html.xpath('.//div[contains(@class, "day")]')
    #result = days.xpath('.//tr//a[contains(.,"Karneval")]/a')
    #print days[0].text
# doc.xpath('.//td[contains(.,"today") and @class="banana"]/a')
# for a in mySearchTree.xpath('.//tr/*/a'):
#     print 'found "%s" link to href "%s"' % (a.text, a.get('href'))


    #while curday <= 
    #for day in days:
    #  anime_link = li.find('div', 'updateinfo').h4.a
    #  anime_updates.append('%s : %s' % (anime_link['title'], anime_link['href']))















@hook.command(autohelp=False)
def railgun(inp):
     
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    jp = timezone('Asia/Tokyo')
    # Current time in UTC
    jt = datetime.now(timezone('Asia/Tokyo'))
    now_jst = jt.strftime(fmt)

    jp_lt = jp.localize(datetime(2013, 04, 19, 11, 30, 0))
    #future_jst = jp_lt.strftime(fmt)    
    days_remaining = (jp_lt-jt).days
    seconds_remaining = (jp_lt-jt).seconds
    return '%s days %s remaining.' % (days_remaining, GetInHMS(seconds_remaining))

@hook.command(autohelp=False)
def yahari(inp):
    from datetime import datetime, timedelta
    from pytz import timezone
    import pytz
    import time 
    fmt = '%Y-%m-%d %H:%M:%S %Z%z'
    jp = timezone('Asia/Tokyo')
    # Current time in UTC
    jt = datetime.now(timezone('Asia/Tokyo'))
    now_jst = jt.strftime(fmt)

    jp_lt = jp.localize(datetime(2013, 04, 20, 01, 30, 0))
    #future_jst = jp_lt.strftime(fmt)    
    days_remaining = (jp_lt-jt).days
    seconds_remaining = (jp_lt-jt).seconds
    return '%s days %s remaining.' % (days_remaining, GetInHMS(seconds_remaining))