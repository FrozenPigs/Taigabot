from util import hook, user, database
import os
import sys
import re
import json
import time
import subprocess

# def get_chan(inp,chan):
#     if inp:
#         if inp[0][0] == "#": 
#             chan = inp.split()[0]
#             inp = inp.replace(chan,'').strip()
#     return (inp.lower(),chan.lower())

@hook.command(adminonly=True)
def gadmin(inp, notice=None, bot=None, config=None, db=None):
    "gadmin <add|del> <nick|host> -- Make <nick|host> an global admin." \
    "(you can delete multiple admins at once)"
    inp = inp.lower()
    command = inp.split()[0]
    targets = inp.split()[1:]

    if 'add' in command:
        for target in targets:
            target = user.get_hostmask(target,db)
            if target in bot.config["admins"]:
                notice(u"%s is already a global admin." % target)
            else:
                notice(u"%s is now a global admin." % target)
                bot.config["admins"].append(target)
                bot.config["admins"].sort()
                json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
        return
    elif 'del' in command:
        for target in targets:
            if target in bot.config["admins"]:
                notice(u"%s is no longer a global admin." % target)
                bot.config["admins"].remove(target)
                bot.config["admins"].sort()
                json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
            else:
                notice(u"%s is not a global admin." % target)
        return


@hook.command(autohelp=False)
def gadmins(inp, notice=None, bot=None):
    "admins -- Lists bot's global admins."
    if bot.config["admins"]:
        notice(u"Admins are: %s." % ", ".join(bot.config["admins"]))
    else:
        notice(u"There are no users with global admin powers.")
    return


@hook.command(autohelp=False, permissions=["permissions_users"], adminonly=True)
def permissions(inp, bot=None, notice=None):
    """permissions [group] -- lists the users and their permission level who have permissions."""
    permissions = bot.config.get("permissions", [])
    groups = []
    if inp:
        for k in permissions:
            if inp == k:
                groups.append(k)
    else:
        for k in permissions:
            groups.append(k)
    if not groups:
        notice(u"{} is not a group with permissions".format(inp))
        return None

    for v in groups:
        members = ""
        for value in permissions[v]["users"]:
            members = members + value + ", "
        if members:
            notice(u"the members in the {} group are..".format(v))
            notice(members[:-2])
        else:
            notice(u"there are no members in the {} group".format(v))


@hook.command(permissions=["permissions_users"], adminonly=True)
def deluser(inp, bot=None, notice=None):
    """deluser [user] [group] -- removes elevated permissions from [user].
    If [group] is specified, they will only be removed from [group]."""
    permissions = bot.config.get("permissions", [])
    inp = inp.split(" ")
    groups = []
    try:
        specgroup = inp[1]
    except IndexError:
        specgroup = None
        for k in permissions:
            groups.append(k)
    else:
        for k in permissions:
            if specgroup == k:
                groups.append(k)
    if not groups:
        notice(u"{} is not a group with permissions".format(inp[1]))
        return None

    removed = 0
    for v in groups:
        users = permissions[v]["users"]
        for value in users:
            if inp[0] == value:
                users.remove(inp[0])
                removed = 1
                notice(u"{} has been removed from the group {}".format(inp[0], v))
                json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
    if specgroup:
        if removed == 0:
            notice(u"{} is not in the group {}".format(inp[0], specgroup))
    else:
        if removed == 0:
            notice(u"{} is not in any groups".format(inp[0]))


@hook.command(permissions=["permissions_users"], adminonly=True)
def adduser(inp, bot=None, notice=None):
    """adduser [user] [group] -- adds elevated permissions to [user].
    [group] must be specified."""
    permissions = bot.config.get("permissions", [])
    inp = inp.split(" ")
    try:
        user = inp[0]
        targetgroup = inp[1]
    except IndexError:
        notice(u"the group must be specified")
        return None
    if not re.search('.+!.+@.+', user):
        notice(u"the user must be in the form of \"nick!user@host\"")
        return None
    try:
        users = permissions[targetgroup]["users"]
    except KeyError:
        notice(u"no such group as {}".format(targetgroup))
        return None
    if user in users:
        notice(u"{} is already in {}".format(user, targetgroup))
        return None

    users.append(user)
    notice(u"{} has been added to the group {}".format(user, targetgroup))
    users.sort()
    json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)


