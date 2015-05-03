from util import hook
import log

channel_columns = ['chan NOT NULL',
		   'admins', 'permissions', 'ops', 'bans', 'disabled', 'ignored', 'badwords', 'flood', 'cmdflood', 'trimlength', 'autoop', 'votekick', 'voteban',
		   'primary key(chan)']
user_columns	= ['nick NOT NULL', 
		   'mask', 'version', 'location', 'lastfm', 'fines', 'battlestation', 'desktop', 'horoscope', 'greeting', 'waifu', 'husbando', 'birthday', 'homescreen', 'snapchat', 'mal', 'selfie', 'steam',
		   'primary key(nick)']

db_ready = False

def init(db):
    global db_ready
    if not db_ready: 
        # db.execute("CREATE TABLE if not exists seen(name, time, quote, chan, host, primary key(name, chan))")
        db.execute("CREATE TABLE if not exists channels({});".format(", ".join(channel_columns)))
        db.execute("CREATE TABLE if not exists users({});".format(", ".join(user_columns)))
        db.commit()
        db_ready = True

def field_exists(db,table,matchfield,matchvalue):
    init(db)
    exists = db.execute("SELECT EXISTS(SELECT 1 FROM {} WHERE {}='{}' LIMIT 1);".format(table,matchfield,matchvalue.encode('utf8'))).fetchone()[0]
    if exists: return True
    else: return False

def get(db,table,field,matchfield,matchvalue):
    init(db)
    matchvalue = matchvalue.encode('utf-8').lower()
    try:
        result = db.execute("SELECT {} FROM {} WHERE {}='{}';".format(field,table,matchfield,matchvalue)).fetchone()
        if result: return result[0].encode('utf-8')
        else: return False
    except:
        log.log("***ERROR: SELECT {} FROM {} WHERE {}='{}';".format(field,table,matchfield,matchvalue))


def set(db, table, field, value, matchfield, matchvalue):
    init(db)
    if value is None: value = ''
    matchvalue = matchvalue.decode('utf-8').lower()
    if type(value) is str: value = value.replace("'","").replace('\"', "")

    try:
	db.execute("ALTER TABLE {} ADD COLUMN {};".format(table, field))
    except:
        pass

    try:
        if field_exists(db,table,matchfield,matchvalue):
            db.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}';".format(table,field,value,matchfield,matchvalue))
        else: 
            db.execute("INSERT INTO {} ({},{}) VALUES ('{}','{}');".format(table,field,matchfield,value,matchvalue))
    except:
        db.execute("UPDATE {} SET {} = '{}' WHERE {} = '{}';".format(table,field,value,matchfield,matchvalue))
        
    db.commit()
    return
