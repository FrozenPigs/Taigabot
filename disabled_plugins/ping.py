# ping plugin by neersighted
from util import hook
import time
import subprocess
import re
import os



@hook.command('pingme', autohelp=False)
@hook.command(autohelp=False)
def ping(inp, nick=None, chan=None, conn=None, notice=None, reply=None):
    "version <nick> -- Returns version "
    import core_ctcp
    if '.' in inp:
        return pingip(inp,reply)
    else:
        inp = inp.split(" ")
        user = inp[0]
        if not user: user=nick
        #curtime = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds())
        # print len(ctcpcache)
        curtime = time.time()
        core_ctcp.ctcpcache.append(("PING",user, chan))
        # ctcpcache_timer
        conn.send(u"PRIVMSG {} :\x01PING {}\x01".format(user, str(curtime)))
    return


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
