from util import hook, http
import re
import random
from datetime import datetime, timedelta
from pytz import timezone
import pytz
import time
import media

def parse_dayname(inp):
    days = {'sunday': 0,'monday': 1,'tuesday': 2,'wednesday': 3,'thursday': 4,'friday': 5,'saturday': 6}
    now = datetime.now(timezone('Asia/Tokyo'))
    today = days[now.strftime("%A").lower()]
    destday = days[inp.lower()]
    if destday < today: destday = destday + 7
    days_between = destday - today
    return days_between


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
    if days_remaining < 0 or days_remaining == 6: 
        diff=datetime.strptime('23:59:59','%H:%M:%S')-datetime.strptime(GetInHMS(seconds_remaining),'%H:%M:%S')
        return 'Aired %s ago' % (diff)
    else:
        return ('%s days %s' % (days_remaining, GetInHMS(seconds_remaining))).replace('1 days','1 day').replace('0 days ','')


@hook.command('release')
@hook.command
def anime(inp, notice=None):
    "release <input> - Returns the next airdate & time for an anime -- "\
    "Input can be: today, tomorrow, monday-sunday, or show name"

    days = []
    daynames = 'sunday monday tuesday wednesday thursday friday saturday'
    show_name = ''

    now = datetime.now(timezone('Asia/Tokyo'))
    curday = now.day - 1
    month = now.strftime("%m")
    year = now.year

    url = "http://www.animecalendar.net/%s/%s" % (year,month)

    try: soup = http.get_soup(url)
    except: return 'Website is down.'
    days = soup.findAll('div', {"class":re.compile(r'^da.+')})

    if 29 - int(curday) < 7:
        days_nextmonth = []
        url = "http://www.animecalendar.net/%s/%i" % (year, int(month) + 1)
        try: soup = http.get_soup(url)
        except: return 'Website is down.'
        days_nextmonth = soup.findAll('div', {"class":re.compile(r'^da.+')})
        days = days + days_nextmonth

    if inp.lower() in daynames \
    or inp == 'today' \
    or inp == 'tomorrow' \
    or inp == 'yesterday':
        if inp.lower() in daynames: curday = curday + parse_dayname(inp)
        elif inp == 'today': curday = curday 
        elif inp == 'tomorrow': curday = curday + 1
        elif inp == 'yesterday': curday = curday - 1
        show_date = days[curday].thead.h2.a['href'].replace('/','',1)
        result = ''
        shows = days[curday].table.tbody.findAll('div', {'class': 'tooltip'})
        for show in shows:
            show_name = show.find('td', {'class': 'tooltip_title'}).h4.text.strip()
            show_time =  show.find('td', {'class': 'tooltip_info'}).h4.text.split(' on')[0].strip()
            air_time = show_time.split('at ')[1].split(' ')[0].strip() + ':00'
            air_date = show_date.replace('/','-')
            time_until = get_time_until('%s %s' % (air_date,air_time))
            try: notice('%s\x02%s\x02: %s [%s]\n' % (result, show_name.decode('utf-8'), show_time,time_until))
            except: notice('%s\x02%s\x02: %s [%s]\n' % (result, show_name, show_time,time_until))
        return 'Sent!'
    else:
        while curday is not len(days):
            if days[curday].find(text=re.compile(".*"+inp+".*",re.IGNORECASE)):
                show_date = days[curday].thead.h2.a['href'].replace('/','',1)
                shows = days[curday].findAll('tr')
                for show in shows:
                    if show.find(text=re.compile(".*"+inp+".*",re.IGNORECASE)):
                        show_name = show.find('td', {'class': 'tooltip_title'}).h4.text.strip()
                        show_time =  show.find('td', {'class': 'tooltip_info'}).h4.text.split(' on')[0].strip()
                        air_time = show_time.split('at ')[1].split(' ')[0].strip() + ':00'
                        air_date = show_date.replace('/','-')
                        time_until = get_time_until('%s %s' % (air_date,air_time))
                        try: return('\x02%s\x02: %s on %s [%s]\n' % (show_name.decode('utf-8'), show_time, show_date, time_until))
                        except: return('\x02%s\x02: %s on %s [%s]\n' % (show_name, show_time, show_date, time_until))
                        return
            curday = curday + 1

    return media.get_series_info(inp)    
    
    


@hook.command
def animetake(inp):
    "animetake <list> | <get [query]> - searches animetake for the latest updates"
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
    search_url = 'http://nyaa.eu/?page=search&cats=1_37&filter=0&term=%s' % (inp.replace(' ','+'))
    return u'%s' % (search_url)


