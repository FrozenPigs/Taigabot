import re

from util import hook

#def parse_mask(inp):
    #if '*' in inp:
        #check if inp at [0][0]
        #check if inp at last
    #else

@hook.sieve
def ignoresieve(bot, input, func, type, args):
    """ blocks input from ignored channels/nicks/hosts """
    ignorelist = bot.config["plugins"]["ignore"]["ignored"]
    # don't block input to event hooks
    if type == "event":
        return input
    else:
        print "not-event"
    if input.chan.lower() in ignorelist or\
        input.nick.lower().replace('~','') in ignorelist or\
        input.mask.lower().replace('~','') in ignorelist:
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
        try: channel_admins = bot.channelconfig[input.chan.lower()]['channel_admins'].lower()
        except: channel_admins = " "
        if input.nick.lower() not in channel_admins and input.mask.lower() not in channel_admins:
            if args.get('adminonly', False):
                admins = bot.config.get('admins', [])
                if input.nick not in admins and input.mask not in admins:
                    input.notice("Sorry, you are not allowed to use this command.")
                    return None
    elif args.get('adminonly', False):
        admins = bot.config.get('admins', [])
        if input.nick not in admins and input.mask not in admins:
            input.notice("Sorry, you are not allowed to use this command.")
            return None


    return input
