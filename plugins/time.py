from util import hook, http, database, formatting
import time
from util.text import capitalize_first
from bs4 import BeautifulSoup
import urllib2
import re

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.215 Safari/535.1"};

@hook.command('t', autohelp=False)
@hook.command('time', autohelp=False)
def timefunction(inp, nick="", reply=None, db=None, notice=None):
    "time [location] [dontsave] | [@ nick] -- Gets time for <location>."

    save = True

    if '@' in inp:
        nick = inp.split('@')[1].strip()
        location = database.get(db,'users','location','nick',nick)
        if not location: return "No location stored for {}.".format(nick.encode('ascii', 'ignore'))
    else:
        location = database.get(db,'users','location','nick',nick)
        if not inp:
            if not location:
                notice(time.__doc__)
                return
        else:
            # if not location: save = True
            if " dontsave" in inp: save = False
            location = inp.split()[0]

    # now, to get the actual time
    try:
        url = "https://www.google.com/search?q=time+in+{}".format(location.replace(' ','+').replace(' save',''))
        request = urllib2.Request(url, None, headers)
        page = urllib2.urlopen(request).read()
        soup = BeautifulSoup(page, 'lxml')
        soup = soup.find('div', attrs={'id': re.compile('ires')})

        time = filter(None, http.strip_html(soup.find('div', attrs={'class': re.compile('vk_gy')}).renderContents().strip()).split(' '))
        prefix = ' '.join(time[6:])
        curtime = time[0]
        day = time[1]
        date = ' '.join(time[2:4])
    except IndexError:
        return "Could not get time for that location."

    if location and save: database.set(db,'users','location',location,'nick',nick)

    return formatting.output('Time', [u'{} is \x02{}\x02 [{} {}]'.format(prefix, curtime, day, date)])



@hook.command('ttest', autohelp=False)
def timefunction2(inp, nick="", reply=None, db=None, notice=None):
    "time [location] [dontsave] | [@ nick] -- Gets time for <location>."

    save = True

    if '@' in inp:
        nick = inp.split('@')[1].strip()
        location = database.get(db,'users','location','nick',nick)
        if not location: return "No location stored for {}.".format(nick.encode('ascii', 'ignore'))
    else:
        location = database.get(db,'users','location','nick',nick)
        if not inp:
            if not location:
                notice(time.__doc__)
                return
        else:
            # if not location: save = True
            if " dontsave" in inp: save = False
            location = inp.split()[0]

    # now, to get the actual time
    try:
        url = "https://time.is/%s" % location.replace(' ','+').replace(' save','')
        html = http.get_html(url)
        prefix = html.xpath("//div[@id='msgdiv']/h1/a/text()")[0].strip()
        curtime = html.xpath("//div[contains(@id,'twd')]/text()")[0].strip()
        ampm = html.xpath("//div[contains(@id,'twd')]/span/text()")[0].strip()
        date = html.xpath("//h2[contains(@id,'dd')]/text()")[0].strip()
    except IndexError:
        return "Could not get time for that location."

    if location and save: database.set(db,'users','location',location,'nick',nick)

    return u'Time in {} is \x02{} {}\x02 [{}]'.format(prefix, curtime, ampm.upper(), date)




api_url = 'http://api.wolframalpha.com/v2/query?format=plaintext'

def watime(inp, bot=None):
    """time <area> -- Gets the time in <area>"""

    query = "current time in {}".format(inp)

    api_key = bot.config.get("api_keys", {}).get("wolframalpha", None)
    if not api_key:
        return "error: no wolfram alpha api key set"

    request = http.get_xml(api_url, input=query, appid=api_key)
    time = " ".join(request.xpath("//pod[@title='Result']/subpod/plaintext/text()"))
    time = time.replace("  |  ", ", ")

    if time:
        # nice place name for UNIX time
        if inp.lower() == "unix":
            place = "Unix Epoch"
        else:
            place = capitalize_first(" ".join(request.xpath("//pod[@"
                                                            "title='Input interpretation']/subpod/plaintext/text()"))[
                                     16:])
        return "{} - \x02{}\x02".format(time, place)
    else:
        return u"Could not get the time for '{}'.".format(inp)


@hook.command(autohelp=False)
def beats(inp):
    """beats -- Gets the current time in .beats (Swatch Internet Time). """

    if inp.lower() == "wut":
        return "Instead of hours and minutes, the mean solar day is divided " \
               "up into 1000 parts called \".beats\". Each .beat lasts 1 minute and" \
               " 26.4 seconds. Times are notated as a 3-digit number out of 1000 af" \
               "ter midnight. So, @248 would indicate a time 248 .beats after midni" \
               "ght representing 248/1000 of a day, just over 5 hours and 57 minute" \
               "s. There are no timezones."
    elif inp.lower() == "guide":
        return u"1 day = 1000 .beats, 1 hour = 41.666 .beats, 1 min = 0.6944 .beats, 1 second = 0.01157 .beats"

    t = time.gmtime()
    h, m, s = t.tm_hour, t.tm_min, t.tm_sec

    utc = 3600 * h + 60 * m + s
    bmt = utc + 3600  # Biel Mean Time (BMT)

    beat = bmt / 86.4

    if beat > 1000:
        beat -= 1000

    return formatting.output('Swatch Internet Time', ['@{0:.2f}'.format(beat)])
