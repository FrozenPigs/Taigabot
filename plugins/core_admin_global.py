import json
import os
import re
import subprocess
import sys
import time

from util import database, hook, user


@hook.command(autohelp=False, adminonly=True)
def gadmins(inp, notice=None, bot=None):
    "admins -- Lists bot's global admins."
    if bot.config["admins"]:
        notice(u"Admins are: %s." % ", ".join(bot.config["admins"]))
    else:
        notice(u"There are no users with global admin powers.")
    return


@hook.command(adminonly=True)
def gadmin(inp, notice=None, bot=None, config=None, db=None):
    "gadmin <add|del> <nick|host> -- Make <nick|host> an global admin." \
    "(you can delete multiple admins at once)"
    inp = inp.lower()
    command = inp.split()[0]
    targets = inp.split()[1:]

    if 'add' in command:
        for target in targets:
            target = user.get_hostmask(target, db)
            if target in bot.config["admins"]:
                notice(u"%s is already a global admin." % target)
            else:
                notice(u"%s is now a global admin." % target)
                bot.config["admins"].append(target)
                bot.config["admins"].sort()
                json.dump(
                    bot.config, open('config', 'w'), sort_keys=True, indent=2)
        return
    elif 'del' in command:
        for target in targets:
            target = user.get_hostmask(target, db)
            if target in bot.config["admins"]:
                notice(u"%s is no longer a global admin." % target)
                bot.config["admins"].remove(target)
                bot.config["admins"].sort()
                json.dump(
                    bot.config, open('config', 'w'), sort_keys=True, indent=2)
            else:
                notice(u"%s is not a global admin." % target)
        return


#################################
### GDisable/GEnable Commands ###


@hook.command(permissions=["op_lock", "op"], adminonly=True, autohelp=False)
def gdisabled(inp, notice=None, bot=None, chan=None, db=None):
    """gignored -- Lists globally disabled commands."""
    if bot.config["disabled_commands"]:
        notice(u"Globally disabled commands are: %s." % ", ".join(
            bot.config["disabled_commands"]))
    else:
        notice(u"There are no globally disabled commands.")
    return


@hook.command(permissions=["op_lock", "op"], adminonly=True)
def gdisable(inp, notice=None, bot=None, chan=None, db=None):
    """gdisable <commands> -- Makes the bot globally disable a command."""
    disabledcommands = bot.config["disabled_commands"]
    targets = inp.split()
    for target in targets:
        if "gdisable" in target or "genable" in target or "core_admin" in target:
            notice(u"[Global]: {} cannot be disabled.".format(target))
        elif disabledcommands and target in disabledcommands:
            notice(u"[Global]: {} is already disabled.".format(target))
        else:
            bot.config["disabled_commands"].append(target)
            bot.config["disabled_commands"].sort()
            json.dump(
                bot.config, open('config', 'w'), sort_keys=True, indent=2)
            notice(u"[Global]: {} has been disabled.".format(target))
    return


@hook.command(permissions=["op_lock", "op"], adminonly=True)
def genable(inp, notice=None, bot=None, chan=None, db=None):
    """genable <commands] -- Enables currently globally disabled commands"""
    disabledcommands = bot.config["disabled_commands"]
    targets = inp.split()
    for target in targets:
        if disabledcommands and target in disabledcommands:
            bot.config["disabled_commands"].remove(target)
            bot.config["disabled_commands"].sort()
            json.dump(
                bot.config, open('config', 'w'), sort_keys=True, indent=2)
            notice(u"[Global]: {} has been enabled.".format(target))
        else:
            notice(u"[Global]: {} is not disabled.".format(target))
    return


# if 'all' in targets or '*' in targets:

################################
### Ignore/Unignore Commands ###


@hook.command(permissions=["op_lock", "op"], adminonly=True, autohelp=False)
def gignored(inp, notice=None, bot=None, chan=None, db=None):
    """ignored [channel]-- Lists ignored channels/nicks/hosts."""
    if bot.config["ignored"]:
        notice(u"Global ignores are: %s." % ", ".join(bot.config["ignored"]))
    else:
        notice(u"There are no global ignores.")
    return


@hook.command(permissions=["op_lock", "op"], adminonly=True, autohelp=False)
def gignore(inp, notice=None, bot=None, chan=None, db=None):
    """gignore <nick|host> -- Makes the bot ignore nick|host."""
    ignorelist = bot.config["ignored"]
    targets = inp.split()
    for target in targets:
        target = user.get_hostmask(target, db)
        if (user.is_globaladmin(target, db, bot)):
            notice(u"[Global]: {} is an admin and cannot be ignored.".format(
                inp))
        else:
            if ignorelist and target in ignorelist:
                notice(u"[Global]: {} is already ignored.".format(target))
            else:
                bot.config["ignored"].append(target)
                bot.config["ignored"].sort()
                json.dump(
                    bot.config, open('config', 'w'), sort_keys=True, indent=2)
                notice(u"[Global]: {} has been ignored.".format(target))
    return
    #         if ignorelist and target in ignorelist:
    #             notice(u"[{}]: {} is already ignored.".format(chan, target))
    #         else:
    #             ignorelist = '{} {}'.format(target,ignorelist)
    #             database.set(db,'channels','ignored',ignorelist,'chan',chan)

    #             notice(u"[{}]: {} has been ignored.".format(chan,target))
    # return


