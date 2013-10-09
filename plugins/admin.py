from util import hook
import os
import re
import json
import time
import subprocess
from configobj import ConfigObj


@hook.command
def url(inp):
    "url -- Returns Uguubots URL."
    return 'https://github.com/infinitylabs/UguuBot'


#Database conversion commands
#Update Uguu's default databases
@hook.command(adminonly=True)
def migrate_old_db(inp, notice=None, bot=None, db=None, config=None):
    db.execute("ALTER TABLE weather RENAME TO locations")
    db.commit()

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

    
@hook.command(adminonly=True)
def gadmin(inp, notice=None, bot=None, config=None):
    "gadmin <add|del> <nick|host> -- Make <nick|host> an global admin." \
    "(you can delete multiple admins at once)"
    inp = inp.lower()
    command = inp.split()[0]
    targets = inp.split()[1:]

    if 'add' in command:
        for target in targets:
            if target in bot.config["admins"]:
                notice("%s is already a global admin." % target)
            else:
                notice("%s is now a global admin." % target)
                bot.config["admins"].append(target)
                bot.config["admins"].sort()
                json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
        return
    elif 'del' in command:
        for target in targets:
            if target in bot.config["admins"]:
                notice("%s is no longer a global admin." % target)
                bot.config["admins"].remove(target)
                bot.config["admins"].sort()
                json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
            else:
                notice("%s is not a global admin." % target)
        return


@hook.command(autohelp=False)
def gadmins(inp, notice=None, bot=None):
    "admins -- Lists bot's global admins."
    if bot.config["admins"]:
        notice("Admins are: %s." % ", ".join(bot.config["admins"]))
    else:
        notice("There are no users with global admin powers.")
    return


@hook.command(adminonly=True)
def admin(inp, chan=None, notice=None, bot=None, config=None):
    "admin [channel] <add|del> <nick|host> -- Make <nick|host> a channel admin." \
    "(you can add/delete multiple admins at once)"
    inp = inp.lower()
    if inp[0][0] == "#": 
        chan = inp.split(" ")[0]
        inp = inp.replace(chan,'').strip()
    channel = chan.lower()
    command = inp.split()[0]
    targets = inp.split()[1:]
    
    try: bot.channelconfig[channel]
    except: bot.channelconfig[channel] = {}

    try: 
        channel_admins = bot.channelconfig[channel]['admins']
    except: 
        channel_admins = []
        bot.channelconfig[channel]['admins'] = channel_admins

    if 'add' in command:
        for target in targets:
            if target in channel_admins:
                notice("%s is already a channel admin." % target)
            else:
                notice("%s is now a channel admin." % target)
                bot.channelconfig[channel]['admins'].append(target)
    elif 'del' in command:
        for target in targets:
            if target in channel_admins:
                notice("%s is no longer a channel admin on %s." % (target,chan))
                bot.channelconfig[channel]['admins'].remove(target)
                bot.channelconfig.write()
            else:
                notice("%s is not a channel admin." % target)
    bot.channelconfig.write()
    return


@hook.command(autohelp=False)
def admins(inp, chan=None, notice=None, bot=None):
    "admins -- Lists channel's admins."
    channel = chan.lower()
    if bot.channelconfig[channel]['admins']:
        notice("Admins on %s are: %s." % (chan, ', '.join(bot.channelconfig[channel]['admins'])))
    else:
        notice("There are no users with admin powers on %s." % chan)
    return


@hook.command("quit", autohelp=False, adminonly=True)
@hook.command(autohelp=False, adminonly=True)
def stop(inp, nick=None, conn=None):
    "stop [reason] -- Kills the bot with [reason] as its quit message."
    if inp:
        conn.cmd("QUIT", ["Killed by %s (%s)" % (nick, inp)])
    else:
        conn.cmd("QUIT", ["Killed by %s." % nick])
    time.sleep(5)
    os.execl("./uguubot", "uguubot", "stop")


