# Plugin made by Lukeroge and neersighted
from util import hook


@hook.command(channeladminonly=True)
def topic(inp, conn=None, chan=None, notice=None):
    "topic [channel] <topic> -- Change the topic of a channel."
    message = inp
    inp = inp.split(" ")
    if inp[0][0] == "#":
        message = message.replace(inp[0],'').strip()
        out = "TOPIC %s :%s" % (inp[0], message)
    else:
        out = "TOPIC %s :%s" % (chan, message)
    conn.send(out)


@hook.command('k',channeladminonly=True)
@hook.command('kal',channeladminonly=True)
@hook.command(channeladminonly=True)
def kick(inp, chan=None, conn=None, notice=None):
    "kick [channel] <user> [reason] -- Makes the bot kick <user> in [channel] "\
    "If [channel] is blank the bot will kick the <user> in "\
    "the channel the command was used in."
    inp = inp.split(" ")
    if inp[0][0] == "#":
        chan = inp[0]
        user = inp[1]
        out = "KICK %s %s" % (chan, user)
        if len(inp) > 2:
            reason = ""
            for x in inp[2:]:
                reason = reason + x + " "
            reason = reason[:-1]
            out = out + " :" + reason
    else:
        user = inp[0]
        out = "KICK %s %s" % (chan, user)
        if len(inp) > 1:
            reason = ""
            for x in inp[1:]:
                reason = reason + x + " "
            reason = reason[:-1]
            out = out + " :" + reason

    notice("Attempting to kick %s from %s..." % (user, chan))
    conn.send(out)


@hook.command(channeladminonly=True)
def op(inp, conn=None, chan=None, notice=None):
    "op [channel] <user> -- Makes the bot op <user> in [channel]. "\
    "If [channel] is blank the bot will op <user> in "\
    "the channel the command was used in."
    inp = inp.split(" ")
    if inp[0][0] == "#":
        chan = inp[0]
        user = inp[1]
        out = "MODE %s +o %s" % (chan, user)
    else:
        user = inp[0]
        out = "MODE %s +o %s" % (chan, user)
    notice("Attempting to op %s from %s..." % (user, chan))
    conn.send(out)


@hook.command(channeladminonly=True)
def deop(inp, conn=None, chan=None, notice=None):
    "deop [channel] <user> -- Makes the bot deop <user> in [channel]. "\
    "If [channel] is blank the bot will deop <user> in "\
    "the channel the command was used in."
    inp = inp.split(" ")
    if inp[0][0] == "#":
        chan = inp[0]
        user = inp[1]
        out = "MODE %s -o %s" % (chan, user)
    else:
        user = inp[0]
        out = "MODE %s -o %s" % (chan, user)
    notice("Attempting to deop %s from %s..." % (user, chan))
    conn.send(out)


@hook.command(channeladminonly=True,autohelp=False)
def up(inp, conn=None, chan=None, notice=None, nick=None):
    "up -- Makes the bot op you in [channel]. "\
    "If [channel] is blank the bot will op you in "\
    "the channel the command was used in."
    out = u"MODE %s +o %s" % (chan, nick)
    notice("Attempting to op %s from %s..." % (nick,chan))
    conn.send(out)


@hook.command(channeladminonly=True,autohelp=False)
def down(inp, conn=None, chan=None, notice=None, nick=None):
    "down -- Makes the bot deop you in [channel]. "\
    "If [channel] is blank the bot will op you in "\
    "the channel the command was used in."
    out = "MODE %s -o %s" % (chan, nick)
    notice("Attempting to deop %s from %s..." % (nick,chan))
    conn.send(out)


@hook.command(channeladminonly=True)
def ban(inp, conn=None, chan=None, notice=None):
    "ban [channel] <user> -- Makes the bot ban <user> in [channel]. "\
    "If [channel] is blank the bot will ban <user> in "\
    "the channel the command was used in."
    inp = inp.split(" ")
    if inp[0][0] == "#":
        chan = inp[0]
        user = inp[1]
        out = "MODE %s +b %s" % (chan, user)
    else:
        user = inp[0]
        out = "MODE %s +b %s" % (chan, user)
    notice("Attempting to ban %s from %s..." % (user, chan))
    conn.send(out)


@hook.command(channeladminonly=True)
def unban(inp, conn=None, chan=None, notice=None):
    "unban [channel] <user> -- Makes the bot unban <user> in [channel]. "\
    "If [channel] is blank the bot will unban <user> in "\
    "the channel the command was used in."
    inp = inp.split(" ")
    if inp[0][0] == "#":
        chan = inp[0]
        user = inp[1]
        out = "MODE %s -b %s" % (chan, user)
    else:
        user = inp[0]
        out = "MODE %s -b %s" % (chan, user)
    notice("Attempting to unban %s from %s..." % (user, chan))
    conn.send(out)


@hook.command('kb',channeladminonly=True)
@hook.command(channeladminonly=True)
def kickban(inp, chan=None, conn=None, notice=None):
    "kickban [channel] <user> [reason] -- Makes the bot kickban <user> in [channel] "\
    "If [channel] is blank the bot will kickban the <user> in "\
    "the channel the command was used in."
    inp = inp.split(" ")
    if inp[0][0] == "#":
        chan = inp[0]
        user = inp[1]
        out1 = "MODE %s +b %s" % (chan, user)
        out2 = "KICK %s %s" % (chan, user)
        if len(inp) > 2:
            reason = ""
            for x in inp[2:]:
                reason = reason + x + " "
            reason = reason[:-1]
            out = out + " :" + reason
    else:
        user = inp[0]
        out1 = "MODE %s +b %s" % (chan, user)
        out2 = "KICK %s %s" % (chan, user)
        if len(inp) > 1:
            reason = ""
            for x in inp[1:]:
                reason = reason + x + " "
            reason = reason[:-1]
            out = out + " :" + reason

    notice("Attempting to kickban %s from %s..." % (user, chan))
    conn.send(out1)
    conn.send(out2)

