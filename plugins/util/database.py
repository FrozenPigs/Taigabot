from util import hook
import log

db_ready = False

def init(db):
    global db_ready
    if not db_ready: 
        # db.execute("CREATE TABLE if not exists seen(name, time, quote, chan, host, primary key(name, chan))")
        db.execute("CREATE TABLE if not exists channels(chan NOT NULL, admins, permissions, ops, bans, disabled, ignored, badwords, flood, cmdflood, trimlength, autoop, votekick, voteban, primary key(chan));")
        db.execute("CREATE TABLE if not exists users(nick NOT NULL, mask, version, location, lastfm, fines, battlestation, desktop, horoscope, greeting, waifu, husbando, birthday, homescreen, primary key(nick));")
        db.commit()
        db_ready = True

def init_tables(db, table):
    if "channels" in table: db.execute("INSERT INTO channels VALUES(?,'','','','','','','','','','')", [chan])
    # if "channels" in table: db.execute("INSERT INTO channels VALUES(?,'','','','','','','','','','')", [chan])
    # nick, mask, version, location, lastfm, fines, battlestation, desktop, horoscope, primary key(nick)
    db.commit()

# def table_exists(db,table):
#     init(db)
#     exists = db.execute("SELECT EXISTS (SELECT 1 FROM {} WHERE type = 'table' and name = '{}'").format(db,table).fetchone()[0] == 1
#     if not exists: create_table(db,table)

def field_exists(db,table,matchfield,matchvalue):
    # if table_exists(db,table):
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
        #if result: print "Get: {}='{}'".format(field,result[0].strip())
        # if result is '' or result is ' ' or result is None or result is False or result is 'NULL': return False
        # elif result is int and len(str(result)) == 1: return False
        if result: return result[0]
        else: return False
    except:
        log.log("***ERROR: SELECT {} FROM {} WHERE {}='{}';".format(field,table,matchfield,matchvalue))


def set(db, table, field, value, matchfield, matchvalue):
    init(db)
    if value is None: value = ''
    # .replace('`','').disabled
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




# 11:56:43 #degeneracy <infinity> .set desktop wat531[Luna] http://i.imgur.com/bPoI3OA.png
# [u'http://i.imgur.com/bPoI3OA.png']
# Exists: '0'
# INSERT INTO users (location,nick) VALUES ('[u'http://i.imgur.com/bPoI3OA.png']','wat531[luna]');
# >>> u"NOTICE infinity :PRIVMSG #degeneracy :Set desktop for wat531[Luna] to [u'http://i.imgur.com/bPoI3OA.png']."




#INSERT OR IGNORE INTO users (nick, battlestation, desktop) SELECT nick, battlestation, desktop FROM usersettings;
# UPDATE users SET desktop = ( SELECT desktop FROM usersettings WHERE users.nick = usersettings.nick );




# INSERT OR IGNORE INTO users (nick, fines) SELECT nick, totalfines FROM fines;
# UPDATE users SET fines = ( SELECT totalfines FROM fines WHERE users.nick = fines.nick );
# DROP TABLE IF EXISTS fines;

# INSERT OR IGNORE INTO users (nick, location) SELECT ircname, location FROM locations;
# UPDATE users SET location = ( SELECT location FROM locations WHERE users.nick = locations.ircname );
# DROP TABLE IF EXISTS locations;

# INSERT OR IGNORE INTO users (nick, lastfm) SELECT ircname, lastfmname FROM usernames;
# UPDATE users SET lastfm = ( SELECT lastfmname FROM usernames WHERE users.nick = usernames.ircname );
# DROP TABLE IF EXISTS usernames;



# UPDATE closure SET checked = 0 
# WHERE item_id IN (SELECT id FROM item WHERE ancestor_id = 1);