from util import hook, user, database
import time

db_ready = False

def db_init(db):
    global db_ready
    db.execute("CREATE TABLE if not exists votes(chan, action, target, voters, time, primary key(chan, action, target));")
    db.commit()
    db_ready = True

def process_vote(target,action,chan,mask,db,notice,conn):
    if ' ' in target: 
        notice('Invalid nick')
        return

    try: votes2kick = database.get(db,'channels','votekick','chan',chan)
    except: votes2kick = 10
    try: votes2ban = database.get(db,'channels','voteban','chan',chan)
    except: votes2ban = 10

    if len(target) is 0:
        if action is 'kick': notice('Votes required to kick: {}'.format(votes2kick))
        elif action is 'ban': notice('Votes required to ban: {}'.format(votes2ban))
        return

    votefinished = False
    global db_ready
    if not db_ready: db_init(db)
    chan = chan.lower()
    target = target.lower()
    voter = user.format_hostmask(mask)
    oters = db.execute("SELECT voters FROM votes where chan='{}' and action='{}' and target like '{}'".format(chan,action,target)).fetchone()

    if conn.nick.lower() in target: return "I dont think so Tim."

    if voters: 
        voters = voters[0]
        if voter in voters: 
            notice("You have already voted.")
            return
        else:
            voters = '{} {}'.format(voters,voter).strip()
            notice("Thank you for your vote!")
    else: 
        voters = voter

    votecount = len(voters.split(' '))

    if 'kick' in action: 
        votemax = int(votes2kick)
        if votecount >= votemax:
            votefinished = True
            conn.send("KICK {} {} :{}".format(chan, target, "You have been voted off the island."))
    if 'ban' in action:
        votemax = int(votes2ban)
        if votecount >= votemax:
            votefinished = True
            conn.send("MODE {} +b {}".format(chan, user.get_hostmask(target,db)))
            conn.send("KICK {} {} :".format(chan, target, "You have been voted off the island."))
    
    if votefinished: db.execute("DELETE FROM votes where chan='{}' and action='{}' and target like '{}'".format(chan,action,target))
    else: db.execute("insert or replace into votes(chan, action, target, voters, time) values(?,?,?,?,?)", (chan, action, target, voters, time.time()))
        
    db.commit()
    return ("Votes to {} {}: {}/{}".format(action, target, votecount,votemax))



@hook.command(autohelp=False)
def votekick(inp, nick=None, mask=None, conn=None, chan=None, db=None, notice=None):
    return process_vote(inp,'kick',chan,mask,db,notice,conn)


@hook.command(autohelp=False)
def voteban(inp, nick=None, mask=None, conn=None, chan=None, db=None, notice=None):
    return process_vote(inp,'ban',chan,mask,db,notice,conn)


# UPVOTE
 

 # @hook.command(autohelp=False)
# def vote(inp, nick=None, mask=None,conn=None, chan=None, db=None, notice=None):
#     global db_ready
#     if not db_ready: db_init(db)
#     chan = chan.lower()
#     action = inp.split(" ")[0].lower()
#     target = inp.split(" ")[1].lower()
#     voter = user.format_hostmask(mask)
#     voters = db.execute("SELECT voters FROM votes where chan='{}' and action='{}' and target like '{}'".format(chan,action,target)).fetchone()

#     if voters: 
#         voters = voters[0]
#         if voter in voters: 
#             notice("You have already voted.")
#             return
#         else:
#             voters = '{} {}'.format(voters,voter).strip()
#             notice("Thank you for your vote!")
#     else: 
#         voters = voter

#     votecount = len(voters.split(' '))

#     if votecount >= 4: 
#         if 'kick' in action: 
#             conn.send("KICK {} {} :{}".format(chan, target, "You have been voted off the island."))
#         if 'ban' in action:
#             conn.send("MODE {} +b {}".format(chan, target))
#             conn.send("KICK {} {} :".format(chan, target, "You have been voted off the island."))
#         db.execute("DELETE FROM votes where chan='{}' and action='{}' and target like '{}'".format(chan,action,target))
#         db.commit()
#         return
#     else:
#         db.execute("insert or replace into votes(chan, action, target, voters, time) values(?,?,?,?,?)", (chan, action, target, voters, time.time()))
#         db.commit()
#         notice("Vote count to {} {}: {} / 4".format(action, target, votecount))
#         return
