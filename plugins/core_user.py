from util import hook, database, http


# Battlestations
@hook.command('bullshit', autohelp=False)
@hook.command('keyboard', autohelp=False)
@hook.command(autohelp=False)
def battlestation(inp, nick=None, db=None, notice=None):
    "battlestation <url | @ person> -- Shows a users Battlestation."
    if inp:
        if 'http' in inp:
            database.set(db, 'users', 'battlestation', inp.strip(), 'nick', nick)
            notice("Saved your battlestation.")
            return
        elif 'del' in inp:
            database.set(db, 'users', 'battlestation', '', 'nick', nick)
            notice("Deleted your battlestation.")
            return
        else:
            if '@' in inp:
                nick = inp.split('@')[1].strip()
            else:
                nick = inp.strip()

    result = database.get(db, 'users', 'battlestation', 'nick', nick)
    if result:
        return '{}: {}'.format(nick, result)
    else:
        if '@' not in inp:
            notice(battlestation.__doc__)
        return 'No battlestation saved for {}.'.format(nick)


# Desktops
@hook.command(autohelp=False)
def desktop(inp, nick=None, db=None, notice=None):
    "desktop http://url.to/desktop | @ nick -- Shows a users Desktop."
    if inp:
        if 'http' in inp:
            database.set(db, 'users', 'desktop', inp.strip(), 'nick', nick)
            notice("Saved your desktop.")
            return
        elif 'del' in inp:
            database.set(db, 'users', 'desktop', '', 'nick', nick)
            notice("Deleted your desktop.")
            return
        else:
            if '@' in inp:
                nick = inp.split('@')[1].strip()
            else:
                nick = inp.strip()

    result = database.get(db, 'users', 'desktop', 'nick', nick)
    if result:
        return '{}: {}'.format(nick, result)
    else:
        if '@' not in inp:
            notice(desktop.__doc__)
        return 'No desktop saved for {}.'.format(nick)


# Greeting
@hook.command('intro', autohelp=False)
@hook.command(autohelp=False)
def greeting(inp, nick=None, db=None, notice=None):
    "greet <message | @ person> -- Shows a users Greeting."
    if nick == 'kimi':
        return
    try:
        if not inp or '@' in inp:
            if '@' in inp:
                nick = inp.split('@')[1].strip()
            result = database.get(db, 'users', 'greeting', 'nick', nick)
            if result:
                return '{}: {}'.format(nick, result)
            else:
                if '@' not in inp:
                    notice(greeting.__doc__)
                return 'No greeting saved for {}.'.format(nick)
        elif 'del' in inp:
            database.set(db, 'users', 'greeting', '', 'nick', nick)
            notice("Deleted your greeting.")
        else:
            # TODO clean this digusting mess it does nothing
            inp = inp.strip().replace("'", "").replace("ACTION", "").replace("PRIVMSG", "").replace("PING", "").replace("NOTICE", "").replace("\x01", "")
            database.set(db, 'users', 'greeting', '{} '.format(inp.encode('utf8')), 'nick', nick)
            notice("Saved your greeting.")
        return
    except Exception:
        return "Uwaaahh~~?"


# Waifu & Husbando
@hook.command(autohelp=False)
def waifu(inp, nick=None, db=None, notice=None):
    "waifu <waifu | @ person> -- Shows a users Waifu or Husbando."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'waifu', 'nick', nick)
        if result:
            return '{}: {}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(waifu.__doc__)
            return 'No waifu saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'waifu', '', 'nick', nick)
        notice("Deleted your waifu.")
    else:
        database.set(db, 'users', 'waifu', '{} '.format(inp.strip().encode('utf8')), 'nick', nick)
        notice("Saved your waifu.")
    return


@hook.command(autohelp=False)
def husbando(inp, nick=None, db=None, notice=None):
    "husbando <husbando | @ person> -- Shows a users husbando or Husbando."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'husbando', 'nick', nick)
        if result:
            return '{}: {}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(husbando.__doc__)
            return 'No husbando saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'husbando', '', 'nick', nick)
        notice("Deleted your husbando.")
    else:
        database.set(db, 'users', 'husbando', '{} '.format(inp.strip().encode('utf8')), 'nick', nick)
        notice("Saved your husbando.")
    return


@hook.command(autohelp=False)
def imouto(inp, nick=None, db=None, notice=None):
    "imouto <imouto | @ person> -- Shows a users imouto or Husbando."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'imouto', 'nick', nick)
        if result:
            return '{}: {}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(imouto.__doc__)
            return 'No imouto saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'imouto', '', 'nick', nick)
        notice("Deleted your imouto.")
    else:
        database.set(db, 'users', 'imouto', '{} '.format(inp.strip().encode('utf8')), 'nick', nick)
        notice("Saved your imouto.")
    return


