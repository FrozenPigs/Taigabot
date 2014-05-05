from util import database
import re
from fnmatch import fnmatch

#@hook.command(autohelp=False)
def get_hostmask(inp,db):
    "userhost -- Returns a nicks userhost"
    #db.execute("create table if not exists seen(name, time, quote, chan, host, primary key(name, chan))")
    #db.commit()
    nick = inp.strip().replace('~','').lower()
    db_host = database.get(db,'users','mask','nick',nick)
    if nick is db_host: db_host = database.get(db,'seen','host','name',nick)
    try:
        if db_host.count('.') == 1:
            hostmatch = re.search(r"^(.+@)(.+\.)(\w+)$", db_host, re.I)
            userhost = '{}{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3))
        elif db_host.count('.') == 2:
            hostmatch = re.search(r"^(.+@).+\.(.+\.)(.+)$", db_host, re.I)
            userhost = '{}*{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3))
        else:    
            # ^(.+@).*\b(\w+\.)(\w+\.)(\w+)$
            hostmatch = re.search(r"^(.+@).+\.(.+\.)(.+\.)(.+)$", db_host, re.I)
            userhost = '{}*{}{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3),hostmatch.group(4))
        return userhost.lower()
    except:
        return nick.lower()


def format_hostmask(inp):
    "format_hostmask -- Returns a nicks userhost"
    db_host = inp.strip().replace('~','').lower()
    try:
        if db_host.count('.') == 1:
            hostmatch = re.search(r"^(.+@)(.+\.)(\w+)$", db_host, re.I)
            userhost = '{}{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3))
        elif db_host.count('.') == 2:
            hostmatch = re.search(r"^(.+@).+\.(.+\.)(.+)$", db_host, re.I)
            userhost = '{}*{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3))
        else:    
            # ^(.+@).*\b(\w+\.)(\w+\.)(\w+)$
            hostmatch = re.search(r"^(.+@).+\.(.+\.)(.+\.)(.+)$", db_host, re.I)
            userhost = '{}*{}{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3),hostmatch.group(4))
        return userhost.lower()
    except:
        return db_host.lower()

# def compare_masks(mask,matchlist):
#     for pattern in channeladmins.split(' '):
#         if bool(fnmatch(mask, pattern)): return True
#     return False


#@hook.command(autohelp=False)
def compare_hostmasks(hostmask,matchmask):
    hostmask = hostmask.lower().replace('~','').replace('*','\S+')
    matchmask = ' '.join(matchmask).lower().replace('*','.+')
    if bool(re.search(hostmask,matchmask)): return True
    else: return False


def is_globaladmin(inp,chan,bot):
    hostmask = format_hostmask(inp)
    globaladmins = bot.config.get('admins', [])
    # if globaladmins and compare_hostmasks(hostmask,globaladmins): return True
    # else: return False
    # print "{} - {}".format(globaladmins,hostmask)
    if globaladmins and hostmask in globaladmins: return True
    else: return False


def is_channeladmin(inp,chan,db):
    hostmask = format_hostmask(inp)
    channeladmins = database.get(db,'channels','admins','chan',chan)
    # if channeladmins and compare_hostmasks(hostmask,channeladmins): return True
    # else: return False
    # print "{} - {}".format(channeladmins,hostmask)
    if channeladmins and hostmask in channeladmins: return True
    else: return False


def is_admin(inp,chan,db,bot):
    if is_globaladmin(inp,chan,bot): return True  
    if is_channeladmin(inp,chan,db): return True
    return False




# def format_hostmask(inp):
#     "userhost -- Returns a nicks userhost"
#     inp_mask = inp.lower().strip()
#     try: 
#         if db_host.count('.') <= 2:
#             hostmatch = re.search(r"^.*\b(\w+@)(.+\.)(\w+)$", db_host, re.I)
#             userhost = '{}{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3))
#         elif db_host.count('.') == 3: 
#             hostmatch = re.search(r"^.*\b(\w+@).*\b(\w+\.)(\w+)$", db_host, re.I)
#             userhost = '{}*{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3))
#         else:    
#             hostmatch = re.search(r"^.*\b(\w+@).*\b(\w+\.)(\w+\.)(\w+)$", db_host, re.I)
#             userhost = '{}*{}{}{}'.format(hostmatch.group(1),hostmatch.group(2),hostmatch.group(3),hostmatch.group(4)).host
#         return userhost.lower()
#     except:
#         return inp_mask.lower()





# def is_channeladmin(inp,chan,db):
#     admin = False
#     channeladmins = database.get(db,'channels','admins','chan',chan)
#     userhost = parse_hostmask(inp)

#     if bool(re.search(channeladmins,userhost)): 
#         return True
#     else:
#         return False

    # if channeladmins:
    #     if target in channeladmins: admin = True  
    # return admin

# def is_globaladmin(target,chan,bot):
#     globaladmin = False
#     try: globaladmins = bot.config.get('admins', [])
#     except: globaladmins = ''

#     admins = database.get(db,'channels','admins','chan',chan)

#     if admins:
#         if target in admins: admin = True
#     if channeladmins:
#         if target in channeladmins: admin = True  
#     return admin







# def check_hostmask(inp):
#     inp = inp.split(' ')
#     user_mask = inp[0].replace('~','').lower()
#     match_mask = inp[1].replace('*','.+').lower()
#     if bool(re.search(match_mask,user_mask)): 
#         return True
#     else:
#         return False


# def is_channeladmin(inp,chan,db):
#     channeladmins = database.get(db,'channels','admins','chan',chan)
#     userhost = parse_hostmask(inp)
#     print "{} - {}".format(channeladmins,userhost)
#     if channeladmins and userhost in channeladmins: 
#         return True
#     else:
#         return False


# def is_globaladmin(inp,chan,bot):
#     globaladmins = bot.config.get('admins', [])
#     userhost = parse_hostmask(inp)
#     # print "{} - {}".format(globaladmins,userhost)
#     if globaladmins and userhost in globaladmins: 
#         return True
#     else:
#         return False