@hook.command("quit", autohelp=False, permissions=["botcontrol"], adminonly=True)
@hook.command(autohelp=False, permissions=["botcontrol"])
def stop(inp, nick=None, conn=None):
    """stop [reason] -- Kills the bot with [reason] as its quit message."""
    if inp:
        conn.cmd("QUIT", ["Killed by {} ({})".format(nick, inp)])
    else:
        conn.cmd("QUIT", ["Killed by {}.".format(nick)])
    time.sleep(5)
    os.execl("./bot", "bot", "stop")


@hook.command(autohelp=False, permissions=["botcontrol"], adminonly=True)
def restart(inp, nick=None, conn=None, bot=None):
    """restart [reason] -- Restarts the bot with [reason] as its quit message."""
    for botcon in bot.conns:
        if inp:
            bot.conns[botcon].cmd("QUIT", ["Restarted by {} ({})".format(nick, inp)])
        else:
            bot.conns[botcon].cmd("QUIT", ["Restarted by {}.".format(nick)])
    time.sleep(5)
    #os.execl("./bot", "bot", "restart")
    args = sys.argv[:]
    args.insert(0, sys.executable)
    os.execv(sys.executable, args)


@hook.command(autohelp=False, permissions=["botcontrol"], adminonly=True)
def clearlogs(inp, input=None):
    """clearlogs -- Clears the bots log(s)."""
    subprocess.call(["./bot", "clear"])


@hook.command(permissions=["botcontrol"], adminonly=True)
def join(inp, conn=None, notice=None, bot=None):
    """join <channel> -- Joins <channel>."""
    for target in inp.split(" "):
        if not target.startswith("#"):
            target = "#{}".format(target)
        notice(u"Attempting to join {}...".format(target))
        conn.join(target)

    channellist = bot.config["connections"][conn.name]["channels"]
    channellist.append(target)
    json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)


@hook.command(autohelp=False, permissions=["botcontrol"], adminonly=True)
def part(inp, conn=None, chan=None, notice=None, bot=None):
    """part <channel> -- Leaves <channel>.
    If [channel] is blank the bot will leave the
    channel the command was used in."""
    if inp:
        targets = inp
    else:
        targets = chan
    for target in targets.split(" "):
        if not target.startswith("#"):
            target = "#{}".format(target)
        notice(u"Attempting to leave {}...".format(target))
        conn.part(target)

    channellist = bot.config["connections"][conn.name]["channels"]
    channellist.remove(target)
    json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)


@hook.command(autohelp=False, permissions=["botcontrol"], adminonly=True)
def cycle(inp, conn=None, chan=None, notice=None):
    """cycle <channel> -- Cycles <channel>.
    If [channel] is blank the bot will cycle the
    channel the command was used in."""
    if inp:
        target = inp
    else:
        target = chan
    notice(u"Attempting to cycle {}...".format(target))
    conn.part(target)
    conn.join(target)


@hook.command(permissions=["botcontrol"], adminonly=True)
def nick(inp, notice=None, conn=None):
    """nick <nick> -- Changes the bots nickname to <nick>."""
    if not re.match("^[A-Za-z0-9_|.-\]\[]*$", inp.lower()):
        notice(u"Invalid username!")
        return
    notice(u"Attempting to change nick to \"{}\"...".format(inp))
    conn.set_nick(inp)


@hook.command(permissions=["botcontrol"], adminonly=True)
def raw(inp, conn=None, notice=None):
    """raw <command> -- Sends a RAW IRC command."""
    notice(u"Raw command sent.")
    conn.send(inp)


@hook.command(permissions=["botcontrol"], adminonly=True)
def say(inp, conn=None, chan=None):
    """say [channel] <message> -- Makes the bot say <message> in [channel].
    If [channel] is blank the bot will say the <message> in the channel
    the command was used in."""
    inp = inp.split(" ")
    if inp[0][0] == "#":
        message = " ".join(inp[1:])
        out = u"PRIVMSG {} :{}".format(inp[0], message)
    else:
        message = " ".join(inp[0:])
        out = u"PRIVMSG {} :{}".format(chan, message)
    conn.send(out)


