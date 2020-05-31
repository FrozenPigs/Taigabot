# Plugin by neersighted
import time
import re
from util import hook, database, user

# used in pingip
import subprocess
import os
ping_regex = re.compile(r"(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")  # TODO ipv6

global ctcpcache
ctcpcache = []


# CTCP responses
@hook.regex(r'^\x01VERSION\x01$')
def ctcp_version(inp, notice=None):
    notice('\x01VERSION Skynet v0.99\x01')


@hook.regex(r'^\x01PING')
def ctcp_ping(inp, notice=None):
    msg = ' '.join(inp.string.split()[1:])
    notice(u'\x01PING {}'.format(msg))


@hook.regex(r'^\x01TIME\x01$')
def ctcp_time(inp, notice=None):
    now = time.strftime("%r", time.localtime())
    notice('\x01TIME The time is: {}\x01'.format(now))


@hook.regex(r'^\x01FINGER\x01$')
def ctcp_finger(inp, notice=None):
    notice('\x01FINGER pls no\x01')


@hook.command(adminonly=True)
def ctcp(inp, conn=None, chan=None, notice=None):
    "ctcp <destination> <command> -- Send a CTCP command"
    inp = inp.split(" ")
    destination = inp[0]
    command = inp[1]
    command = command.upper()
    conn.send(u'PRIVMSG {} :\x01{}\x01'.format(destination, command))


@hook.command('ver', autohelp=False)
@hook.command(autohelp=False)
def version(inp, nick=None, chan=None, conn=None, notice=None):
    "version <user> -- Returns version "
    inp = inp.split(" ")
    user = inp[0]
    if not user:
        user = nick
    if 'uguubot' in user:
        return '[VERSION] uguubot: SkyNet 0.99 kawaii disrespecting humanitys freedom edition'
    # ctcpcache_timer
    ctcpcache.append(("VERSION", user, chan))
    conn.send(u"PRIVMSG {} :\x01VERSION\x01".format(user))
    return


@hook.command('pingme', autohelp=False)
@hook.command(autohelp=False)
def ping(inp, nick=None, chan=None, conn=None, notice=None, reply=None):
    "version <nick> -- Returns version "
    if '.' in inp:
        return pingip(inp, reply)
    else:
        inp = inp.split(" ")
        user = inp[0]
        if not user:
            user = nick
        curtime = time.time()
        ctcpcache.append(("PING", user, chan))
        # ctcpcache_timer
        conn.send(u"PRIVMSG {} :\x01PING {}\x01".format(user, str(curtime)))
    return


@hook.command(adminonly=True)
def pingip(inp, reply=None):
    "ping <host> [count] -- Pings <host> [count] times."

    if os.name == "nt":
        return "Sorry, this command is not supported on Windows systems."

    args = inp.split(' ')
    host = args[0]

    # check for a seccond argument and set the ping count
    if len(args) > 1:
        count = int(args[1])
        if count > 20:
            count = 20
    else:
        count = 5

    count = str(count)

    host = re.sub(r'([^\s\w\.])+', '', host)

    reply("Attempting to ping {} {} times...".format(host, count))

    try:
        pingcmd = subprocess.check_output(["ping", "-c", count, host])
    except Exception as e:
        print '[!] error while executing a system command'
        print e
        return 'error: ping command exited unexpectedly'

    if "request timed out" in pingcmd or "unknown host" in pingcmd:
        return "error: could not ping host"
    else:
        m = re.search(ping_regex, pingcmd)
        return "min: {}ms, max: {}ms, average: {}ms, range: {}ms, count: {}".format(
            m.group(1), m.group(3), m.group(2), m.group(4), count)


@hook.singlethread
@hook.event('*')
def ctcp_event(paraml, input=None, bot=None, conn=None):
    inpkind = input.msg.split(" ")[0].strip()
    if re.search("VERSION", inpkind, re.I) or re.search("PING", inpkind, re.I):
        inpnick = filter(None, input.nick)
        inpresult = input.msg.replace(inpkind, '').replace('\x01', '').strip()
        if ctcpcache:
            for x in ctcpcache:
                kind, nick, channel = (x[0], x[1], x[2])
                if re.search(kind, inpkind, re.I) and re.search(re.escape(nick), inpnick, re.I):
                    ctcpcache.remove(x)

                    if kind == "VERSION":
                        conn.send(u"PRIVMSG {} :[{}] {}: {}".format(channel, kind, nick, inpresult))
                        return
                    elif kind == "PING":
                        curtime = time.time()
                        senttime = re.search(r'\d+\.\d+', inpresult)
                        if senttime:
                            diff = (curtime - float(senttime.group(0)))
                            if diff <= 1:
                                conn.send(u"PRIVMSG {} :[{}] {}: {} ms".format(channel, kind, nick, diff * 1000))
                            else:
                                conn.send(u"PRIVMSG {} :[{}] {}: {} seconds".format(channel, kind, nick, diff))
                            return
                        else:
                            return
    return


@hook.command
def host(inp, nick=None, conn=None, db=None):
    if not inp:
        return 'Your host is ' + user.get_hostmask(nick, db)
    db_host = database.get(db, 'users', 'mask', 'nick', inp)
    if inp is db_host:
        db_host = database.get(db, 'seen', 'host', 'name', inp)
    return "{}: {}".format(inp, db_host)


@hook.command
def fhost(inp, nick=None, conn=None, db=None):
    if not inp:
        inp = nick
    return user.get_hostmask(inp, db)


@hook.command
def trolltest(inp, msg=None, nick=None):
    if nick == "Havixil":
        return '[=]quitchannels'
    else:
        return u'why would i want to troll {}?'.format(nick)
