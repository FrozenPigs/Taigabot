from util import hook,http, database
import random
import urllib

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
def pantsumap(inp, chan=None, notice=None):
    "pantsumap -- pantsumap"
    if chan == "#pantsumen": notice(("Pantsumen Map: http://tinyurl.com/clx2qeg\r\n").encode('utf-8', 'ignore'))


@hook.command('deidle', autohelp=False)
@hook.command(autohelp=False)
def idle(inp):
    "idle -- idle"
    return 'Thats not a command you baka.'


@hook.command()
def penis(inp, conn=None, chan=None, notice=None, nick=None):
    "penis <nicks> -- Analyzes Penis's"
    url = 'http://en.inkei.net/{}'.format('!'.join(inp.split(' ')))
    return url


@hook.regex(r'^\[(.*)\]$')
@hook.command(autohelp=False)
def intensify(inp):
    "intensify <word> -- idle"
    try: word = inp.upper()
    except: word = inp.group(1).upper()
    return '\x02[{} INTENSIFIES]\x02'.format(word)


@hook.command(autohelp=False)
def hug(inp):
    "hug <nick> -- hugs someone"
    #return u'\x02♥♡♥ {} ♥♡♥\x02'.format(inp.strip())
    return '♥♡❤♡♥ {} ♥♡❤♡♥'.format(inp).decode('UTF-8')


@hook.command(autohelp=False)
def sudoku(inp, conn=None, chan=None, notice=None, nick=None, say=None):
    "up -- Makes the bot kill you in [channel]. "\
    "If [channel] is blank the bot will op you in "\
    "the channel the command was used in."
    say("Sayonara bonzai-chan...")
    conn.send(u"KICK {} {}".format(chan, nick)) 
    return


@hook.command(autohelp=False)
def increase(inp):
    "increase"
    return '\x02[QUALITY OF CHANNEL SIGNIFICANTLY INCREASED]\x02'


@hook.command(autohelp=False)
def decrease(inp):
    "decrease"
    return '\x02[QUALITY OF CHANNEL SIGNIFICANTLY DECREASED]\x02'


# HONK HONK
def citation(db,chan,nick,reason):
    fine = random.randint(1, 500)
    try: totalfines = int(database.get(db,'users','fines','nick',nick)) + fine
    except: totalfines = 0 + fine
    database.set(db,'users','fines',totalfines,'nick',nick)
    return u"PRIVMSG {} :\x01ACTION fines {} \x02${}\x02 {}. You owe: \x0304${}\x02\x01".format(chan, nick, fine, reason, totalfines)


@hook.command(autohelp=False)
def owed(inp, nick=None, conn=None, chan=None,db=None):
    if '@' in inp: nick = inp.split('@')[1].strip()
    return u'\x02{} owes: \x0304${}\x02'.format(nick,database.get(db,'users','fines','nick',nick))


@hook.command('rape', autohelp=False)
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
        'spank':'spanked',
        'rape':'raped'
    }
    # actions = (
    #     ("honk", "honked at", "honking"),
    #     ("pet", "pet", "petting"),
    #     ("diddle", "diddled", "diddling"),
    #     ("spank", "spanked", "spanking"),
    #     ("rape", "raped", "raping")
    # )

    if len(inp) == 0:
        if random.randint(1, 3) == 2: 
            out = citation(db,chan,nick,"for {}ing".format(command))
        else:
            out = u"PRIVMSG {} :\x01ACTION {}s {}\x01".format(chan, command, nick)
    else:
        randnum = random.randint(1, 4)
        if randnum == 1: 
            out = citation(db,chan,nick,"for {}ing".format(command))
        elif randnum == 2: 
            out = citation(db,chan,target,"for being too lewd and getting {}".format(actions[command]))
        else:
            out = u"PRIVMSG {} :\x01ACTION {}s {}\x01".format(chan, command, target)
    conn.send(out)



# /action uguubot bursts out laughing


# @hook.command('siid')
# @hook.command(autohelp=False)
# def sleepytime(inp, chan=None, conn=None, notice=None):
#     "kick [channel] <user> [reason] -- Makes the bot kick <user> in [channel] "\
#     "If [channel] is blank the bot will kick the <user> in "\
#     "the channel the command was used in."
#     user = 'siid'
#     out = "KICK %s %s" % (chan, user)
#     reason = "sleepytime!"
#     out = out + " :" + reason
#     notice("Attempting to kick %s from %s..." % (user, chan))
#     conn.send(out)


# @hook.command(autohelp=False,channeladminonly=True)
# def touhouradio(inp, chan=None, notice=None, bot=None):
#     "disabled -- Lists channels's disabled commands."
#     url = "http://booru.touhouradio.com/post/list/%7Bchannel%7C%23pantsumen%7D/1"
#     html = http.get_html(url)
# 
#     link = html.xpath("//div[@id='main']//a/@href")[0]
#     #COMPARE TO DB
#     image = http.unquote(re.search('.+?imgurl=(.+)&imgrefurl.+', link).group(1))
#     return image
