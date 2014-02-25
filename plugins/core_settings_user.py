from util import hook, database
import random

### Battlestations
@hook.command(autohelp=False)
def battlestation(inp, nick=None, conn=None, chan=None,db=None, notice=None):
    "battlestation <url | @ person> -- Shows a users Battlestation."

    if  "http" in inp:
        database.set(db,'users','battlestation',inp.strip(),'nick',nick)
        notice("Saved your battlestation.")
        return
    elif 'del' in inp:
        database.set(db,'users','battlestation','','nick',nick)
        notice("Deleted your battlestation.")
        return
    elif not inp: 
        battlestation = database.get(db,'users','battlestation','nick',nick)
    else:
        if '@' in inp: nick = inp.split('@')[1].strip()
        else: nick = inp.strip()

    battlestation = database.get(db,'users','battlestation','nick',nick)
    if desktop: return '{}: {}'.format(nick,battlestation)
    else: return 'No battlestation saved for {}.'.format(nick)

### Desktops
@hook.command(autohelp=False)
def desktop(inp, nick=None, conn=None, chan=None,db=None, notice=None):
    "desktop <url | @ person> -- Shows a users Desktop."
    if  "http" in inp:
        database.set(db,'users','desktop',inp.strip(),'nick',nick)
        notice("Saved your desktop.")
        return
    elif 'del' in inp:
        database.set(db,'users','desktop','','nick',nick)
        notice("Deleted your desktop.")
        return
    elif not inp: 
        desktop = database.get(db,'users','desktop','nick',nick)
    else:
        if '@' in inp: nick = inp.split('@')[1].strip()
        else: nick = inp.strip()

    desktop = database.get(db,'users','desktop','nick',nick)
    if desktop: 
        return '{}: {}'.format(nick,desktop)
    else: 
        # notice(desktop.__doc__)
        return 'No desktop saved for {}.'.format(nick)
        

### Desktops
@hook.command('intro', autohelp=False)
@hook.command(autohelp=False)
def greeting(inp, nick=None, conn=None, chan=None,db=None, notice=None):
    "greet <message | @ person> -- Shows a users Greeting."

    if not inp or '@' in inp:
        if '@' in inp: nick = inp.split('@')[1].strip()
        greeting = database.get(db,'users','greeting','nick',nick)
        if greeting: return '{}: {}'.format(nick,greeting)
        else: return 'No greeting saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db,'users','greeting','','nick',nick)
        notice("Deleted your desktop.")
    else:
        database.set(db,'users','greeting',inp.strip(),'nick',nick)
        notice("Saved your greeting.")
    return


### Waifu & Husbando
@hook.command(autohelp=False)
def waifu(inp, nick=None, conn=None, chan=None,db=None, notice=None):
    "waifu <waifu | @ person> -- Shows a users Waifu or Husbando."

    if not inp or '@' in inp:
        if '@' in inp: nick = inp.split('@')[1].strip()
        waifu = database.get(db,'users','waifu','nick',nick)
        if waifu: return '{}: {}'.format(nick,waifu)
        else: return 'No waifu saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db,'users','waifu','','nick',nick)
        notice("Deleted your waifu.")
    else:
        database.set(db,'users','waifu',inp.strip(),'nick',nick)
        notice("Saved your waifu.")
    return


@hook.command(autohelp=False)
def husbando(inp, nick=None, conn=None, chan=None,db=None, notice=None):
    "husbando <husbando | @ person> -- Shows a users husbando or Husbando."

    if not inp or '@' in inp:
        if '@' in inp: nick = inp.split('@')[1].strip()
        husbando = database.get(db,'users','husbando','nick',nick)
        if husbando: return '{}: {}'.format(nick,husbando)
        else: return 'No husbando saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db,'users','husbando','','nick',nick)
        notice("Deleted your husbando.")
    else:
        database.set(db,'users','husbando',inp.strip(),'nick',nick)
        notice("Saved your husbando.")
    return


### Desktops
@hook.command(autohelp=False)
def birthday(inp, nick=None, conn=None, chan=None,db=None, notice=None):
    "birthday <date | @ person> -- Shows a users Birthday."
    return
    if not inp or '@' in inp:
        if '@' in inp: nick = inp.split('@')[1].strip()
        birthday = database.get(db,'users','birthday','nick',nick)
        if birthday: return '{}: {}'.format(nick,birthday)
        else: return 'No birthday saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db,'users','birthday','','nick',nick)
        notice("Deleted your desktop.")
    else:
        database.set(db,'users','birthday',inp.strip(),'nick',nick)
        notice("Saved your birthday.")
    return