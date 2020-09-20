from util import hook, database
import time


usr = ''
running = ''


@hook.command(autohelp=False)
def migrate(inp, conn=None, notice=None, nick=None, chan=None, db=None):
    """.migrate <all|value> [user] -- Migrate database value from uguubot to Taigabot. h:value for hashtags. .migrate values to see the valid values."""
    global usr
    global running
    if not inp:
        notice('[{}]: {}'.format(chan, migrate.__doc__))
        running = ''
        return
    if running == 'True':
        running = ''
        notice('[{}]: Command already running, please wait then try again.'.format(chan))
        return
    values = ['all', 'h:hashtag', 'values', 'quotes', 'weather', 'owe', 'lastfm', 'desktop', 'battlestation', 'birthday', 'waifu', 'imouto', 'husbando', 'daughteru', 'homescreen', 'myanime', 'mymanga', 'selfie', 'steam', 'greeting', 'socialmedias', 'snapchat']
    running = 'True'
    inp = inp.strip().split()
    usr = nick
    value = inp[0]
    try:
        usr = inp[-1]
        if usr in values:
            usr = nick
    except IndexError:
        pass
    if value not in values:
        if value[0:2] == 'h:':
            value = value
        else:
            notice('[{}]: Valid values are: {}'.format(chan, ', '.join(sorted(values, key=str.lower))))
            running = ''
            return
    if value == 'all':
        notice('[{}]: Doing this will overrwite commands such as .np, and .desktop, type .confirm if you want to continue.'.format(chan))
        time.sleep(5)
        if running != 'Yes':
            running = ''
    elif value == 'weather':
        weather_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'owe':
        owe_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'np' or value == 'lastfm':
        lastfm_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'desktop':
        desktop_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'battlestation':
        battlestation_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'birthday':
        birthday_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'waifu':
        waifu_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'imouto':
        imouto_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'husbando':
        husbando_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'daughteru':
        daughteru_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'homescreen':
        homescreen_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'myanime':
        myanime_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'mymanga':
        mymanga_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'selfie':
        selfie_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'steam':
        steam_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'greeting' or value == 'intro':
        greeting_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'socialmedia':
        socialmedia_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'snapchat':
        snapchat_mig(usr, conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'quotes':
        quotes_mig(usr, conn)
        notice('[{}]: Done. But probably not this one takes a while.'.format(chan))
        running = ''
    elif value[0:2] == 'h:':
        hash_mig(value[2:], conn)
        notice('[{}]: Done.'.format(chan))
        running = ''
    elif value == 'values':
        notice('[{}]: Valid values are: {}'.format(chan, ', '.join(sorted(values, key=str.lower))))
        running = ''


@hook.command
def confirm(inp, conn=None, notice=None, chan=None):
    global usr
    global running
    running = 'Yes'
    if not usr:
        return
    user = usr
    usr = ''
    weather_mig(user, conn)
    owe_mig(user, conn)
    lastfm_mig(user, conn)
    desktop_mig(user, conn)
    battlestation_mig(user, conn)
    birthday_mig(user, conn)
    waifu_mig(user, conn)
    imouto_mig(user, conn)
    husbando_mig(user, conn)
    daughteru_mig(user, conn)
    homescreen_mig(user, conn)
    myanime_mig(user, conn)
    mymanga_mig(user, conn)
    selfie_mig(user, conn)
    steam_mig(user, conn)
    greeting_mig(user, conn)
    socialmedia_mig(user, conn)
    snapchat_mig(user, conn)
    quotes_mig(user, conn)
    notice('[{}]: Done.'.format(chan))
    running = ''


def weather_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .w @ {}'.format(nick))
    time.sleep(5)


def owe_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .owe @ {}'.format(nick))
    time.sleep(5)


def lastfm_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .np @ {}'.format(nick))
    time.sleep(5)


def desktop_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .desktop @ {}'.format(nick))
    time.sleep(5)


def battlestation_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .battlestation @ {}'.format(nick))
    time.sleep(5)


def birthday_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .birthday @ {}'.format(nick))
    time.sleep(5)


def waifu_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .waifu @ {}'.format(nick))
    time.sleep(5)


def imouto_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .imouto @ {}'.format(nick))
    time.sleep(5)


def husbando_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .husbando @ {}'.format(nick))
    time.sleep(5)


def daughteru_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .daughteru @ {}'.format(nick))
    time.sleep(5)


def homescreen_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .homescreen @ {}'.format(nick))
    time.sleep(5)


def myanime_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .myanime @ {}'.format(nick))
    time.sleep(5)


def mymanga_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .mymanga @ {}'.format(nick))
    time.sleep(5)


def selfie_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .selfie @ {}'.format(nick))
    time.sleep(5)


def steam_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .steam @ {}'.format(nick))
    time.sleep(5)


def greeting_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .greeting @ {}'.format(nick))
    time.sleep(5)


def socialmedia_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .socialmedia @ {}'.format(nick))
    time.sleep(5)


def snapchat_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .snapchat @ {}'.format(nick))
    time.sleep(5)


def quotes_mig(nick, conn):
    conn.msg('swewewewe', '.msg uguubot .q {} 1'.format(nick))
    time.sleep(5)


def hash_mig(value, conn):
    conn.msg('swewewewe', '.msg uguubot #{}'.format(value))
    time.sleep(5)
