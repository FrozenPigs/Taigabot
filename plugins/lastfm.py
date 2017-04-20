from util import hook, http, database
import time
from datetime import datetime

@hook.command
def band(inp, bot=None):
    artist = inp
    print artist
    api_key = bot.config['api_keys']['lastfm']
    api_url = 'http://ws.audioscrobbler.com/2.0/?format=json'
    query_params = {'method': 'artist.getInfo',
                    'artist': artist,
                    'api_key': api_key}
    response = http.get_json(api_url, query_params=query_params)
    plays = response['artist']['stats']['playcount']
    listeners = response['artist']['stats']['listeners']
    similar = []
    for i in response['artist']['similar']['artist']:
        similar.append(i['name'])
    similar = ", ".join(similar)
    tags = []
    for i in response['artist']['tags']['tag']:
        tags.append(i['name'])
    tags = ', '.join(tags)
    return artist + ' have ' + plays + ' plays and ' + listeners +'. Similar artists include ' + similar +'. Tags: (' + tags + ').'


@hook.command('np', autohelp=False)
@hook.command(autohelp=False)
def lastfm(inp, db=None, bot=None, reply=None, chan=None, notice=None, nick=None, conn=None):
    """lastfm [username|@nick] -- Displays the current/last played track."""
    api_key = bot.config['api_keys']['lastfm']
    api_url = 'http://ws.audioscrobbler.com/2.0/?format=json'
    save = False
    if '@' in inp:
        nick = inp.split('@')[1].strip()
        user = database.get(db, 'users', 'lastfm', 'nick', nick)
        if not user:
            reply('No lastfm user stored for {}.'.format(nick))
    else:
        user = database.get(db, 'users', 'lastfm', 'nick', nick)
        if not inp:
            if not user:
                notice('[{}]: {}{}'.format(chan, conn.conf.get('command_prefix'),
                       lastfm.__doc__))
                return
        else:
            if not user:
                save = True
            if ' save' in inp:
                save = True
            user = inp.split()[0]

    if user == None:
        return
    query_params = {'method': 'user.getRecentTracks',
                    'user': user,
                    'limit': 1,
                    'api_key': api_key}
    if not api_key:
        reply('Error: no api key set')
    response = http.get_json(api_url, query_params=query_params)
    try:
        track = response['recenttracks']['track'][0]
    except IndexError:
        notice('[{}] {} has no recent tracks.'.format(chan, user))
        return
    title = track['name']
    artist = track['artist']['#text']
    album = track['album']['#text']
    if album == '':
        album = 'Unknown Album'
    try:
        tag_params = {'method': 'track.getTopTags',
                        'track': title,
                        'artist': artist,
                        'api_key': api_key}
        tagr = http.get_json(api_url, query_params=tag_params)
        tagr = tagr['toptags']['tag'][0:5]
        tags = []
        for i in tagr:
            tags.append(i['name'])
        tags = ', '.join(tags)
    except:
        tags = ''
    try:
        pc_params = {'method': 'track.getInfo',
                        'track': title,
                        'artist': artist,
                        'username': user,
                        'api_key': api_key}
        pc = http.get_json(api_url, query_params=pc_params)
        played = pc['track']['userplaycount']
    except:
        played = ''
    try:
        listened = datetime.strptime(track['date']['#text'], '%d %b %Y, %H:%M')
        curtime = datetime.fromtimestamp(time.time())
        curtime = datetime.strptime(str(curtime), '%Y-%m-%d %H:%M:%S.%f')
        diff = str((curtime - listened))
        listened = diff.split('.')[0]
        if listened[0:2] == '-1':
            listened = listened[8:-6] + ' seconds'
        elif listened[0] == '0':
            if listened[2:4] == '01':
                listened = listened[3:-3] + ' minute'
            elif listened[2:3] == '0':
                if listened[2:4] == '00':
                    listened = '1 minute'
                else:
                    listened = listened[3:-3] + ' minutes'
            else:
                listened = listened[2:-3] + ' minutes'
        else:
            if listened[-8:-6] == ' 1' or listened[0:2] == '1:':
                listened = listened[:-6] + ' hour'
            else:
                listened = listened[:-6] + ' hours'

        if tags:
            out = (u'{} listened to "{}" by \x02{}\x02 from the'
                   u' album \x02{}\x02 {} ago, Play Count: {}, Tags: {}'
                   .format(user, title, artist, album, listened, played, tags))
        else:
            out = (u'{} listened to "{}" by \x02{}\x02 from the'
                   u' album \x02{}\x02 {} ago, Play Count: {}.'
                   .format(user, title, artist, album, listened, played))
    except KeyError:
        if tags:
            out = (u'{} is listening to "{}" by \x02{}\x02 from the'
                   u' album \x02{}\x02, Play Count: {}, Tags: {}.'
                   .format(user, title, artist, album, played, tags))
        else:
            out = (u'{} is listening to "{}" by \x02{}\x02 from the'
                   u' album \x02{}\x02, Play Count: {}.'
                   .format(user, title, artist, album, played))
    if user and save:
        database.set(db, 'users', 'lastfm', user, 'nick', nick)
    reply(out)