@hook.command
def sn(inp):
    "sukebei nyaa <query> - sukebei NYAA Search"
    search_url = 'http://sukebei.nyaa.se/?page=search&filter=0&term=%s' % (inp.replace(' ','+'))
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
        result = results.xpath("//tbody//strong/a/@href")[0]
        return u'%s' % (result)
    except IndexError:
        return u'No matches found.'


@hook.command
def mal(inp):
    "mal <query> - MyAnimeList anime result"
    url = "http://myanimelist.net/anime.php?q=%s" % inp.replace(' ','%20').strip()
    return url






# @hook.command(autohelp=False)
# def railgun(inp):
#     return get_time_until('2013-04-19 23:30:00')


# @hook.command(autohelp=False)
# def yahari(inp):
#     return get_time_until('2013-04-20 01:30:00')

@hook.command(autohelp=False)
def destiny(inp):
    return get_time_until('2014-12-09 22:59:00')

@hook.command(autohelp=False)
def iphone(inp):
    return get_time_until('2014-09-10 2:00:00')

@hook.command(autohelp=False)
def halo(inp):
    return get_time_until('2014-11-11 15:59:00')

@hook.command(autohelp=False)
def s6(inp):
    return 'nobody cares'


# import pyanidb as anidb
  
# #anidb.set_client("pyanihttp", 1)
  
# def get_anime(user, channel, text):
#     try:
#         aid = int(text.split()[1])
#     except ValueError:
#         msg(channel, "%s: %s can't be parsed into an anime id" % (user,
#             text.split()[1]))
#         return None
#     except IndexError:
#         return None
#     print "Querying AniDb for information about {}".format(aid)
#     try:
#         anime = anidb.query(anidb.QUERY_ANIME, aid)
#     except anidb.exceptions.BannedException:
#         msg(channel, "%s: Sorry, looks like I'm banned from using the HTTP api"
#                 % user)
#         return None
#     if anime is None:
#         print"No data"
#         return "Sorry, no data could be retrieved"
#     return anime
  

# def atags(user, channel, text):
#     """Show the tags of an anime. Parameters: an aid"""
#     anime = get_anime(user, channel, text)
#     if anime is None:
#         return
#     anime.tags.sort(cmp=lambda x, y: cmp(int(x.count), int(y.count)))
#     anime.tags.reverse()
#     tags = [tag.name for tag in anime.tags]
#     msg(channel, "Anime %s is tagged %s" % (anime.id,
#             ", ".join(tags[:int(get("max_tags", 5))])))
  

# def ainfo(user, channel, text):
#     """Query the AniDB for information about an anime. Parameters: An aid"""
#     anime = get_anime(user, channel, text)
#     if anime is None:
#         return
#     info_s = "Anime #%i: %i episodes." % (anime.id,
#             anime.episodecount)
#     if anime.startdate is not None:
#         info_s += " Airing from: %i/%i/%i" % (anime.startdate.year,
#                 anime.startdate.month, anime.startdate.day)
#     if anime.enddate is not None:
#         info_s += " to: %i/%i/%i" % (anime.enddate.year,
#                 anime.enddate.month, anime.enddate.day)
#     msg(channel, info_s)
  
#     rating_s = u"Ratings:"
#     for i in ("permanent", "temporary"):
#         if anime.ratings[i]["count"] is not None:
#             rating_s += " %s: %.2f by %i people." % \
#                 (i,
#                  anime.ratings[i]["rating"],
#                  anime.ratings[i]["count"])
#     msg(channel, rating_s)
#     titles = []
#     for lang in ("ja", "x-jat", "en", "de"):
#         try:
#             titles += [title.title for title in anime.titles[lang] if title.type ==
#                     "main" or title.type == "official"]
#         except KeyError:
#             # There are no titles for that language
#             pass
#     title_s = "Known as: %s" % ", ".join(titles)
#     msg(channel, title_s)
  
# @hook.command(autohelp=False)
# def asearch(inp, chan=None, notice=None):
#     """Search for an anime"""
#     try:
#         name = " ".join(inp.split()[1:])
#     except KeyError:
#         pass
#     print name
#     results = anidb.search(name)
#     max_results = int(get("max_search_results", 5))
  
#     if len(results) > max_results:
#         notice("Too many results, please refine your search")
        
  
#     result_strings = []
#     for anime in results:
#         titles = []
#         for lang in ("ja", "x-jat", "en", "de"):
#             try:
#                 titles += [title.title for title in anime.titles[lang] if title.type ==
#                         "main" or title.type == "official"]
#             except KeyError:
#                 # There are no titles for that language
#                 pass
#         result_strings.append("%i: %s" % (anime.id, ", ".join(titles)))
#     return result_strings
  
