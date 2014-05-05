from util import hook, user, database
import os
import sys
import re
import json
import time
import subprocess



# @hook.command(autohelp=False, permissions=["permissions_users"], adminonly=True)
# def permissions(inp, bot=None, notice=None):
#     """permissions [group] -- lists the users and their permission level who have permissions."""
#     permissions = bot.config.get("permissions", [])
#     groups = []
#     if inp:
#         for k in permissions:
#             if inp == k:
#                 groups.append(k)
#     else:
#         for k in permissions:
#             groups.append(k)
#     if not groups:
#         notice(u"{} is not a group with permissions".format(inp))
#         return None

#     for v in groups:
#         members = ""
#         for value in permissions[v]["users"]:
#             members = members + value + ", "
#         if members:
#             notice(u"the members in the {} group are..".format(v))
#             notice(members[:-2])
#         else:
#             notice(u"there are no members in the {} group".format(v))


# @hook.command(permissions=["permissions_users"], adminonly=True)
# def deluser(inp, bot=None, notice=None):
#     """deluser [user] [group] -- removes elevated permissions from [user].
#     If [group] is specified, they will only be removed from [group]."""
#     permissions = bot.config.get("permissions", [])
#     inp = inp.split(" ")
#     groups = []
#     try:
#         specgroup = inp[1]
#     except IndexError:
#         specgroup = None
#         for k in permissions:
#             groups.append(k)
#     else:
#         for k in permissions:
#             if specgroup == k:
#                 groups.append(k)
#     if not groups:
#         notice(u"{} is not a group with permissions".format(inp[1]))
#         return None

#     removed = 0
#     for v in groups:
#         users = permissions[v]["users"]
#         for value in users:
#             if inp[0] == value:
#                 users.remove(inp[0])
#                 removed = 1
#                 notice(u"{} has been removed from the group {}".format(inp[0], v))
#                 json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
#     if specgroup:
#         if removed == 0:
#             notice(u"{} is not in the group {}".format(inp[0], specgroup))
#     else:
#         if removed == 0:
#             notice(u"{} is not in any groups".format(inp[0]))


# @hook.command(permissions=["permissions_users"], adminonly=True)
# def adduser(inp, bot=None, notice=None):
#     """adduser [user] [group] -- adds elevated permissions to [user].
#     [group] must be specified."""
#     permissions = bot.config.get("permissions", [])
#     inp = inp.split(" ")
#     try:
#         user = inp[0]
#         targetgroup = inp[1]
#     except IndexError:
#         notice(u"the group must be specified")
#         return None
#     if not re.search('.+!.+@.+', user):
#         notice(u"the user must be in the form of \"nick!user@host\"")
#         return None
#     try:
#         users = permissions[targetgroup]["users"]
#     except KeyError:
#         notice(u"no such group as {}".format(targetgroup))
#         return None
#     if user in users:
#         notice(u"{} is already in {}".format(user, targetgroup))
#         return None

#     users.append(user)
#     notice(u"{} has been added to the group {}".format(user, targetgroup))
#     users.sort()
#     json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)


@hook.command("stfu", adminonly=True)
@hook.command("silence", adminonly=True)
@hook.command(adminonly=True)
def shutup(inp, conn=None, chan=None, notice=None):
    "shutup [channel] <user> -- Shuts the user up. "
    # inp = inp.split(" ")
    if inp[0][0] == "#":
        chan = inp.split(" ")[0]
        users = inp.split(" ")[1:]
    else:
        users = inp.split(" ")

    for user in users:
        out = u"MODE %s +m-voh %s %s %s" % (chan, user, user, user)
        conn.send(out)
        notice(u"Shut up %s from %s..." % (user, chan))

    conn.send(out)


@hook.command(adminonly=True)
def speak(inp, conn=None, chan=None, notice=None):
    "speak [channel] <user> -- Shuts the user up. "
    if inp[0][0] == "#":
        chan = inp.split(" ")[0]
        users = inp.split(" ")[1:]
    else:
        users = inp.split(" ")

    for user in users:
        out = u"MODE %s -m" % (chan)
        conn.send(out)

    notice(u"Shut up %s from %s..." % (user, chan))


# @hook.command(adminonly=True, autohelp=False)
# def db(inp,db=None):
#     split = inp.split(' ')
#     action = split[0]
#     if "init" in action:
#         result = db.execute("create table if not exists users(nick primary key, host, location, greeting, lastfm, fines, battlestation, desktop, horoscope, version)")
#         db.commit()
#         return result
#     elif "addcol" in action: 
#         table = split[1]
#         col = split[2]
#         if table is not None and col is not None:
#             db.execute("ALTER TABLE {} ADD COLUMN {}".format(table,col))
#             db.commit
#             return "Added Column"