@hook.command(autohelp=False)
def daughteru(inp, nick=None, db=None, notice=None):
    "daughteru <daughteru | @ person> -- Shows a users daughteru."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'daughteru', 'nick', nick)
        if result:
            return '{}: {}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(imouto.__doc__)
            return 'No daughteru saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'daughteru', '', 'nick', nick)
        notice("Deleted your daughteru.")
    else:
        database.set(db, 'users', 'daughteru', '{} '.format(inp.strip().encode('utf8')), 'nick', nick)
        notice("Saved your daughteru.")
    return


@hook.command(autohelp=False)
def mom(inp, nick=None, db=None, notice=None):
    "mom <mom | @ person> -- Shows a users mom."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'mom', 'nick', nick)
        if result:
            return '{}: {}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(mom.__doc__)
            return 'No mom saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'mom', '', 'nick', nick)
        notice("Deleted your mom.")
    else:
        database.set(db, 'users', 'mom', '{} '.format(inp.strip().encode('utf8')), 'nick', nick)
        notice("Saved your mom.")
    return


@hook.command(autohelp=False)
def dad(inp, nick=None, db=None, notice=None):
    "dad <dad | @ person> -- Shows a users dad."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'dad', 'nick', nick)
        if result:
            return '{}: {}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(dad.__doc__)
            return 'No dad saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'dad', '', 'nick', nick)
        notice("Deleted your dad.")
    else:
        database.set(db, 'users', 'dad', '{} '.format(inp.strip().encode('utf8')), 'nick', nick)
        notice("Saved your dad.")
    return


# Desktops
@hook.command(autohelp=False)
def birthday(inp, nick=None, db=None, notice=None):
    "birthday <01/01/2001> | <@ person> -- Shows a users Birthday."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'birthday', 'nick', nick)
        if result:
            return '{}: {}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(birthday.__doc__)
            return 'No birthday saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'birthday', '', 'nick', nick)
        notice("Deleted your birthday.")
    else:
        database.set(db, 'users', 'birthday', '{} '.format(inp.strip()), 'nick', nick)
        notice("Saved your birthday.")
    return


@hook.command(autohelp=False)
def horoscope(inp, db=None, notice=None, nick=None):
    """horoscope <sign> [save] -- Get your horoscope."""
    save = False
    database.init(db)

    if '@' in inp:
        nick = inp.split('@')[1].strip()
        sign = database.get(db, 'users', 'horoscope', 'nick', nick)
        if not sign:
            return "No horoscope sign stored for {}.".format(nick)
    else:
        sign = database.get(db, 'users', 'horoscope', 'nick', nick)
        if not inp:
            if not sign:
                notice(horoscope.__doc__)
                return
        else:
            if not sign:
                save = True
            if " save" in inp:
                save = True
            sign = inp.split()[0]

    url = "https://my.horoscope.com/astrology/free-daily-horoscope-{}.html".format(sign)
    try:
        result = http.get_soup(url)
        container = result.find('div', attrs={'class': 'main-horoscope'})
        if not container:
            return 'Could not parse the horoscope for {}.'.format(sign)

        paragraph = container.find('p')

        if paragraph:
            return nick + ': ' + paragraph.text
        else:
            return 'Could not read the horoscope for {}.'.format(sign)

    except Exception:
        raise
        return "Could not get the horoscope for {}.".format(sign)

    if sign and save:
        database.set(db, 'users', 'horoscope', sign, 'nick', nick)

    return u"\x02{}\x02 {}".format(title, horoscopetxt)


@hook.command(autohelp=False)
def homescreen(inp, nick=None, db=None, notice=None):
    "homescreen <url | @ person> -- Shows a users homescreen."
    if "http" in inp:
        database.set(db, 'users', 'homescreen', inp.strip(), 'nick', nick)
        notice("Saved your homescreen.")
        return
    elif 'del' in inp:
        database.set(db, 'users', 'homescreen', '', 'nick', nick)
        notice("Deleted your homescreen.")
        return
    elif not inp:
        homescreen = database.get(db, 'users', 'homescreen', 'nick', nick)
    else:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        else:
            nick = inp.strip()

    homescreen = database.get(db, 'users', 'homescreen', 'nick', nick)
    if homescreen:
        return '{}: {}'.format(nick, homescreen)
    else:
        # notice(homescreen.__doc__)
        return 'No homescreen saved for {}.'.format(nick)


@hook.command(autohelp=False)
def snapchat(inp, nick=None, db=None, notice=None):
    "snapchat <snapchatname | @ person> -- Shows a users snapchat name."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'snapchat', 'nick', nick)
        if result:
            return '{}: {}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(snapchat.__doc__)
            return 'No snapchat saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'snapchat', '', 'nick', nick)
        notice("Deleted your snapchat.")
    else:
        database.set(db, 'users', 'snapchat', '{} '.format(inp.strip().encode('utf8')), 'nick', nick)
        notice("Saved your snapchat.")
    return


