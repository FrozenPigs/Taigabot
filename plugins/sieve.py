import re
from util import hook
import os
import time
import inspect
import json

filename = 'flood'
if not os.path.exists(filename): open(filename, 'w').write(inspect.cleandoc(r'''{}'''))

def check_hostmask(input, matchlist):
     user_mask = input.mask.lower().replace('~','').lower()
     for match in matchlist:
         match_mask = match.replace('*','.+').lower()
         if bool(re.search(match_mask,user_mask)): return True


def is_admin(input,bot):
    admins = bot.config.get('admins', [])
    if input.nick.lower().replace('~','') in admins or check_hostmask(input,admins): return True
        

def is_channel_admin(input,bot):
    try: channel_admins = bot.channelconfig[input.chan.lower()]['admins']
    except: channel_admins = " "
    if input.nick.lower().replace('~','') in channel_admins or check_hostmask(input,channel_admins): return True


@hook.sieve
def ignoresieve(bot, input, func, type, args):
    """ blocks input from ignored channels/nicks/hosts """
    ignorelist = bot.config["plugins"]["ignore"]["ignored"]
    # don't block input to event hooks
    if type == "event":
        return input
    if input.chan.lower() in ignorelist \
       or input.nick.lower().replace('~','') in ignorelist \
       or input.mask.lower().replace('~','').lower() in ignorelist:
        if input.command == "PRIVMSG" and input.lastparam[1:] == "unignore":
            return input
        else:
            return None
    return input


@hook.sieve
def sieve_suite(bot, input, func, kind, args):
    if input.command == 'PRIVMSG' and\
       input.nick.endswith('bot') and args.get('ignorebots', True):
            return None

    try: disabled_channel_commands = bot.channelconfig[input.chan.lower()]['disabled_commands']
    except: disabled_channel_commands = " "
    
    try: flood_protection = bot.channelconfig[input.chan.lower()]['flood_protection']
    except: flood_protection = None

    if kind == "command":
        if input.trigger in bot.config.get('disabled_commands', []):
            return None

        if input.trigger in disabled_channel_commands:
            print "Rejected: %s on %s" % (input.trigger,input.chan)
            return None

    fn = re.match(r'^plugins.(.+).py$', func._filename)
    if fn and fn.group(1).lower() in bot.config.get('disabled_plugins', []):
        return None
    if fn and fn.group(1).lower().strip() in disabled_channel_commands:
        print "Rejected: %s on %s" % (fn.group(1),input.chan)
        return None

    acl = bot.config.get('acls', {}).get(func.__name__)
    if acl:
        if 'deny-except' in acl:
            allowed_channels = map(unicode.lower, acl['deny-except'])
            if input.chan.lower() not in allowed_channels:
                return None
        if 'allow-except' in acl:
            denied_channels = map(unicode.lower, acl['allow-except'])
            if input.chan.lower() in denied_channels:
                return None

    if args.get('channeladminonly', False):
        if not is_admin(input,bot) and not is_channel_admin(input,bot):
            input.notice("Sorry, you are not allowed to use this command.")
            return None
    elif args.get('adminonly', False):
        if not is_admin(input,bot) and not is_channel_admin(input,bot):
            input.notice("Sorry, you are not allowed to use this command.")
            return None
    else:
        #flood protection
        if kind == "command" and flood_protection:
            flood_num = flood_protection[0]
            flood_duration = flood_protection[1]
            now = time.time()
            flood = json.load(open(filename))
            try: 
                user = flood[input.nick]
            except: 
                user = []
                flood[input.nick] = user

            flood[input.nick].append(now)

            for x in flood[input.nick]:
                if now - x > int(flood_duration):
                    flood[input.nick].remove(x)

            json.dump(flood, open(filename, 'w'), sort_keys=True, indent=2)

            if len(flood[input.nick]) > (int(flood_num) + 1):
                input.notice("Flood detected. Please wait 30 seconds.")
                return None

    return input

