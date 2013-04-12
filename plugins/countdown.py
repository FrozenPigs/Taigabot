from util import hook
import time

countdown_is_running = False
countdown_nicks = []

def set_countdown_to_true():
    global countdown_is_running
    countdown_is_running = True

def set_countdown_to_false():
    global countdown_is_running
    countdown_is_running = False

def send(conn, chan, line):
    out = "PRIVMSG %s :\x01ACTION %s\x01" % (chan, line)
    conn.send(out)



@hook.command(autohelp=False) #, adminonly=True
def countdown(inp, bot=None, nick=None, conn=None, chan=None, notice=None):
    "countdown [seconds] -- does a countdown for the channel"

    admins = bot.config.get('admins', [])

    if countdown_is_running: return
    else: set_countdown_to_true()
    if inp: count = int(inp) + 1
    else: count = 6

    if count > 6: 
        if nick in admins:
            if count > 16: count = 16
        else: count = 6

    for cur in range(1, count):
      send(conn,chan,u'*** %s ***' % (count - cur))
      time.sleep(1)
    else:
      set_countdown_to_false()
      return u'*** GO ***'


@hook.command('readycount')
@hook.command #, adminonly=True
def readycountdown(inp, bot=None, nick=None, conn=None, chan=None, notice=None):
    "readycountdown [seconds] <nick1 nick2 nick3>-- does a countdown for the channel" \
    "The countdown will begin when all the users type .ready"

    if countdown_is_running: return
    else: set_countdown_to_true()

    admins = bot.config.get('admins', [])
    global countdown_nicks
    wait_count = 1
    inp = inp.lower().replace(',','')
    count = 0

    if inp[0][0].isdigit(): 
        count = inp.split()[0]
        countdown_nicks = inp.split()[1:]
        print inp
    else:
        countdown_nicks = inp.split()[0:]

    print countdown_nicks
    send(conn,chan,u'Countdown Started! Waiting for %s.' % ', '.join(countdown_nicks))

    while countdown_nicks:
        time.sleep(1)
        wait_count = int(wait_count) + 1
        if wait_count == 60:
            set_countdown_to_false()
            return "Countdown has expired."
            break
    
    send(conn,chan,'Ready! The countdown will begin in 5 seconds...')
    time.sleep(5)

    if count: count = int(count) + 1
    else: count = 6

    if count > 6: 
       if nick in admins:
           if count > 16: count = 16
       else: count = 6

    for cur in range(1, count):
     send(conn,chan,u'*** %s ***' % (count - cur))
     time.sleep(1)
    else:
     set_countdown_to_false()
     return u'*** GO ***'


@hook.command(autohelp=False) #, adminonly=True
def ready(inp, bot=None, nick=None,chan=None,conn=None):
    "ready-- when all users are ready the countdown will begin."

    nicks_size_start = len(countdown_nicks)
    global countdown_nicks
    countdown_nicks.remove(nick.lower())
    if nicks_size_start > len(countdown_nicks):
        if len(countdown_nicks) > 0:
            send(conn,chan,u'Waiting for: %s' % ', '.join(countdown_nicks))