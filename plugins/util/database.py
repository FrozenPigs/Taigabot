from util import hook
import log

db_ready = False

def init(db):
    global db_ready
    if not db_ready: 
        # db.execute("CREATE TABLE if not exists seen(name, time, quote, chan, host, primary key(name, chan))")
        db.execute("CREATE TABLE if not exists channels(chan NOT NULL, admins, permissions, ops, bans, disabled, ignored, badwords, flood, cmdflood, trimlength, autoop, votekick, voteban, primary key(chan));")
        db.execute("CREATE TABLE if not exists users(nick NOT NULL, mask, version, location, lastfm, fines, battlestation, desktop, horoscope, greeting, waifu, husbando, birthday, homescreen, snapchat, mal, selfie, primary key(nick));")
        db.commit()
        db_ready = True

def init_tables(db, table):
    if "channels" in table: db.execute("INSERT INTO channels VALUES(?,'','','','','','','','','','')", [chan])
    # nick, mask, version, location, lastfm, fines, battlestation, desktop, horoscope, primary key(nick)
    db.commit()

def field_exists(db,table,matchfield,matchvalue):
    init(db)
    exists = db.execute("SELECT EXISTS(SELECT 1 FROM {} WHERE {}='{}' LIMIT 1);".format(table,matchfield,matchvalue.encode('utf8'))).fetchone()[0]
    # print "Exists: '{}'".format(exists)
    if exists: return True
    else: return False

def get(db,table,field,matchfield,matchvalue):
    init(db)
    matchvalue = matchvalue.encode('utf-8').lower()
    try:
        #print "SELECT {} FROM {} WHERE {}='{}';".format(field,table,matchfield,matchvalue.lower())
        result = db.execute("SELECT {} FROM {} WHERE {}='{}';".format(field,table,matchfield,matchvalue)).fetchone()
        if result: return result[0]
        else: return False
    except:
        log.log("***ERROR: SELECT {} FROM {} WHERE {}='{}';".format(field,table,matchfield,matchvalue))


def set(db, table, field, value, matchfield, matchvalue):
    init(db)
    if value is None: value = ''
    matchvalue = matchvalue.encode('utf-8').lower()
    if type(value) is str: value = value.replace("'","").replace('\"', "").encode('utf-8')
    try:
        if field_exists(db,table,matchfield,matchvalue):
            # print "UPDATE {} SET {} = '{}' WHERE {} = '{}';".format(table,field,value,matchfield,matchvalue.encode('utf8').lower())
            db.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}';".format(table,field,value,matchfield,matchvalue))
        else: 
            # print "INSERT INTO {} ({},{}) VALUES ('{}','{}');".format(table,field,matchfield,value,matchvalue.encode('utf8').lower())
            db.execute("INSERT INTO {} ({},{}) VALUES ('{}','{}');".format(table,field,matchfield,value,matchvalue))
    except:
        #print "DB"
        # print "UPDATE {} SET {} = '{}' WHERE {} = '{}';".format(table,field,value,matchfield,matchvalue.encode('utf8').lower())
        db.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}';".format(table,field,value,matchfield,matchvalue))
        
    db.commit()
    return
