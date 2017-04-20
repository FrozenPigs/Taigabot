" seen.py: written by sklnd in about two beers July 2009"

import time
import re
<<<<<<< HEAD
import sys
import os
=======
import datafiles
>>>>>>> infinuguu/master

from util import hook, timesince

db_ready = False

<<<<<<< HEAD

def db_init(db, bot):
    "check to see that our db has the the seen table and return a connection."
    try:
        db.execute("create table if not exists seen(name, time, quote, chan, host, primary key(name, chan))")
    except:
        for botcon in bot.conns:
            bot.conns[botcon].cmd("QUIT", ["Restarted"])
        time.sleep(5)
        #os.execl("./bot", "bot", "restart")
        args = sys.argv[:]
        args.insert(0, sys.executable)
        os.execv(sys.executable, args)
=======
with open("plugins/data/insults.txt") as f:
    insults = [line.strip() for line in f.readlines() if not line.startswith("//")]


def db_init(db):
    "check to see that our db has the the seen table and return a connection."
    db.execute("create table if not exists seen(name, time, quote, chan, host, primary key(name, chan))")
>>>>>>> infinuguu/master
    db.commit()
    db_ready = True


def findnth(source, target, n):
    num = 0
    start = -1
    while num < n:
        start = source.find(target, start+1)
        if start == -1: return -1
        num += 1
    return start

def replacenth(source, old, new, n):
    p = findnth(source, old, n)
    if n == -1: return source
    return source[:p] + new + source[p+len(old):]


def correction(input,db,notice,say):
    splitinput = input.msg.split("/")
    nick = input.nick
    num=1
<<<<<<< HEAD
    if len(splitinput) > 3:
=======
    if len(splitinput) > 3:         
>>>>>>> infinuguu/master
        if ' ' in splitinput[3]:
            nick = splitinput[3].split(' ')[1].strip()
            splitinput[3] = splitinput[3].split(' ')[0].strip()

<<<<<<< HEAD
        if len(splitinput[3]) > 2:
=======
        if len(splitinput[3]) > 2: 
>>>>>>> infinuguu/master
            nick = splitinput[3].strip()
        else:
            if 'g' in splitinput[3]:
                num = 0
<<<<<<< HEAD
            else:
=======
            else: 
>>>>>>> infinuguu/master
                try: num = int(splitinput[3].strip())
                except: num = 1

    last_message = db.execute("select name, quote from seen where name like ? and chan = ?", (nick.lower(), input.chan.lower())).fetchone()

    if last_message:
        splitinput = input.msg.split("/")
        find = splitinput[1]
        replace = splitinput[2]
        if find in last_message[1]:
            if "\x01ACTION" in last_message[1]:
                msg = last_message[1].replace("\x01ACTION ", "/me ").replace("\x01", "")
            else:
                msg = last_message[1]

            if num == 0:
                say(u"<{}> {}".format(nick, msg.replace(find, "\x02" + replace + "\x02")))
            else:
                say(u"<{}> {}".format(nick, replacenth(msg,find,"\x02" + replace + "\x02",num)))
        #else:
            #notice(u"{} can't be found in your last message".format(find))
    else:
        if nick == input.nick:
            notice(u"I haven't seen you say anything here yet")
        else:
            notice(u"I haven't seen {} say anything here yet".format(nick))


@hook.singlethread
@hook.event('PRIVMSG', ignorebots=False)
def seen_sieve(paraml, input=None, db=None, bot=None, notice=None, say=None):
<<<<<<< HEAD
    if not db_ready: db_init(db, bot)

    if re.match(r'^(s|S)/.*/.*\S*$', input.msg):
=======
    if not db_ready: db_init(db)

    if re.match(r'^(s|S)/.*/.*\S*$', input.msg): 
>>>>>>> infinuguu/master
        correction(input,db,notice,say)
        return

    # keep private messages private
    if input.chan[:1] == "#":
<<<<<<< HEAD
        #try:
        db.execute("insert or replace into seen(name, time, quote, chan, host) values(?,?,?,?,?)", (input.nick.lower(), time.time(), input.msg.replace('\"', "").replace("'", ""), input.chan, input.mask))
        db.commit()
        #except:
        #    for botcon in bot.conns:
        #        if inp:
        #            bot.conns[botcon].cmd("QUIT", ["Restarted by {} ({})".format(nick, inp)])
        #        else:
        #            bot.conns[botcon].cmd("QUIT", ["Restarted by {}.".format(nick)])
        #    time.sleep(5)
        #    args = sys.argv[:]
        #    args.insert(0, sys.executable)
        #    os.execv(sys.executable, args)

@hook.command
def seen(inp, nick='', chan='', db=None, input=None, bot=None):
    "seen <nick> -- Tell when a nickname was last in active in one of this bot's channels."

    if input.conn.nick.lower() == inp.lower():
        return "You need to get your eyes checked."

    if inp.lower() == nick.lower():
        return "Have you looked in a mirror lately?"
=======
        db.execute("insert or replace into seen(name, time, quote, chan, host) values(?,?,?,?,?)", (input.nick.lower(), time.time(), input.msg.replace('\"', "").replace("'", ""), input.chan, input.mask))
        db.commit()
        # database.set(db,'users','mask',input.mask.lower().replace('~',''),'nick',input.nick.lower())
        # db.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}';".format(table,field,value,matchfield,matchvalue))

@hook.command
def seen(inp, nick='', chan='', db=None, input=None, conn=None, notice=None):
    "seen <nick> -- Tell when a nickname was last in active in one of this bot's channels."

    if input.conn.nick.lower() == inp.lower():
        phrase = datafiles.get_phrase(nick,insults,nick,conn,notice,chan)
        return phrase

    if inp.lower() == nick.lower():
        return phrase
>>>>>>> infinuguu/master

    #if not re.match("^[A-Za-z0-9_|.\-\]\[]*$", inp.lower()):
    #    return "I can't look up that name, its impossible to use!"

<<<<<<< HEAD
    if not db_ready: db_init(db, bot)
=======
    if not db_ready: db_init(db)
>>>>>>> infinuguu/master

    last_seen = db.execute("select name, time, quote from seen where name like ? and chan = ?", (inp, chan)).fetchone()

    if last_seen:
        reltime = timesince.timesince(last_seen[1])
        if last_seen[0] != inp.lower():  # for glob matching
            inp = last_seen[0]
        if last_seen[2][0:1] == "\x01":
<<<<<<< HEAD
            print 'notelse'
            return u'{} was last seen {} ago: * {} {}'.format(inp, reltime, inp,
                                                             last_seen[2][8:-1]).encode('utf-8')
        else:
            return u'{} was last seen {} ago saying: {}'.format(inp, reltime, last_seen[2]).encode('utf-8')
=======
            return '{} was last seen {} ago: * {} {}'.format(inp, reltime, inp,
                                                             last_seen[2][8:-1])
        else:
            return '{} was last seen {} ago saying: {}'.format(inp, reltime, last_seen[2])
>>>>>>> infinuguu/master
    else:
        return "I've never seen {} talking in this channel.".format(inp)
