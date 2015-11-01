# Plugin by neersighted
import time
import getpass
import re
from util import hook,database, user

# CTCP responses
@hook.regex(r'^\x01VERSION\x01$')
def ctcp_version(inp, notice=None):
    notice('\x01VERSION: Skynet v0.99')


@hook.regex(r'^\x01PING\x01$')
def ctcp_ping(inp, notice=None):
    notice('\x01PING: PONG')


@hook.regex(r'^\x01TIME\x01$')
def ctcp_time(inp, notice=None):
    notice('\x01TIME: The time is: %s' % time.strftime("%r", time.localtime()))


@hook.regex(r'^\x01FINGER\x01$')
def ctcp_finger(inp, notice=None):
    notice('\x01FINGER: Username is: $s' % getpass.getuser())

global ctcpcache
ctcpcache = []

# def ctcpcache_timer():
#     print "Running"
#     x = 10
#     while x > 0:
#         print x
#         x = x-1
#         time.sleep(1)
#     ctcpcache = []


@hook.command(adminonly=True)
def ctcp(inp, conn=None, chan=None, notice=None):
    "ctcp <destination> <command> -- Send a CTCP command"
    inp = inp.split(" ")
    destination = inp[0]
    command = inp[1]
    command = command.upper()
    result = conn.send('PRIVMSG {} :\x01{}\x01'.format( destination, command ) )


@hook.command('ver', autohelp=False)
@hook.command(autohelp=False)
def version(inp, nick=None, chan=None, conn=None, notice=None):
    "version <user> -- Returns version "
    inp = inp.split(" ")
    user = inp[0]
    if not user: user=nick
    if 'uguubot' in user: return '[VERSION] uguubot: SkyNet 0.99 kawaii disrespecting humanitys freedom edition'
    # ctcpcache_timer
    ctcpcache.append(("VERSION",user, chan))
    conn.send(u"PRIVMSG {} :\x01VERSION\x01".format(user))
    return

@hook.command('pingme', autohelp=False)
@hook.command(autohelp=False)
def ping(inp, nick=None, chan=None, conn=None, notice=None, reply=None):
    "version <nick> -- Returns version "
    if '.' in inp:
        return pingip(inp,reply)
    else:
        inp = inp.split(" ")
        user = inp[0]
        if not user: user=nick
        #curtime = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())
        # print len(ctcpcache)
        curtime = time.time()
        ctcpcache.append(("PING",user, chan))
        # ctcpcache_timer
        conn.send(u"PRIVMSG {} :\x01PING {}\x01".format(user, str(curtime)))
    return

import subprocess
import os
ping_regex = re.compile(r"(\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)")

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

    reply("Attempting to ping %s %s times..." % (host, count))

    pingcmd = subprocess.check_output(["ping", "-c", count, host])
    if "request timed out" in pingcmd or "unknown host" in pingcmd:
        return "error: could not ping host"
    else:
        m = re.search(ping_regex, pingcmd)
        return "min: %sms, max: %sms, average: %sms, range: %sms, count: %s" \
        % (m.group(1), m.group(3), m.group(2), m.group(4), count)


@hook.singlethread
@hook.event('*')
def ctcp_event(paraml, input=None, bot=None, conn=None):
    inpkind = input.msg.split(" ")[0].strip()
    if re.search("VERSION", inpkind, re.I) or re.search("PING", inpkind, re.I):
        inpnick = filter(None, input.nick)
        inpresult = input.msg.replace(inpkind,'').replace('\x01','').strip()
        if ctcpcache:
            for x in ctcpcache:
                kind,nick,channel = (x[0], x[1], x[2]) #"VERSION",nick, chan
                # print "{} {} {}".format(kind,nick,channel )
                if re.search(kind, inpkind, re.I) and re.search(re.escape(nick), inpnick, re.I): #.replace('[','\[').replace(']','\]')
                    ctcpcache.remove(x)
                    if kind == "VERSION":
                        conn.send(u"PRIVMSG {} :[{}] {}: {}".format(channel, kind, nick, inpresult))
                        return
                    elif kind == "PING":

                        curtime = time.time()
                        senttime = re.search(r'\d+\.\d+',inpresult)
                        if senttime:
                            diff = (curtime - float(senttime.group(0)))
                            if diff <= 1:
                                conn.send(u"PRIVMSG {} :[{}] {}: {} ms".format(channel, kind, nick, diff*1000))
                            else:
                                conn.send(u"PRIVMSG {} :[{}] {}: {} seconds".format(channel, kind, nick, diff))
                            return
                        else:
                            #conn.send(u"PRIVMSG {} :[{}] {}: Infinite. Enable CTCP Responses you baka.".format(channel, kind, nick))
                            return
                        #diff.seconds/60



                        # diff = (curtime - float(re.search(r'\d+\.\d+',inpresult).group(0)))
                        # conn.send(u"PRIVMSG {} :[{}] {}: {}ms".format(channel, kind, nick, diff))
                        # return
                        #diff.seconds/60
    return


@hook.command #(channeladminonly=True)
def host(inp, nick=None, conn=None, db=None):
    # return user.get_hostmask(inp,db)
    if not inp: inp = nick
    db_host = database.get(db,'users','mask','nick',inp)
    if inp is db_host: db_host = database.get(db,'seen','host','name',inp)
    return "{}: {}".format(inp,db_host)


@hook.command #(channeladminonly=True)
def fhost(inp, nick=None, conn=None, db=None):
    if not inp: inp = nick
    return user.get_hostmask(inp,db)




@hook.command
def trolltest(inp, msg=None, nick=None):
    if nick == "Havixil":
        msg('[=]quitchannels')
    else:
        msg('why would i want to troll {}?'.format(nick))


#names
# @hook.command(permissions=["op_rem", "op"], channeladminonly=True)
# def names(inp, chan=None, conn=None):
#     """names [channel] -- Gets Names."""
#     inp,chan = get_chan(inp,chan)
#     test = conn.send(u"NAMES {}:".format(chan))
#     return test

# @hook.command(channeladminonly=True)
# def host(inp,db=None):
#     "userhost -- Returns a nicks userhost"
#     #db.execute("create table if not exists seen(name, time, quote, chan, host, primary key(name, chan))")
#     #db.commit()
#     nick = inp.strip().replace('~','').lower()
#     print nick
#     db_host = database.get(db,'users','mask','nick',nick)
#     print db_host
#     if nick is db_host: db_host = database.get(db,'seen','host','name',nick)

#     if db_host.count('.') == 1:
#         hostmatch = re.search(r"^(.+@)(.+\.)(\w+)$", db_host, re.I)
#         userhost = '{}{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3))
#     if db_host.count('.') == 2:
#         hostmatch = re.search(r"^(.+@)(.+\.)(.+\.)(.+)$", db_host, re.I)
#         userhost = '{}{}{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3),hostmatch.group(4))
#     elif db_host.count('.') >= 3:
#         # ^(.+@).*\b(\w+\.)(\w+\.)(\w+)$
#         hostmatch = re.search(r"^(.+@).+\.(.+\.)(.+\.)(.+)$", db_host, re.I)
#         userhost = '{}*{}{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3),hostmatch.group(4))
#     return userhost.lower()
#     #except:
#     #    return inp.lower()

# @hook.regex(r'.*- VERSION.*')
# def versionreply(inp):
#     print "test2"


# @hook.event('PING')
# def ctcp_pingme(inp, notice=None):
#     print "test"
#     print match.group(1)
