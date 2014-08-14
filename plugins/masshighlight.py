import re
from util import hook, database, user

global userlist
userlist = {}

@hook.event('353')
def onnames(input, conn=None, bot=None):
    global userlist
    inp = re.sub('[~&@+%,\.]', '', ' '.join(input))
    chan,users = re.match(r'.*#(\S+)(.*)', inp.lower()).group(1, 2)
    try: userlist[chan]
    except: userlist[chan] = []
    userlist[chan] = set(userlist[chan])|set(users.split(' ')) 


@hook.event("JOIN")
def onjoined_addhighlight(inp,input=None, conn=None, chan=None,raw=None):
    global userlist
    try: userlist[input.chan.lower().replace('#','')].add(input.nick.lower())
    except: return     
    

@hook.sieve
def highlight_sieve(bot, input, func, kind, args):
    fn = re.match(r'^plugins.(.+).py$', func._filename)
    if fn.group(1) == 'seen' or \
       fn.group(1) == 'tell' or\
       fn.group(1) == 'ai' or \
       fn.group(1) == 'core_ctcp': return input

    global userlist
    try: users = userlist[input.chan.lower().replace('#','')]
    except: return input
    inp = set(re.sub('[#~&@+%,\.]', '', input.msg.lower()).split(' '))
    if len(users & inp) > 3: 
        globaladmin = user.is_globaladmin(input.mask, input.chan, bot) 
        db = bot.get_db_connection(input.conn)
        channeladmin = user.is_channeladmin(input.mask, input.chan, db)
        if not globaladmin and not channeladmin:
            if len(users & inp) > 5: 
                input.conn.send(u"MODE {} +b *!*{}".format(input.chan, user.format_hostmask(input.mask)))
            input.conn.send(u"KICK {} {} :MASSHIGHLIGHTING FAGGOT GET #REKT".format(input.chan, input.nick))
    return input




@hook.command(autohelp=False,adminonly=True)
def users(inp, nick=None,chan=None,notice=None):
    notice(' '.join(userlist[chan.replace('#','')]))
    notice('Users: {}'.format(len( userlist[chan.replace('#','')])))


@hook.command(autohelp=False,adminonly=True)
def getusers(inp, conn=None,chan=None):
    if inp: chan = inp
    conn.send('NAMES {}'.format(chan))

    
### dev ###
# @hook.command(autohelp=False,adminonly=True)
# def testcompare(inp, conn=None,chan=None, notice=None):
#     users = 'greenbagels ChanStat Pinyin austin j4jackj uguubot infinity fappyhour takoyaki unfinity themadman Knish Onee-chan'.split(' ')
#     inp = 'infinity uguubot themadman josh test2 test3'.split(' ')
#     a = set(users)
#     b = set(inp)
#     notice(' '.join(a|b))
