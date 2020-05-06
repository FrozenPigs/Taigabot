from util import hook, database, http
import random

# RATINGS
# .RATE INFINITY BATTLESTATION 8/10

# .BS WOULD DISPLAY RATING AND TOTAL VOTES
#TYPE, NICK, VOTES, VOTERS

### Battlestations
@hook.command(autohelp=False)
def stats(inp, nick=None, conn=None, chan=None,db=None, notice=None):
    "battlestation <url | @ person> -- Shows a users Battlestation."
    if inp:
        if  "http" in inp:
            database.set(db,'users','battlestation',inp.strip(),'nick',nick)
            notice("Saved your battlestation.")
            return
        elif 'del' in inp:
            database.set(db,'users','battlestation','','nick',nick)
            notice("Deleted your battlestation.")
            return
        else:
            if '@' in inp: nick = inp.split('@')[1].strip()
            else: nick = inp.strip()

    result = database.get(db,'users','battlestation','nick',nick)
    if result: 
        return '{}: {}'.format(nick,result)
    else: 
        if not '@' in inp: notice(battlestation.__doc__)
        return 'No battlestation saved for {}.'.format(nick)


# 4 main compounds - bench, ohp, deadlift and squat. Body weight, height and bf?