@hook.command(autohelp=False, adminonly=True)
def restart(inp, nick=None, conn=None):
    "restart [reason] -- Restarts the bot with [reason] as its quit message."
    if inp:
        conn.cmd("QUIT", ["Restarted by %s (%s)" % (nick, inp)])
    else:
        conn.cmd("QUIT", ["Restarted by %s." % nick])
    time.sleep(5)
    os.execl("./uguubot", "uguubot", "restart")


@hook.command(autohelp=False, adminonly=True)
def clearlogs(inp, input=None):
    "clearlogs -- Clears the bots log(s)."
    subprocess.call(["./uguubot", "clear"])


@hook.command('request',autohelp=False, channeladminonly=True)
@hook.command(channeladminonly=True)
def join(inp, conn=None, notice=None, bot=None,):
    "join <channel> -- Joins <channel>."
    notice("Attempting to join %s..." % inp)
    conn.join(inp)

    channellist = bot.config["connections"][conn.name]["channels"]
    channellist.append(inp)
    json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)


@hook.command('leave',autohelp=False, channeladminonly=True)
@hook.command(autohelp=False, channeladminonly=True)
def part(inp, conn=None, chan=None, notice=None, bot=None,):
    "part <channel> -- Leaves <channel>." \
    "If [channel] is blank the bot will leave the " \
    "channel the command was used in."
    if inp:
        target = inp
    else:
        target = chan
    notice("Attempting to leave %s..." % target)
    conn.part(target)

    channellist = bot.config["connections"][conn.name]["channels"]
    channellist.remove(target)
    json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)


@hook.command(autohelp=False, adminonly=True)
def cycle(inp, conn=None, chan=None, notice=None):
    "cycle <channel> -- Cycles <channel>." \
    "If [channel] is blank the bot will cycle the " \
    "channel the command was used in."
    if inp:
        target = inp
    else:
        target = chan
    notice("Attempting to cycle %s..." % target)
    conn.part(target)
    conn.join(target)


@hook.command(adminonly=True)
def nick(inp, input=None, notice=None, conn=None):
    "nick <nick> -- Changes the bots nickname to <nick>."
    if not re.match("^[A-Za-z0-9_|.\-\]\[]*$", inp.lower()):
        notice("Invalid username!")
        return
    notice("Attempting to change nick to \"%s\"..." % inp)
    conn.set_nick(inp)


@hook.command(adminonly=True)
def raw(inp, conn=None, notice=None):
    "raw <command> -- Sends a RAW IRC command."
    notice("Raw command sent.")
    conn.send(inp)

@hook.command(adminonly=True)
def msg(inp, conn=None, chan=None, notice=None):
    "msg <user> <message> -- Sends a Message."
    user = inp.split()[0]
    message = inp.replace(user,'').strip()
    out = "PRIVMSG %s :%s" % (user, message)
    conn.send(out)

