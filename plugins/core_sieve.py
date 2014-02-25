import re
from util import hook, database, user
import os
import time
import inspect
import json

#count = 0

# db.execute("CREATE TABLE if not exists channelsettings(channel, admins, permissions, aop, bans, disabled, ignored, badwords, flood, cmdflood, trim, primary key(channel))")
# try: db.execute("select channel from channelsettings where channel=lower(?)", [chan]).fetchone()[0]
# except: db.execute("INSERT INTO channelsettings VALUES(?,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ')", [chan])
# db.commit()



cmdflood_filename = 'cmdflood'
if not os.path.exists(cmdflood_filename): open(cmdflood_filename, 'w').write(inspect.cleandoc(r'''{}'''))

flood_filename = 'flood'
if not os.path.exists(flood_filename): open(flood_filename, 'w').write(inspect.cleandoc(r'''{}'''))


@hook.sieve
def ignoresieve(bot, input, func, type, args):
    """ blocks input from ignored channels/nicks/hosts """
    # ignorelist = bot.config["plugins"]["ignore"]["ignored"]
    db = bot.get_db_connection(input.conn)
    mask = input.mask.lower()
    chan = input.chan.lower()
    ignorelist = database.get(db,'channels','ignored','chan',chan)

    # don't block input to event hooks
    if type == "event":
        return input

    if user.is_admin(mask,chan,db,bot): return input

    if ignorelist and user.format_hostmask(mask) in ignorelist: 
        print "[{}]: {} is ignored.".format(input.chan,mask)
        return None

    # if input.chan.lower() in ignorelist \
    #    or input.nick.lower().replace('~','') in ignorelist \
    #    or input.mask.lower().replace('~','').lower() in ignorelist:
    #     if input.command == "PRIVMSG" and input.lastparam[1:] == "unignore":
    #         return input
    #     else:
    #         return None
    return input


@hook.sieve
def sieve_suite(bot, input, func, kind, args):
    fn = re.match(r'^plugins.(.+).py$', func._filename)

    # ignore joins/parts/modes 
    # if "MODE" or "JOIN" or "PART" in input.command: return input
    # print fn.group(1)
    # dont process other sieves
    if fn.group(1) == 'seen' or \
       fn.group(1) == 'tell' or\
       fn.group(1) == 'ai' : return input
       # fn.group(1) == 'log': 

    # ignore any input from the bot
    if input.nick == input.conn.nick: 
        # print "Ignoring {}".format(input.conn.nick)
        return None

    # ignore bots if ignorebots = true
    if input.command == 'PRIVMSG' and input.nick.endswith('bot') and args.get('ignorebots', True): return None


    ### process global config options
    # ignore plugins disabled in the config
    if fn and fn.group(1).lower() in bot.config.get('disabled_plugins', []): return None
    # process acls
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


    # if not fn.group(1) == 'log': print fn.group(1)

    # print input.mask.lower().replace('~','')
    ### channel configs
    db = bot.get_db_connection(input.conn)
    chan = input.chan.lower()
    channeladmin = user.is_channeladmin(input.mask, input.chan, db)
    globaladmin = user.is_globaladmin(input.mask, input.chan, bot)

    if "JOIN" or "PART" in input.command: 
        database.set(db,'users','mask',input.mask.lower().replace('~',''),'nick',input.nick.lower())
    
    if args.get('channeladminonly', False): 
        if not channeladmin and not globaladmin:
            input.notice("Sorry, I cant let you do that {}.".format(input.nick))
            return None
        
    if args.get('adminonly', False):
        if not globaladmin:
            input.notice("Sorry, I cant let you do that {}.".format(input.nick))
            return None

    disabled_commands = database.get(db,'channels','disabled','chan',chan)
    if disabled_commands:
        for disabled_command in disabled_commands.split(' '):
            if fn and fn.group(1).lower().strip() == disabled_command:
                # input.notice("[{}]: {} is disabled.".format(input.chan,fn.group(1)))
                print("[{}]: {} is disabled.".format(input.chan,fn.group(1)))
                return None

            if kind == "command":
                if input.trigger == disabled_command:
                    input.notice("[{}]: {} is disabled.".format(input.chan,input.trigger))
                    return None

    #flood protection
    if not globaladmin and not channeladmin:
        if kind == "command":
            # try: cmdflood_protection = bot.channelconfig[input.chan.lower()]['cmdflood_protection']
            # except: cmdflood_protection = None
            cmdflood_protection = database.get(db,'channels','cmdflood','chan',chan)
            if cmdflood_protection:
                cmdflood_num = cmdflood_protection.split(' ')[0]
                cmdflood_duration = cmdflood_protection.split(' ')[1]
                now = time.time()
                cmdflood = json.load(open(cmdflood_filename))
                try: 
                    nick = cmdflood[input.nick]
                except: 
                    nick = []
                    cmdflood[input.nick] = nick

                cmdflood[input.nick].append(now)

                for x in cmdflood[input.nick]:
                    if now - x > int(cmdflood_duration):
                        cmdflood[input.nick].remove(x)

                json.dump(cmdflood, open(cmdflood_filename, 'w'), sort_keys=True, indent=2)
     
                if len(cmdflood[input.nick]) > (int(cmdflood_num)):
                    input.notice("Flood detected. Please wait {} seconds.".format(cmdflood_duration))
                    return None

        elif kind == "event":
            if input.command == 'PRIVMSG':
                flood_protection = database.get(db,'channels','flood','chan',chan)
                if flood_protection:
                    flood_num = (int(flood_protection.split(' ')[0]) * 1)
                    flood_duration = flood_protection.split(' ')[1]
                    now = time.time()
                    flood = json.load(open(flood_filename))
                    try: 
                        nick = flood[input.nick]
                    except: 
                        nick = []
                        flood[input.nick] = nick

                    for x in flood[input.nick]:
                        if now - x > int(flood_duration):
                            flood[input.nick].remove(x)

                    flood[input.nick].append(now)

                    # print "%s / %s" % (flood_num,len(flood[input.nick]))

                    if len(flood[input.nick]) == (int(flood_num)):
                        input.conn.send("KICK {} {} #rekt".format(input.chan, input.nick))
                        flood[input.nick] = []
                        json.dump(flood, open(flood_filename, 'w'), sort_keys=True, indent=2)
                        return None
                    else:
                        json.dump(flood, open(flood_filename, 'w'), sort_keys=True, indent=2)

    return input