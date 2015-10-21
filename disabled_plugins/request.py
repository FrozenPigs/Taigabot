import time
import re
from util import hook, timesince
db_ready=False

def db_init(db):
    "check to see that our db has the request table and return a dbection."
    global db_ready
    db.execute("create table if not exists requests"
                "(user_from, message, chan, time,"
                "primary key(message))")
    db.commit()
    db_ready=True
    print "Request Database Ready"

    return db


def get_requests(db):
    return db.execute("select user_from, message, time, chan from requests"
                         " order by time").fetchall()


@hook.singlethread
@hook.event('PRIVMSG')
def requestinput(paraml, input=None, notice=None, db=None, bot=None, nick=None, conn=None):
    if 'showrequests' in input.msg.lower():
        return

    if not db_ready: db_init(db)

    requests = get_requests(db)

    if requests:
        user_from, message, time, chan = requests[0]
        reltime = timesince.timesince(time)

        reply = "{} sent a request {} ago from {}: {}".format(user_from, reltime, chan, message)
        if len(requests) > 1:
            reply += " (+%d more, %sshowtells to view)" % (len(requests) - 1, conn.conf["command_prefix"])

        if 'del' in inp:
            db.execute("delete from requests where user_from=? and message=?", (user_from, message))
            db.commit()
        notice(reply)


@hook.command(adminonly=True, autohelp=False)
def showrequests(inp, nick='', chan='', notice=None, db=None, bot=None):
    "showrequests [del nick/all] -- View all pending requests (sent in a notice)."
    gadmins = bot.config['admins']
    admins = []

    for admin in gadmins:
        admin = admin.split('@')
        admins.append(admin[0])
    admins = " ".join(admins)

    if nick not in admins:
        return
    else:
        if not db_ready: db_init(db)

        requests = get_requests(db)
        print requests

        if not requests:
            notice("You have no pending tells.")
            return

        for request in requests:
            user_from, message, time, chan = request
            past = timesince.timesince(time)
            notice("%s sent you a message %s ago from %s: %s" % (user_from, past, chan, message))

        if 'del' in inp:
            inp = inp.split(" ")
            if inp[1] == 'all':
                db.execute("delete from requests where user_from=?",
                            (user_from,))
                db.commit()
            else:
                db.execute("delete from requests where user_from=?",
                            (inp[1],))
                db.commit()

@hook.command
def request(inp, nick='', chan='', db=None, input=None, notice=None):
    "request <command/fix> -- Relay <command/fix> to gadmins."
    query = inp.split(' ', 1)

    if len(query) != 1:
        notice(request.__doc__)
        return

    message = query[0].strip()
    user_from = nick

    if chan.lower() == user_from.lower():
        chan = 'a pm'

    if not db_ready: db_init(db)

    try:
        db.execute("insert into requests(user_from, message, chan, time) values(?,?,?,?)",
                   (user_from, message, chan, time.time()))
        db.commit()
    except db.IntegrityError:
        notice("Request has already been queued.")
        return

    notice("Your request will be sent!")