@hook.command('soc', autohelp=False)
@hook.command(autohelp=False)
def socialmedia(inp, nick=None, db=None, notice=None):
    "socialmedia <socialmedianames | @ person> -- Shows a users social medias names."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'socialmedias', 'nick', nick)
        if result:
            return '{}: {}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(snapchat.__doc__)
            return 'No social medias saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'socialmedias', '', 'nick', nick)
        notice("Deleted your social medias.")
    else:
        database.set(db, 'users', 'socialmedias', '{} '.format(inp.strip().encode('utf8')), 'nick', nick)
        notice("Saved your social medias.")
    return


@hook.command(autohelp=False)
def myanime(inp, nick=None, db=None, notice=None):
    "myanime <mal name | @ person> -- Shows a users myanimelist profile."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'mal', 'nick', nick)
        if result:
            return '{}: http://myanimelist.net/animelist/{}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(myanime.__doc__)
            return 'No mal saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'mal', '', 'nick', nick)
        notice("Deleted your mal.")
    else:
        database.set(db, 'users', 'mal', '{} '.format(inp.strip().encode('utf8')), 'nick', nick)
        notice("Saved your mal.")
    return


@hook.command(autohelp=False)
def mymanga(inp, nick=None, db=None, notice=None):
    "mymanga <mal name | @ person> -- Shows a users myanimelist profile."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'mal', 'nick', nick)
        if result:
            return '{}: http://myanimelist.net/mangalist/{}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(mymanga.__doc__)
            return 'No mal saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'mal', '', 'nick', nick)
        notice("Deleted your mal.")
    else:
        database.set(db, 'users', 'mal', '{} '.format(inp.strip().encode('utf8')), 'nick', nick)
        notice("Saved your mal.")
    return


@hook.command(autohelp=False)
def selfie(inp, nick=None, db=None, notice=None):
    "selfie <url | @ person> -- Shows a users selfie."
    if inp:
        if 'http' in inp:
            database.set(db, 'users', 'selfie', inp.strip(), 'nick', nick)
            notice("Saved your selfie.")
            return
        elif 'del' in inp:
            database.set(db, 'users', 'selfie', '', 'nick', nick)
            notice("Deleted your selfie.")
            return
        else:
            if '@' in inp:
                nick = inp.split('@')[1].strip()
            else:
                nick = inp.strip()

    result = database.get(db, 'users', 'selfie', 'nick', nick)
    if result:
        return '{}: {}'.format(nick, result)
    else:
        if '@' not in inp:
            notice(selfie.__doc__)
        return 'No selfie saved for {}.'.format(nick)


@hook.command(autohelp=False)
def fit(inp, nick=None, db=None, notice=None):
    "fit <url | @ person> -- Shows a users outfit."
    if inp:
        if "http" in inp:
            database.set(db, 'users', 'fit', inp.strip(), 'nick', nick)
            notice("Saved your fit.")
            return
        elif 'del' in inp:
            database.set(db, 'users', 'fit', '', 'nick', nick)
            notice("Deleted your fit.")
            return
        else:
            if '@' in inp:
                nick = inp.split('@')[1].strip()
            else:
                nick = inp.strip()

    result = database.get(db, 'users', 'fit', 'nick', nick)
    if result:
        return '{}: {}'.format(nick, result)
    else:
        if '@' not in inp:
            notice(fit.__doc__)
        return 'No fit saved for {}.'.format(nick)


@hook.command('hw', autohelp=False)
@hook.command(autohelp=False)
def handwriting(inp, nick=None, db=None, notice=None):
    "handwriting <url | @ person> -- Shows a users handwriting."
    if inp:
        if 'http' in inp:
            database.set(db, 'users', 'handwriting', inp.strip(), 'nick', nick)
            notice("Saved your handwriting.")
            return
        elif 'del' in inp:
            database.set(db, 'users', 'handwriting', '', 'nick', nick)
            notice("Deleted your handwriting.")
            return
        else:
            if '@' in inp:
                nick = inp.split('@')[1].strip()
            else:
                nick = inp.strip()

    result = database.get(db, 'users', 'handwriting', 'nick', nick)
    if result:
        return '{}: {}'.format(nick, result)
    else:
        if '@' not in inp:
            notice(fit.__doc__)
        return 'No handwriting saved for {}.'.format(nick)


@hook.command(autohelp=False)
def steam(inp, nick=None, db=None, notice=None):
    "steam <steam | @ person> -- Shows a users steam information."

    if not inp or '@' in inp:
        if '@' in inp:
            nick = inp.split('@')[1].strip()
        result = database.get(db, 'users', 'steam', 'nick', nick)
        if result:
            return '{}: {}'.format(nick, result)
        else:
            if '@' not in inp:
                notice(steam.__doc__)
            return 'No steam information saved for {}.'.format(nick)
    elif 'del' in inp:
        database.set(db, 'users', 'steam', '', 'nick', nick)
        notice("Deleted your steam information.")
    else:
        database.set(db, 'users', 'steam', '{} '.format(inp.strip().encode('utf8')), 'nick', nick)
        notice("Saved your steam information.")
    return
