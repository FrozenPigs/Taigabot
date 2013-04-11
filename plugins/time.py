from util import hook, http
import time
from util.text import capitalize_first

import urllib, urllib2

@hook.command('t', autohelp=False)
@hook.command(autohelp=False)
def time(inp, nick="", reply=None, db=None, notice=None):
    "time <location|@nick> [save] -- Gets time for <location>."

    # initalise locations DB
    db.execute("create table if not exists locations(ircname primary key, location)")
    
    if not inp: # if there is no input, try getting the users last location from the DB
        location = db.execute("select location from locations where ircname=lower(?)", [nick]).fetchone()
        if not location: # no location saved in the database, send the user help text
            notice(time.__doc__)
            return "No location stored for %s." % nick
        location = location[0]
        save = False # no need to save a location, we already have it
    elif inp.endswith(" save"):
        location = inp[:-5].strip().lower() # remove "save" from the input string after checking for it
        save = True
    elif '@' in inp:
        nick = inp.replace('@','')
        location = db.execute("select location from locations where ircname=lower(?)", [nick]).fetchone()
        if not location: # no location saved in the database, send the user help text
            return "No location stored for %s." % nick
        location = location[0]
        save = False # no need to save a location, we already have it
    else: 
        location = db.execute("select location from locations where ircname=lower(?)", [nick]).fetchone() # check if user already has a location
        if not location: save = True # If theres no location in the db, save it
        else: save = False 
        location = inp.strip().lower()

    # now, to get the actual time
    try:
        url = "https://www.google.com/search?q=time+in+%s" % location.replace(' ','+')
        html = http.get_html(url)
        prefix = html.xpath("//div[@class='vk_c vk_gy vk_sh']//span[@class='vk_gy vk_sh']/text()")[0].strip()
        time = html.xpath("//div[@class='vk_c vk_gy vk_sh']//div[@class='vk_bk vk_ans']/text()")[0].strip()
        day = html.xpath("//div[@class='vk_c vk_gy vk_sh']//div[@class='vk_gy vk_sh']/text()")[0].strip()
        date = html.xpath("//div[@class='vk_c vk_gy vk_sh']//div[@class='vk_gy vk_sh']/span/text()")[0].strip()
    except IndexError:
        return "Could not get time for that location."

    if location and save:
        db.execute("insert or replace into locations(ircname, locations) values (?,?)", (nick.lower(), location))
        db.commit()

    return '%s is \x02%s\x02 [%s %s]' % (prefix, time, day, date)



@hook.command(autohelp=False)
def beats(inp):
    "beats -- Gets the current time in .beats (Swatch Internet Time). "

    if inp.lower() == "wut":
        return "Instead of hours and minutes, the mean solar day is divided " \
        "up into 1000 parts called \".beats\". Each .beat lasts 1 minute and" \
        " 26.4 seconds. Times are notated as a 3-digit number out of 1000 af" \
        "ter midnight. So, @248 would indicate a time 248 .beats after midni" \
        "ght representing 248/1000 of a day, just over 5 hours and 57 minute" \
        "s. There are no timezones."

    t = time.gmtime()
    h, m, s = t.tm_hour, t.tm_min, t.tm_sec

    utc = 3600 * h + 60 * m + s
    bmt = utc + 3600  # Biel Mean Time (BMT)

    beat = bmt / 86.4

    if beat > 1000:
        beat -= 1000

    return "Swatch Internet Time: @%06.2f" % beat
