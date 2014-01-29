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
    out = "PRIVMSG %s :\x01ACTION fines %s \x02$%i\x02 %s. You owe: \x0304$%s\x02\x01" % (chan, nick, fine, reason, totalfines)
    save_fines(db,nick,totalfines)
    return out

@hook.command(autohelp=False)
def owed(inp, nick=None, conn=None, chan=None,db=None):
    db_init(db)
    out = '\x02You owe: \x0304${}\x02'.format(get_fines(db,nick))
    return out

@hook.command('spank', autohelp=False)
@hook.command('diddle', autohelp=False)
@hook.command('pet', autohelp=False)
@hook.command(autohelp=False)
def honk(inp, nick=None, conn=None, chan=None,db=None, paraml=None):
    "honk <person} -- Honks at someone."
    target = inp.strip()
    command = paraml[-1].split(' ')[0][1:].lower()
    actions = {
        'honk':'honked at',
        'pet':'pet',
        'diddle':'diddled',
        'spank':'spanked'
    }
 
    db_init(db)
    if len(inp) == 0:
        if random.randint(1, 3) == 2: 
            out = citation(db,chan,nick,"for {}ing".format(command))
        else:
            out = "PRIVMSG {} :\x01ACTION {}s {}\x01".format(chan, command, nick)
    else:
        randnum = random.randint(1, 4)
        if randnum == 1: 
            out = citation(db,chan,nick,"for {}ing".format(command))
        elif randnum == 2: 
            out = citation(db,chan,target,"for being too lewd and getting {}".format(actions[command]))
        else:
            out = "PRIVMSG {} :\x01ACTION {}s {}\x01".format(chan, command, target)
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


@hook.command(autohelp=False)
def intensify(inp):
    "intensify <word> -- idle"
    word = inp.upper()
    return '\x02[{} INTENSIFIES]\x02'.format(word)
