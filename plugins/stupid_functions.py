from util import hook
import random

@hook.regex(r'^(same)$')
def same(inp,bot=None,chan=None):
    "<word>? -- Shows what data is associated with <word>."
    try: disabled_channel_commands = bot.channelconfig[chan.lower()]['disabled_commands']
    except: disabled_channel_commands = " "
    if 'same' in disabled_channel_commands: return None
    if random.randint(1, 5) == 3: 
        return 'butts'
    else:
        return 'same'
    

@hook.regex(r'^(HUEHUEHUE)$')
@hook.regex(r'^(huehuehue)$')
def hue(inp,bot=None,chan=None):
    "<word>? -- Shows what data is associated with <word>."
    try: disabled_channel_commands = bot.channelconfig[chan.lower()]['disabled_commands']
    except: disabled_channel_commands = " "
    if 'hue' in disabled_channel_commands: return None
    return inp.group(0)

@hook.regex(r'^(TETETE)$')
@hook.regex(r'^(tetete)$')
def tetete(inp, nick=None,bot=None,chan=None):
    "<word>? -- Shows what data is associated with <word>."
    try: disabled_channel_commands = bot.channelconfig[chan.lower()]['disabled_commands']
    except: disabled_channel_commands = " "
    if 'tetete' in disabled_channel_commands: return None
    return 'tetete %s%s%s' % (nick, nick, nick)


# def honk_db_init(db):
#     "check to see that our db has the tell table and return a dbection."
#     db.execute("create table if not exists tell"
#                 "(user_to, user_from, message, chan, time,"
#                 "primary key(user_to, message))")
#     db.commit()

#     return db


# def get_tells(db, user_to):
#     return db.execute("select user_from, message, time, chan from tell where"
#                          " user_to=lower(?) order by time",
#                          (user_to.lower(),)).fetchall()

@hook.command(autohelp=False)
def honk(inp, nick=None, conn=None, chan=None):
    "honk <person} -- Honks at someone."
    if len(inp) == 0:
        if random.randint(1, 3) == 2: 
            out = "PRIVMSG %s :\x01ACTION fines %s $%i for honking.\x01" % (chan, nick, random.randint(1, 500))
        else:
            out = "PRIVMSG %s :\x01ACTION honks %s\x01" % (chan, nick)
    else:
        randnum = random.randint(1, 4)
        if randnum == 1: 
            out = "PRIVMSG %s :\x01ACTION fines %s $%i for honking.\x01" % (chan, nick, random.randint(1, 500))
        elif randnum == 2: 
            out = "PRIVMSG %s :\x01ACTION fines %s $%i for being too lewd and getting honked at.\x01" % (chan, inp.strip(), random.randint(1, 500))
        else:
            out = "PRIVMSG %s :\x01ACTION honks %s\x01" % (chan, inp.strip())
        
    conn.send(out)

@hook.command(autohelp=False)
def lewd(inp):
    "lewd -- LEWD"
    return 'ヽ(◔ ◡ ◔)ノ.･ﾟ*｡･+☆LEWD☆'.decode('UTF-8')

@hook.command(autohelp=False)
def pantsumap(inp, chan=None, notice=None):
    "lewd -- LEWD"
    if chan == "#pantsumen":
        notice(("Pantsumen Map: http://tinyurl.com/clx2qeg\r\n").encode('utf-8', 'ignore'))


@hook.command(autohelp=False)
def lcs(inp, chan=None, notice=None):
    "Some LoL shit..."
    return 'http://www.twitch.tv/riotgames?utm_campaign=live_embed_click&utm_source=na.lolesports.com'
