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

def db_init(db):
    db.execute("create table if not exists fines(nick primary key, totalfines)")
    db.commit()

def get_fines(db, nick):
    totalfines = db.execute("select totalfines from fines where nick=lower(?)", [nick]).fetchone()
    if totalfines:
        return totalfines[0]
    else:
        return 0

def save_fines(db, nick, totalfines):
    db.execute("insert or replace into fines(nick, totalfines) values (?,?)", (nick.lower(), totalfines))
    db.commit()

def citation(db,chan,nick,reason):
    fine = random.randint(1, 500)
    totalfines = int(get_fines(db,nick)) + fine
    out = "PRIVMSG %s :\x01ACTION fines %s $%i %s. You owe: $%s\x01" % (chan, nick, fine, reason, totalfines)
    save_fines(db,nick,totalfines)
    return out
    #conn.send(out)

@hook.command(autohelp=False)
def honk(inp, nick=None, conn=None, chan=None,db=None):
    "honk <person} -- Honks at someone."
    db_init(db)
    if len(inp) == 0:
        if random.randint(1, 3) == 2: 
            out = citation(db,chan,nick,"for honking")
        else:
            out = "PRIVMSG %s :\x01ACTION honks %s\x01" % (chan, nick)
    else:
        randnum = random.randint(1, 4)
        if randnum == 1: 
            out = citation(db,chan,nick,"for honking")
        elif randnum == 2: 
            out = citation(db,chan,inp.strip(),"for being too lewd and getting honked at")
        else:
            out = "PRIVMSG %s :\x01ACTION honks %s\x01" % (chan, inp.strip())
    conn.send(out)

@hook.command(autohelp=False)
def pet(inp, nick=None, conn=None, chan=None,db=None):
    "pet <person} -- Pets someone."
    db_init(db)
    if len(inp) == 0:
        if random.randint(1, 3) == 2: 
            out = citation(db,chan,nick,"for petting")
        else:
            out = "PRIVMSG %s :\x01ACTION pets %s\x01" % (chan, nick)
    else:
        randnum = random.randint(1, 4)
        if randnum == 1: 
            out = citation(db,chan,nick,"for petting")
        elif randnum == 2: 
            out = citation(db,chan,inp.strip(),"for being too lewd and getting pet.")
        else:
            out = "PRIVMSG %s :\x01ACTION pets %s\x01" % (chan, inp.strip())
    conn.send(out)

@hook.command(autohelp=False)
def diddle(inp, nick=None, conn=None, chan=None,db=None):
    "diddle <person} -- Diddles someone."
    db_init(db)
    if len(inp) == 0:
        if random.randint(1, 3) == 2: 
            out = citation(db,chan,nick,"for diddling")
        else:
            out = "PRIVMSG %s :\x01ACTION diddles %s\x01" % (chan, nick)
    else:
        randnum = random.randint(1, 4)
        if randnum == 1: 
            out = citation(db,chan,nick,"for diddling")
        elif randnum == 2: 
            out = citation(db,chan,inp.strip(),"for being too lewd and getting diddled.")
        else:
            out = "PRIVMSG %s :\x01ACTION diddles %s\x01" % (chan, inp.strip())
    conn.send(out)


@hook.command(autohelp=False)
def pantsumap(inp, chan=None, notice=None):
    "pantsumap -- pantsumap"
    if chan == "#pantsumen":
        notice(("Pantsumen Map: http://tinyurl.com/clx2qeg\r\n").encode('utf-8', 'ignore'))


@hook.command('deidle', autohelp=False)
@hook.command(autohelp=False)
def idle(inp):
    "idle -- idle"
    return 'Thats not a command you baka.'