# UPDATE usersettings SET fines=(SELECT totalfines FROM fines WHERE nick = usersettings.nick);


def compare_hostmasks(hostmask,matchmask):
    hostmask = hostmask.replace('~','').replace('*','\S+').lower()
    matchmask = matchmask.replace('*','.+').lower()
    if bool(re.search(hostmask,matchmask)): return True
    else: return False

@hook.command(adminonly=True)
def checkhost(inp, conn=None, chan=None, notice=None):
    inp = inp.split(' ')
    hostmask = inp[0]
    matchmask = inp[1]

    return compare_hostmasks(hostmask,matchmask)

from fnmatch import fnmatch
@hook.command(adminonly=True)
def test(inp,db=None):
    #host = user.get_hostmask(inp,db)

    nick = inp.strip().replace('~','').lower()
    host = database.get(db,'users','mask','nick',nick)

    print host
    hostmask = host.lower().replace('~','') #.replace('*','\S+')
    # hostmask = "*{}*".format(hostmask)
    print hostmask
    matchmask = "sid18764@.*uxbridge.irccloud.com infinity@.*like.lolis *@i.like.lolis infinity@i.like.lolis wednesday@le-wednesday-face.org 680i@.+studby.hig.no themadman@.+want.it.now austin@.+this.is.austin urmom@.+kills.your.gainz moss@.+like.a.hamster quinn@.+fios.verizon.net sgs@michael-jackson.whosodomized.me kalashniko@doesnt.break.stuff ichiroku@.+fios.verizon.net connor@.+nasty.skanky.slut"
    #print "{} -- {}".format(matchmask,hostmask)
    for pattern in matchmask.split(' '):
        if fnmatch(hostmask, pattern):
            print "MATCHED: {}".format(pattern)
    # print fnmatch(matchmask,hostmask)
    # matches = re.search(hostmask,matchmask)
    #return matches.group(0)
    #if bool(re.search(hostmask,matchmask)): return True
    #else: return False




    #Database conversion commands
#Update Uguu's default databases
@hook.command(adminonly=True)
def migrate_old_db(inp, notice=None, bot=None, db=None, config=None):
    #db.execute("ALTER TABLE seen_user RENAME TO seen")
    #db.execute("create table if not exists seen(name, time, quote, chan, host, primary key(name, chan))")
    db.commit()

    #db.execute("ALTER TABLE weather RENAME TO locations")
    #db.execute("DROP TABLE seen")
    
    #db.execute("DROP TABLE seen")
    
    #db.execute("create table if not exists seen(name, time, quote, chan, host, "
    #             "primary key(name, chan))")
    #db.commit()
    #db.commit()
    #db.execute("ALTER TABLE seen_user RENAME TO seen")
    #db.execute("INSERT OR IGNORE INTO usersettings (nick, lastfm) SELECT ircname, lastfmname FROM usernames")
    #notice('LastFM data was imported into usersettings')
    #db.commit()

    
    

    #Migrate old CloudBot DBs
    #LastFM
    #db.execute("create table if not exists usernames (ircname primary key, lastfmname)")
    #db.execute("INSERT INTO usernames (ircname, lastfmname) SELECT nick, acc FROM lastfm") 
    #db.execute("DROP TABLE lastfm")
    #db.commit()   
 
    #Weather
    #db.execute("create table if not exists locationsCopy (ircname primary key, location)")
    #db.execute("INSERT INTO locationsCopy (ircname, location) SELECT nick, loc FROM locations")
    #db.execute("ALTER TABLE locations RENAME TO locationsOrig")
    #db.execute("ALTER TABLE locationsCopy RENAME TO locations")    
    #db.execute("DROP TABLE locationsOrig")
    #db.commit()
    conn.send(out)







    # OLD
# @hook.command
# def distance(inp):
#     "distance <start> to <end> -- Calculate the distance between 2 places."
#     if 'from ' in inp: inp = inp.replace('from ','')
#     inp = inp.replace(', ','+')
#     start = inp.split(" to ")[0].strip().replace(' ','+')
#     dest = inp.split(" to ")[1].strip().replace(' ','+')
#     url = "http://www.travelmath.com/flying-distance/from/%s/to/%s" % (start, dest)
#     print url
#     soup = http.get_soup(url)
#     query = soup.find('h1', {'class': re.compile('flight-distance')})
#     distance = soup.find('h3', {'class': 'space'})
#     result = "%s %s" % (query, distance)
#     result = http.strip_html(result)
#     result = unicode(result, "utf8").replace('flight ','')

#     if not distance:
#         return "Could not calculate the distance from %s to %s." % (start, dest)

#     return result






