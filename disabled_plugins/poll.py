from util import hook, http
import time

# TODO: poll timer support

db_ready = False

def db_init(db):
    "check to see that our db has the the seen table and return a connection."
    """Implements a poll system."""
    db.execute('''create table if not exists polls (
              pollID int auto_increment primary key,
              question text,
              active bool )''')
    db.execute('''create table if not exists answers (
              answerID int auto_increment primary key,
              pollID int,
              'index' int,
              answer text,
              unique(pollID, 'index') )''')
    db.execute('''create table if not exists votes (
              voteID int auto_increment primary key,
              answerID int,
              nick varchar(255) )''')
    db.commit()
    print "Created Database"
    db_ready = True

# def load():
    
    # registerFunction("open poll %S", openPoll, "open poll <question>", restricted = True)
    # registerFunction("close poll", closePoll, restricted = True)
    # registerFunction("show poll %!i", showPoll, "show poll [poll ID]")
    # registerFunction("vote for %i", voteFor, "vote for <answer ID>")
    # registerFunction("vote new %S", voteNew, "vote new <answer>")
    # registerFunction("search poll %S", searchPoll, "search poll <search term>")
    # registerFunction("delete poll %i", deletePoll, "delete poll <poll ID>", restricted = True)
    # registerModule("Poll", load)


@hook.command(adminonly=True)
def openPoll(question, reply=None, db=None):
    """Creates a new poll."""
    if not db_ready: db_init(db)
    try:
        active = db.execute("SELECT pollID FROM polls WHERE active = 1").fetchone()[0]
        if active: 
            reply("There already is an open poll.")
            return
    except:
        db.execute("INSERT INTO polls (question, active) VALUES ('{}', 1)".format(question))
        reply("Opened new poll: {}".format(question))
        #reply("Poll opened!")
    return


@hook.command(adminonly=True, autohelp=False)
def closePoll(inp, reply=None, db=None):
    """Closes the current poll."""
    if not db_ready: db_init(db)
    active = db.execute("SELECT pollID FROM polls WHERE active = 1")
    if not active[0]:
        reply("No poll is open at the moment.")
        return
    reply("Pool's closed.")
    for (answer, votes) in db.execute("SELECT answer, count(voteID) FROM polls INNER JOIN answers ON answers.pollID = polls.pollID LEFT JOIN votes ON votes.answerID = answers.answerID WHERE active = 1 GROUP BY answers.answerID, answer ORDER BY count(voteID) DESC LIMIT 1"):
        reply("Winning entry: '%s' with %s votes" % (answer, votes))
    db.execute("UPDATE polls SET active = 0")


@hook.command(autohelp=False)
def showPoll(pollID, db=None):
    """Shows the answers for a given poll."""
    if not db_ready: db_init(db)
    if pollID == None:
        poll = db.execute("SELECT pollID, question FROM polls WHERE active = 1")
        if len(poll) == 0:
            reply("There's no poll open.")
            return
    else:
        poll = db.execute("SELECT pollID, question FROM polls WHERE pollID = '{}'".format(pollID))
        if len(poll) == 0:
            reply("No such poll found.")
            return
    pollID = poll[0][0]
    question = poll[0][1]
    reply(question)
    for (index, answer, votes) in db.execute("SELECT 'index', answer, count(voteID) FROM answers LEFT JOIN votes ON votes.answerID = answers.answerID WHERE pollID = {} GROUP BY answers.answerID, 'index', answer ORDER BY 'index' ASC".format(pollID, )):
        reply("%s. %s (%s)" % (index, answer, votes))


@hook.command
def voteFor(answerIndex, reply=None, db=None):
    """Casts a vote for the current poll."""
    if not db_ready: db_init(db)
    polls = db.execute("SELECT pollID FROM polls WHERE active = 1")
    if len(polls) == 0:
        reply("No poll is open at the moment.")
        return
    pollID = polls[0][0]
    answers = db.execute("SELECT answerID FROM answers WHERE pollID = %s AND 'index' = %s" % (pollID, answerIndex))
    if len(answers) == 0:
        reply("No item #%s found." % answerIndex)
        return
    answerID = answers[0][0]
    db.execute("DELETE FROM votes WHERE nick = %s AND answerID IN (SELECT answerID FROM answers WHERE pollID = %s)", (sender, pollID))
    db.execute("INSERT INTO votes (answerID, nick) VALUES (%s, %s)", (answerID, sender))
    reply("Vote registered.")


@hook.command
def voteNew(answer, reply=None, db=None):
    """Creates a new possible answer for the current poll and votes for it."""
    if not db_ready: db_init(db)
    polls = db.execute("SELECT pollID FROM polls WHERE active = 1")
    if len(polls) == 0:
        reply("No poll is open at the moment.")
        return
    pollID = polls[0][0]
    maxIndex = db.execute("SELECT MAX('index') FROM answers WHERE answers.pollID = %s", pollID)[0][0]
    if maxIndex == None:
        index = 1
    else:
        index = maxIndex + 1
    db.execute("INSERT INTO answers (pollID, 'index', answer) VALUES (%s, %s, %s)", (pollID, index, answer))
    answerID = db.execute("SELECT answerID FROM answers WHERE pollID = %s AND 'index' = %s", (pollID, index))[0][0]
    db.execute("DELETE FROM votes WHERE nick = %s AND answerID IN (SELECT answerID FROM answers WHERE pollID = %s)", (sender, pollID))
    db.execute("INSERT INTO votes (answerID, nick) VALUES (%s, %s)", (answerID, sender))
    reply("Vote added.")


@hook.command
def searchPoll(searchTerm, reply=None, db=None):
    """Search polls matching a given search term."""
    if not db_ready: db_init(db)
    polls = db.execute("SELECT pollID, question FROM polls WHERE question LIKE %s", ('%' + searchTerm + '%',))
    if len(polls) == 0:
        reply("No polls found.")
        return
    if len(polls) > 3:
        reply("%s entries found, refine your search" % len(polls))
        return
    for (pollID, question) in polls:
        winners = db.execute("SELECT answer, count(voteID) FROM answers INNER JOIN votes ON votes.answerID = answers.answerID WHERE pollID = %s GROUP BY answers.answerID, answer ORDER BY count(voteID) DESC LIMIT 1", (pollID, ))
        if len(winners) == 0:
            reply("%s. %s" % (pollID, question))
        else:
            reply("%s. %s -- Winner: %s (%s)" % (pollID, question, winners[0][0], winners[0][1]))


@hook.command(adminonly=True)
def deletePoll(pollID, reply=None, db=None):
    """Deletes a poll from the archives."""
    if not db_ready: db_init(db)
    if len(db.execute("SELECT pollID FROM polls WHERE pollID = %s", (pollID, ))) == 0:
        reply("No such poll found")
    db.execute("DELETE FROM votes WHERE answerID IN (SELECT answerID FROM answers WHERE pollID = %s)", (pollID, ))
    db.execute("DELETE FROM answers WHERE pollID = %s", (pollID, ))
    db.execute("DELETE FROM polls WHERE pollID = %s", (pollID, ))
    reply("Poll deleted.")