@hook.command(channeladminonly=True)
def enable(inp, conn=None, chan=None, notice=None, bot=None):
    "enable [channel] <commands|all> -- Enables commands for a channel." \
    "(you can add/delete multiple commands at once)"
    inp = inp.lower()
    if inp[0][0] == "#": 
        chan = inp.split()[0]
        inp = inp.replace(chan,'').strip()
    channel = chan.lower()
    targets = inp.split()[0:]

    try: bot.channelconfig[channel]
    except: bot.channelconfig[channel] = {}

    try: 
        disabled_commands = bot.channelconfig[channel]['disabled_commands']
    except: 
        disabled_commands = []
        bot.channelconfig[channel]['disabled_commands'] = disabled_commands

    if 'all' in targets:
       notice("All commands are now enabled on %s." % chan)
       bot.channelconfig[chan]['disabled_commands'] = []
    else:
        for target in targets:
            if target in disabled_commands:
                notice("%s is now enabled on %s." % (target,chan))
                bot.channelconfig[channel]['disabled_commands'].remove(target)
            else:
                notice("%s is not disabled on %s." % (target,chan))
    bot.channelconfig.write()
    return

@hook.command(channeladminonly=True)
def disable(inp, conn=None, chan=None, notice=None, bot=None):
    "disable [channel] <commands> -- Disables commands for a channel." \
    "(you can add/delete multiple commands at once)"
    inp = inp.lower()
    if inp[0][0] == "#": 
        chan = inp.split()[0]
        inp = inp.replace(chan,'').strip()
    channel = chan.lower()
    targets = inp.split()[0:]

    try: bot.channelconfig[channel]
    except: bot.channelconfig[channel] = {}

    try:
        disabled_commands = bot.channelconfig[channel]['disabled_commands']
    except: 
        disabled_commands = []
        bot.channelconfig[channel]['disabled_commands'] = disabled_commands

    for target in targets:
        if target in disabled_commands:
            notice("%s is already disabled on %s." % (target,chan))
        else:
            notice("%s is now disabled on %s." % (target,chan))
            bot.channelconfig[channel]['disabled_commands'].append(target)
    bot.channelconfig.write()
    return


@hook.command(autohelp=False,channeladminonly=True)
def disabled(inp, chan=None, notice=None, bot=None):
    "disabled -- Lists channels's disabled commands."
    if bot.channelconfig[chan.lower()]['disabled_commands']:
        notice("Disabled on %s: %s." % (chan, ", ".join(bot.channelconfig[chan]['disabled_commands'])))
    else:
        notice("There is nothing disabled on %s." % chan)
    return



@hook.command(channeladminonly=True)
def flood(inp, conn=None, chan=None, notice=None, bot=None):
    "flood [channel] <number> <duration> -- Enables flood protection for a channel. " \
    "ex: .flood 3 30 -- Allows 3 commands in 30 seconds, set to 0 to disable"
    inp = inp.lower()
    if inp[0][0] == "#": 
        chan = inp.split()[0]
        inp = inp.replace(chan,'').strip()
    channel = chan.lower()
    try: bot.channelconfig[channel]
    except: bot.channelconfig[channel] = {}

    if "0 " in inp:
        bot.channelconfig[channel]['flood_protection'] = []
        notice("Flood Protection Disabled.")
    else:
        flood_num = inp.split()[0]
        flood_duration = inp.split()[1]
        bot.channelconfig[channel]['flood_protection'] = [flood_num,flood_duration]
        notice("Flood Protection limited to %s commands in %s seconds." % (flood_num,flood_duration))
    bot.channelconfig.write()
    return

@hook.command(channeladminonly=True)
def trim(inp, conn=None, chan=None, notice=None, bot=None):
    "trim [channel] <length> -- Sets trim length for parsers. " \
    "ex: .trim 150 -- Returns the first 150 characters of a parsed url"
    inp = inp.lower()
    if inp[0][0] == "#": 
        chan = inp.split()[0]
        inp = inp.replace(chan,'').strip()
    channel = chan.lower()
    try: bot.channelconfig[channel]
    except: bot.channelconfig[channel] = {}

    if "disable" in inp:
        bot.channelconfig[channel]['flood_protection'] = [0]
        notice("Parser Trimming Disabled.")
    else:
        trim_length = inp
        bot.channelconfig[channel]['trim_length'] = [trim_length]
        notice("Parser responses limited to %s." % (trim_length))
    bot.channelconfig.write()
    return
    


@hook.command(autohelp=False)
def sudoku(inp, conn=None, chan=None, notice=None, nick=None):
    "up -- Makes the bot kill you in [channel]. "\
    "If [channel] is blank the bot will op you in "\
    "the channel the command was used in."
    out = u"MODE %s +k %s" % (chan, nick)
    notice("Sayonara bonzai-chan..." % (nick,chan))
    conn.send(out)    
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