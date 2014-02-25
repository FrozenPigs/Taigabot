# Plugin by Infinity - <https://github.com/infinitylabs/UguuBot>

from util import hook, http, text, database

@hook.command(autohelp=False)
def horoscope(inp, db=None, notice=None, nick=None):
    """horoscope <sign> -- Get your horoscope."""
    save = False
    database.init(db)
    
    if '@' in inp:
        nick = inp.split('@')[1].strip()
        sign = database.get(db,'users','horoscope','nick',nick)
        if not sign: return "No horoscope sign stored for {}.".format(nick)
    else:
        sign = database.get(db,'users','horoscope','nick',nick)
        if not inp: 
            if not sign:
                notice(horoscope.__doc__)
                return
        else:
            if not sign: save = True
            if " save" in inp: save = True
            sign = inp.split()[0]

    url = "http://my.horoscope.com/astrology/free-daily-horoscope-%s.html" % sign
    try:
        result = http.get_soup(url)
        title = result.find_all('h1', {'class': 'h1b'})[1].text
        horoscopetxt = result.find('div', {'id': 'textline'}).text
    except: return "Could not get the horoscope for {}.".format(sign)

    if sign and save: database.set(db,'users','horoscope',sign,'nick',nick)
    
    return u"\x02{}\x02 {}".format(title, horoscopetxt)

    ###Old
    #result = unicode(result, "utf8").replace('flight ','')

    # try: sign = db.execute("select horoscope from users where nick=lower(?)", (nick,)).fetchone()[0]
    # except: save = True

    #db.execute("UPSERT INTO users(nick, horoscope) VALUES (?,?)",(nick.lower(), sign,))
    #db.commit()