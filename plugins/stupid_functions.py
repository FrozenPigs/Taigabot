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


@hook.command(autohelp=False)
def honk(inp, nick=None, conn=None, chan=None):
    "honk <person} -- Honks at someone."
    if len(inp) == 0:
        if random.randint(1, 2) == 2: 
            out = "PRIVMSG %s :\x01ACTION fines %s $%i for honking.\x01" % (chan, nick, random.randint(1, 10000))
        else:
            out = "PRIVMSG %s :\x01ACTION honks %s\x01" % (chan, nick)
    else:
        randnum = random.randint(1, 3)
        if randnum == 1: 
            out = "PRIVMSG %s :\x01ACTION fines %s $%i for honking.\x01" % (chan, nick, random.randint(1, 10000))
        elif randnum == 2: 
            out = "PRIVMSG %s :\x01ACTION fines %s $%i for being too lewd and getting honked at.\x01" % (chan, inp.strip(), random.randint(1, 10000))
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