@hook.command(permissions=["op_lock", "op"], adminonly=True, autohelp=False)
def gunignore(inp, notice=None, bot=None, chan=None, db=None):
    """unignore [channel] <nick|host> -- Makes the bot listen to <nick|host>."""
    ignorelist = bot.config["ignored"]
    targets = inp.split()
    for target in targets:
        target = user.get_hostmask(target, db)
        if ignorelist and target in ignorelist:
            bot.config["ignored"].remove(target)
            bot.config["ignored"].sort()
            json.dump(
                bot.config, open('config', 'w'), sort_keys=True, indent=2)
            notice(u"[Global]: {} has been unignored.".format(target))
        else:
            notice(u"[Global]: {} is not ignored.".format(target))
    return


@hook.command(
    "quit", autohelp=False, permissions=["botcontrol"], adminonly=True)
@hook.command(autohelp=False, permissions=["botcontrol"], adminonly=True)
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
            bot.conns[botcon].cmd("QUIT", [
                "Restarted by {} ({})".format(nick, inp)
            ])
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


@hook.command(autohelp=False, permissions=["botcontrol"], adminonly=True)
def join(inp, conn=None, notice=None, bot=None):
    """join <channel> -- Joins <channel>."""
    if "0,0" in inp: return
    for target in inp.split(" "):
        key = None
        if ":" in target:
            key = target.split(":")[1]
            target = target.split(":")[0]
        if not target.startswith("#"):
            target = "#{}".format(target)
        notice(u"Attempting to join {}...".format(target))
        if key:
            conn.join(target, key)
        else:
            conn.join(target)

        channellist = bot.config["connections"][conn.name]["channels"]
        if not target.lower() in channellist:
            channellist.append(target.lower())
            json.dump(
                bot.config, open('config', 'w'), sort_keys=True, indent=2)
    return


@hook.command(autohelp=False, permissions=["botcontrol"], adminonly=True)
def part(inp, conn=None, chan=None, notice=None, bot=None):
    """part <channel> -- Leaves <channel>.
    If [channel] is blank the bot will leave the
    channel the command was used in."""
    if inp: targets = inp
    else: targets = chan

    channellist = bot.config["connections"][conn.name]["channels"]

    for target in targets.split(" "):
        if not target.startswith("#"):
            target = "#{}".format(target)
        if target in conn.channels:
            notice(u"Attempting to leave {}...".format(target))
            conn.part(target)
            channellist.remove(target.lower().strip())
            print 'Deleted {} from channel list.'.format(target)
        else:
            notice(u"Not in {}!".format(target))

    json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)
    return


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
    return


@hook.command(permissions=["botcontrol"], adminonly=True)
def nick(inp, notice=None, conn=None):
    """nick <nick> -- Changes the bots nickname to <nick>."""
    if not re.match("^[A-Za-z0-9_|.-\]\[]*$", inp.lower()):
        notice(u"Invalid username!")
        return
    notice(u"Attempting to change nick to \"{}\"...".format(inp))
    conn.set_nick(inp)
    return


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
    message = inp.replace(user, '').strip()
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
def set(inp, conn=None, chan=None, db=None, notice=None):
    "set <field> <nick> <value> -- Admin override for setting database values. " \
    "Example: set location infinity 80210 - " \
    "set lastfm infinity spookieboogie"

    inpsplit = inp.split(" ")

    if len(inpsplit) is 2:
        field = inp.split(" ")[0].strip()
        value = inp.split(" ")[1].strip()

        if 'voteban' in field or \
            'votekick' in field:
            database.set(db, 'channels', field, value, 'chan', chan)
            notice(u"Set {} to {}.".format(field, value))
            return
    elif len(inpsplit) >= 3:
        field = inp.split(" ")[0].strip()
        nick = inp.split(" ")[1].strip()
        # value = inp.replace(field,'').replace(nick,'').strip()
        value = inp.strip()
        vsplit = value.split()
        if vsplit[1:] >= 2:
            value = ' '.join(vsplit[2:])
        else:
            value = ''.join(vsplit[2:])
        if field and nick and value:
            if 'del' in value or 'none' in value: value = ''
            if 'location' in field or \
                'fines' in field or\
                'lastfm' in field or  \
                'desktop' in field or \
                'battlestation' in field or\
                'birthday' in field or\
                'waifu' in field or\
                'imouto' in field or\
                'husbando' in field or\
                'daughteru' in field or\
                'horoscope' in field or\
                'homescreen' in field or\
                'myanime' in field or\
                'mymanga' in field or\
                'selfie' in field or\
                'steam' in field or\
                'greeting' in field or\
                'seen' in field or\
                'socialmedias' in field or\
                'woeid' in field or\
                'snapchat' in field:
                #if type(value) is list: value = value[0]
                if value.lower() is 'none':
                    database.set(db, 'users', field, '', 'nick', nick)
                else:
                    database.set(db, 'users', field, value, 'nick', nick)
                notice(u"Set {} for {} to {}.".format(field, nick, value))
                return

    notice(u"Could not set {}.".format(field))
    return


@hook.command(autohelp=False, adminonly=True)
def db(inp, db=None, notice=None, chan=None):
    """db <update|init> -- Init or update the database."""
    if 'update' in inp:
        database.update(db)
        notice('[{}]: Updated databases.'.format(chan))
    elif 'init' in inp:
        database.init(db)
        notice('[{}]: Initiated databases.'.format(chan))
