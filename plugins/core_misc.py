import socket
import time
import re
import json
# import datetime

from util import hook, user, database

socket.setdefaulttimeout(10)

nick_re = re.compile(":(.+?)!")


# Identify to NickServ (or other service)
@hook.event('004')
def onjoin(paraml, conn=None, bot=None):
    nickserv_password = conn.conf.get('nickserv_password', '')
    nickserv_name = conn.conf.get('nickserv_name', 'nickserv')
    nickserv_command = conn.conf.get('nickserv_command', 'IDENTIFY %s')
    if nickserv_password:
        if nickserv_password in bot.config['censored_strings']:
            bot.config['censored_strings'].remove(nickserv_password)
        conn.msg(nickserv_name, nickserv_command % nickserv_password)
        bot.config['censored_strings'].append(nickserv_password)
        time.sleep(1)

    # Set bot modes
    mode = conn.conf.get('mode')
    if mode:
        conn.cmd('MODE', [conn.nick, mode])

    # Join config-defined channels
    for channel in conn.channels:
        conn.join(channel)
        time.sleep(1)

    print "Bot ready."
    

# Auto-join on Invite (Configurable, defaults to True)
@hook.event('INVITE')
def invite(paraml, conn=None, bot=None):
    invite_join = conn.conf.get('invite_join', True)
    if invite_join:
        conn.join(paraml[-1])
        channellist = bot.config["connections"][conn.name]["channels"]
        channellist.append(paraml[-1].lower())
        json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)


@hook.event("KICK")
def onkick(paraml, conn=None, chan=None, bot=None):
    # if the bot has been kicked, remove from the channel list
    # conn.channels.remove(chan)
    if paraml[1] == conn.nick:
        auto_rejoin = conn.conf.get('auto_rejoin', False)
        if auto_rejoin:
            conn.join(paraml[0])
        else:
            channellist = bot.config["connections"][conn.name]["channels"]
            channellist.remove(paraml[0])
            json.dump(bot.config, open('config', 'w'), sort_keys=True, indent=2)


@hook.event("JOIN")
def onjoined(inp,input=None, conn=None, chan=None,raw=None, db=None):
    database.set(db,'users','mask',input.mask.lower().replace('~',''),'nick',input.nick.lower())
    mask = user.format_hostmask(input.mask)
    disabled_commands = database.get(db,'channels','disabled','chan',chan)
    if not disabled_commands: disabled_commands = ""
    
    if not 'banlist' in disabled_commands:
        #check if bans
        banlist = database.get(db,'channels','bans','chan',chan)
        if banlist and mask in banlist:
            conn.send(u"MODE {} {} *{}".format(input.chan, '+b', mask))
            conn.send(u"KICK {} {} :{}".format(input.chan, input.nick, 'I dont think so Tim.'))

    if not 'autoop' in disabled_commands:
        #check if ops
        autoop = database.get(db,'channels','autoop','chan',chan)
        if autoop: autoops = database.get(db,'channels','admins','chan',chan)
        else: autoops = database.get(db,'channels','autoops','chan',chan)
        
        if autoops and mask in autoops:
            conn.send(u"MODE {} {} {}".format(input.chan, '+o', input.nick))

    if not 'greeting' in disabled_commands:
        # send greeting
        greeting = database.get(db,'users','greeting','nick',input.nick)

        if greeting: return greeting


@hook.event("PART")
def onpart(inp,input=None, conn=None, chan=None,raw=None, db=None):
    database.set(db,'users','mask',input.mask.lower().replace('~',''),'nick',input.nick.lower())


@hook.event("NICK")
def onnick(paraml, conn=None, raw=None):
    old_nick = nick_re.search(raw).group(1)
    new_nick = str(paraml[0])
    if old_nick == conn.nick:
        conn.nick = new_nick
        print "Bot nick changed from '{}' to '{}'.".format(old_nick, new_nick)


@hook.singlethread
@hook.event('004')
def keep_alive(paraml, conn=None):
    keepalive = conn.conf.get('keep_alive', False)
    if keepalive:
        while True:
            conn.cmd('PING', [conn.nick])
            time.sleep(60)
