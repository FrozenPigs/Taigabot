from util import hook, http, timesince
from datetime import datetime

api_url = "http://ws.audioscrobbler.com/2.0/?format=json"

@hook.command('np', autohelp=False)
@hook.command('l', autohelp=False)
@hook.command(autohelp=False)
def lastfm(inp, nick='', say=None, db=None, bot=None, notice=None):
    "lastfm [user|@nick] [save] -- Displays the now playing (or last played)" \
    " track of LastFM user [user]."
    api_key = bot.config.get("api_keys", {}).get("lastfm")
    if not api_key:
        return "error: no api key set"

    db.execute("create table if not exists usernames(ircname primary key, lastfmname)")

    if not inp: # if there is no input, try getting the users lastfm name from db
        user = db.execute("select lastfmname from usernames where ircname=lower(?)", (nick,)).fetchone()
        if not user: # no lastfm saved in the database, send the user help text
            notice(lastfm.__doc__)
            return "No lastfm username stored for %s." % nick
        user = user[0]
        save = False # no need to save a lastfm, we already have it
    elif inp.endswith(" save"):
        user = inp[:-5].strip().lower() # remove "save" from the input string after checking for it
        save = True
    elif '@' in inp:
        nick = inp.replace('@','')
        user = db.execute("select lastfmname from usernames where ircname=lower(?)", (nick,)).fetchone()
        if not user: # no lastfm saved in the database
            return "No lastfm username stored for %s." % nick
        user = user[0]
        save = False # no need to save a lastfm, we already have it
    else: 
        user = db.execute("select lastfmname from usernames where ircname=lower(?)", (nick,)).fetchone() # check if user already has a lastfm
        # if not user: save = True # If theres no lastfm in the db, save it
        # else: 
        save = True 
        user = inp.strip().lower()


    response = http.get_json(api_url, method="user.getrecenttracks",
                             api_key=api_key, user=user, limit=1)

    if 'error' in response:
        return "Error: %s." % response["message"]

    if not "track" in response["recenttracks"] or len(response["recenttracks"]["track"]) == 0:
        return 'No recent tracks for user "%s" found.' % user

    tracks = response["recenttracks"]["track"]

    if type(tracks) == list:
        # if the user is listening to something, the tracks entry is a list
        # the first item is the current track
        track = tracks[0]
        status = 'is listening to'
        ending = '.'
    elif type(tracks) == dict:
        # otherwise, they aren't listening to anything right now, and
        # the tracks entry is a dict representing the most recent track
        track = tracks
        status = 'last listened to'
        # lets see how long ago they listened to it
        time_listened = datetime.fromtimestamp(int(track["date"]["uts"]))
        time_since = timesince.timesince(time_listened)
        ending = ' (%s ago)' % time_since

    else:
        return "error: could not parse track listing"

    title = track["name"]
    album = track["album"]["#text"]
    artist = track["artist"]["#text"]

    out = '%s %s "%s"' % (user, status, title)
    if artist:
        out += " by \x02%s\x0f" % artist
    if album:
        out += " from the album \x02%s\x0f" % album

    # append ending based on what type it was
    out += ending

    if user and save:
        db.execute("insert or replace into usernames(ircname, lastfmname) values (?,?)",
                     (nick.lower(), user))
        db.commit()

    return out