@hook.command(adminonly=True)
def msg(inp, conn=None, chan=None, notice=None):
    "msg <user> <message> -- Sends a Message."
    user = inp.split()[0]
    message = inp.replace(user,'').strip()
    out = u"PRIVMSG %s :%s" % (user, message)
    conn.send(out)


@hook.command("act", permissions=["botcontrol"], adminonly=True)
@hook.command(permissions=["botcontrol"], adminonly=True)
def me(inp, conn=None, chan=None):
    """me [channel] <action> -- Makes the bot act out <action> in [channel].
    If [channel] is blank the bot will act the <action> in the channel the
    command was used in."""
    inp = inp.split(" ")
    if inp[0][0] == "#":
        message = ""
        for x in inp[1:]:
            message = message + x + " "
        message = message[:-1]
        out = u"PRIVMSG {} :\x01ACTION {}\x01".format(inp[0], message)
    else:
        message = ""
        for x in inp[0:]:
            message = message + x + " "
        message = message[:-1]
        out = u"PRIVMSG {} :\x01ACTION {}\x01".format(chan, message)
    conn.send(out)


@hook.command(adminonly=True)
def ctcp(inp, conn=None, chan=None, notice=None):
    "ctcp <destination> <command> -- Send a CTCP command"
    inp = inp.split(" ")
    destination = inp[0]
    command = inp[1]
    command = command.upper()
    #if message == None:
    result = conn.send('PRIVMSG {} :\x01{}\x01'.format( destination, command ) )
    #out = u"PRIVMSG %s :%s" % (chan, result)
    #conn.send(out)
    #else:
    # conn.send ( 'PRIVMSG {} :\x01{} {}\x01'.format( destination, command, message ) )


@hook.command(adminonly=True)
def set(inp, conn=None, chan=None, db=None, notice=None):
    "set <field> <nick> <value> -- Admin override for setting database values. " \
    "Example: set location infinity 80210 - " \
    "set lastfm infinity spookieboogie"

    # inpsplit = inp.split(" ")
    try:
        field = inp.split(" ")[0].strip()
        nick = inp.split(" ")[1].strip()
        # value = inp.split(" ")[2:]
        value = inp.replace(field,'').replace(nick,'').strip()
        # if type(value) is list: ' '.join(value[0:])
        print value
    except IndexError: 
        notice(u"PRIVMSG {} :Could not set {}.".format(chan, field))
        return

    if field and nick and value:
        if 'del' in value: value = ''
        if 'location' in field or \
            'lastfm' in field or  \
            'desktop' in field or \
            'battlestation' in field or\
            'greeting' in field :
            #if type(value) is list: value = value[0]
            database.set(db,'users',field, value,'nick',nick) 
            notice(u"PRIVMSG {} :Set {} for {} to {}.".format(chan, field, nick, value))
    else:
        notice(u"PRIVMSG {} :Could not set {}.".format(chan, field))

    return

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


@hook.command(adminonly=True, autohelp=False)
def db(inp,db=None):
    split = inp.split(' ')
    action = split[0]
    if "init" in action:
        result = db.execute("create table if not exists users(nick primary key, host, location, greeting, lastfm, fines, battlestation, desktop, horoscope, version)")
        db.commit()
        return result
    elif "addcol" in action: 
        table = split[1]
        col = split[2]
        if table is not None and col is not None:
            db.execute("ALTER TABLE {} ADD COLUMN {}".format(table,col))
            db.commit
            return "Added Column"


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


@hook.command(adminonly=True)
def test(inp,db=None):
    host = user.get_hostmask(inp,db)
    print host
    hostmask = host.lower().replace('~','').replace('*','\S+')
    print hostmask
    matchmask = "sid18764@.+uxbridge.irccloud.com wednesday@le-wednesday-face.org 680i@.+studby.hig.no themadman@.+want.it.now austin@.+this.is.austin urmom@.+kills.your.gainz moss@.+like.a.hamster quinn@.+fios.verizon.net sgs@michael-jackson.whosodomized.me kalashniko@doesnt.break.stuff ichiroku@.+fios.verizon.net connor@.+nasty.skanky.slut"
    #print "{} -- {}".format(matchmask,hostmask)
    if bool(re.search(hostmask,matchmask)): return True
    else: return False




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
