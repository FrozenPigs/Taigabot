from util import hook, http, timesince, database
from datetime import datetime

api_url = "http://ws.audioscrobbler.com/2.0/?format=json"

@hook.command('np', autohelp=False)
@hook.command(autohelp=False)
def lastfm(inp, nick='', db=None, bot=None, notice=None):
    "lastfm [username | @ nick] [save] -- Displays the now playing (or last played) track of LastFM user [username]."
    api_key = bot.config.get("api_keys", {}).get("lastfm")
    if not api_key: return "error: no api key set"
    
    save = False
    
    if '@' in inp:
        nick = inp.split('@')[1].strip()
        user = database.get(db,'users','lastfm','nick',nick)
        if not user: return "No lastfm user stored for {}.".format(nick)
        # else: if inp.split(' ')[-1] == "url": return "[{}]: http://www.last.fm/user/{}".format(user,user)
    else:
        user = database.get(db,'users','lastfm','nick',nick)
        if not inp:
            if not user:
                notice(lastfm.__doc__)
                return
        else:
            if inp.split(' ')[-1] == "url": return "[{}]: http://www.last.fm/user/{}".format(user,user)
            if not user: save = True
            if " save" in inp: save = True
            user = inp.split()[0]

    # if inp.split(' ')[-1] == "url": return "[{}]: http://www.last.fm/user/{}".format(user,user)

    response = http.get_json(api_url, method="user.getrecenttracks", api_key=api_key, user=user, limit=1)

    if 'error' in response: return "Error: {}.".format(response["message"])

    if not "track" in response["recenttracks"] or len(response["recenttracks"]["track"]) == 0: return 'No recent tracks for user "{}" found.'.format(user)

    tracks = response["recenttracks"]["track"]

    # if the user is listening to something, the tracks entry is a list the first item is the current track
    if type(tracks) == list:
        track = tracks[0]
        status = 'is listening to'
        ending = '.'

    # otherwise, they aren't listening to anything right now, and the tracks entry is a dict representing the most recent track
    elif type(tracks) == dict:
        track = tracks
        status = 'last listened to'
        time_listened = datetime.fromtimestamp(int(track["date"]["uts"]))
        time_since = timesince.timesince(time_listened)
        ending = u' ({} ago)'.format(time_since)
    else:
        return "error: could not parse track listing"

    title = track["name"]
    album = track["album"]["#text"]
    artist = track["artist"]["#text"]

    out = u'{} {} "{}"'.format(user, status, title)
    if artist: out += u" by \x02{}\x0f".format(artist)
    if album: out += u" from the album \x02{}\x0f".format(album)
    out += ending
    if user and save: database.set(db,'users','lastfm',user,'nick',nick)

    return out

# ♫♫♫