@hook.command(adminonly=True)
def say(inp, conn=None, chan=None, notice=None):
    "say [channel] <message> -- Makes the bot say <message> in [channel]. " \
    "If [channel] is blank the bot will say the <message> in the channel " \
    "the command was used in."
    inp = inp.split(" ")
    if inp[0][0] == "#":
        message = ""
        for x in inp[1:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :%s" % (inp[0], message)
    else:
        message = ""
        for x in inp[0:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :%s" % (chan, message)
    conn.send(out)


@hook.command("act", adminonly=True)
@hook.command(adminonly=True)
def me(inp, conn=None, chan=None, notice=None):
    "me [channel] <action> -- Makes the bot act out <action> in [channel]. " \
    "If [channel] is blank the bot will act the <action> in the channel the " \
    "command was used in."
    inp = inp.split(" ")
    if inp[0][0] == "#":
        message = ""
        for x in inp[1:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :\x01ACTION %s\x01" % (inp[0], message)
    else:
        message = ""
        for x in inp[0:]:
            message = message + x + " "
        message = message[:-1]
        out = "PRIVMSG %s :\x01ACTION %s\x01" % (chan, message)
    conn.send(out)


@hook.command(autohelp=False)
def ignored(inp, notice=None, bot=None):
    "ignored -- Lists ignored channels/nicks/hosts."
    ignorelist = bot.config["plugins"]["ignore"]["ignored"]
    if ignorelist:
        notice("Ignored channels/nicks/hosts are: %s" % ", ".join(ignorelist))
    else:
        notice("No channels/nicks/hosts are currently ignored.")
    return


@hook.command('block',adminonly=True)
@hook.command(adminonly=True)
def ignore(inp, notice=None, bot=None, config=None):
    "ignore <channel|nick|host> -- Makes the bot ignore <channel|nick|host>."
    admins = bot.config.get('admins', [])
    targets = inp.split()
    for target in targets:  
        target = target.lower()   
        if target in admins: return "%s is an admin and cannot be ignored." % inp
        ignorelist = bot.config["plugins"]["ignore"]["ignored"]
        if target in ignorelist:
            notice("%s is already ignored." % target)
        else:
            notice("%s has been ignored." % target)
            ignorelist.append(target)
            ignorelist.sort()
            json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
    return


@hook.command(adminonly=True)
def unignore(inp, notice=None, bot=None, config=None):
    "unignore <channel|nick|host> -- Makes the bot listen to"\
    " <channel|nick|host>."
    targets = inp.split()
    for target in targets:  
        target = target.lower() 
        ignorelist = bot.config["plugins"]["ignore"]["ignored"]
        if target in ignorelist:
            ignorelist.remove(target)
            ignorelist.sort()
            json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
            notice("%s has been unignored." % target)
        else:
            notice("%s is not ignored." % target)
    return


@hook.command(adminonly=True)
def set(inp, conn=None, chan=None, db=None, notice=None):
    "set <action> <item> <value> -- Admin override for setting database values. " \
    "Example: set location infinity Denver, CO" \
    "set lastfm infinity spookieboogie"

    inp = inp.split()
    try:
        action = inp[0]
        item = inp[1]
        value = ""
        for x in inp[2:]: value = value + x + " "
        value = value[:-1]
    except IndexError: 
        out = "PRIVMSG %s :Could not set %s." % (chan, action)
        notice(out)
        return

    if action and item and value:
        if 'location' in action:
            db.execute("insert or replace into locations(ircname, location) values (?,?)", (item.lower(), value))
            db.commit() 
            out = "PRIVMSG %s :Set %s for %s to %s." % (chan, action, item, value)
        if 'lastfm' in action:
            db.execute("insert or replace into usernames(ircname, lastfmname) values (?,?)", (item.lower(), value))
            db.commit() 
            out = "PRIVMSG %s :Set %s for %s to %s." % (chan, action, item, value)
    else:
        print "FAIL"
        out = "PRIVMSG %s :Could not set %s." % (chan, action)

    notice(out)

@hook.command("stfu", adminonly=True)
@hook.command("silence", adminonly=True)
@hook.command(adminonly=True)
def shutup(inp, conn=None, chan=None, notice=None):
    "shutup [channel] <user> -- Shuts the user up. "
    inp = inp.split(" ")
    if inp[0][0] == "#":
        chan = inp[0]
        user = inp[1]
        out = "MODE %s +m-voh %s %s %s" % (chan, user, user, user)
    else:
        user = inp[0]
        out = "MODE %s +m-voh %s %s %s" % (chan, user, user, user)
    notice("Shut up %s from %s..." % (user, chan))
    conn.send(out)


@hook.command(adminonly=True)
def speak(inp, conn=None, chan=None, notice=None):
    "speak [channel] <user> -- Shuts the user up. "
    inp = inp.split(" ")
    if inp[0][0] == "#":
        chan = inp[0]
        user = inp[1]
        out = "MODE %s -m+v %s" % (chan, user)
    else:
        user = inp[0]
        out = "MODE %s -m+v %s" % (chan, user)
    notice("Gave %s from %s speech..." % (user, chan))
    conn.send(out)