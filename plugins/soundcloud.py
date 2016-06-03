from util import hook, http, web, text, database
from urllib import urlencode
import re
import random
import urllib
import soundcloud


sc_re = (r'(.*:)//(www.)?(soundcloud.com)(.*)', re.I)
api_url = "http://api.soundcloud.com"
sndsc_re = (r'(.*:)//(www.)?(snd.sc)(.*)', re.I)

def soundcloudData(url, api_key):
    data = http.get_json(api_url + '/resolve.json?' + urlencode({'url': url, 'client_id': api_key}))
    print data

    desc = ""
    if data['description']: desc = u": {} ".format(text.truncate_str(data['description'], 50))

    genre = ""
    if data['genre']: genre = u"- Genre: \x02{}\x02 ".format(data['genre'])
        
    duration = ""
    if data['duration']:
        tracklength = float(data['duration']) / 60000
        tracklength = re.match('(.*\...)', str(tracklength)).group(1)
        if tracklength: duration = u"{} mins".format(tracklength)
        

    url = web.try_isgd(data['permalink_url'])

    return u"\x02{}\x02 by \x02{}\x02 {}".format(
        data['title'], data['user']['username'], duration)


@hook.regex(*sc_re)
def soundcloud_url(match, bot=None):
    api_key = bot.config.get("api_keys", {}).get("soundcloud")
    if not api_key:
        print "Error: no api key set"
        return None
    url = match.group(1).split(' ')[-1] + "//" + (match.group(2) if match.group(2) else "") + match.group(3) + \
          match.group(4).split(' ')[0]
    return soundcloudData(url, api_key)


@hook.regex(*sndsc_re)
def sndsc_url(match, bot=None):
    api_key = bot.config.get("api_keys", {}).get("soundcloud")
    if not api_key:
        print "Error: no api key set"
        return None
    url = match.group(1).split(' ')[-1] + "//" + (match.group(2) if match.group(2) else "") + match.group(3) + \
          match.group(4).split(' ')[0]
    return soundcloudData(http.open(url).url, api_key)




@hook.command('track', autohelp=False)
@hook.command('tracks', autohelp=False)
@hook.command(autohelp=False)
def randomtrack(inp, nick=None, conn=None, chan=None,db=None, paraml=None, bot=None):
	api_key = bot.config.get("api_keys", {}).get("soundcloud")
	api_secret = bot.config.get("api_keys", {}).get("soundcloud_secret")

	if not api_key or not api_secret:
		print "Error: no api key set"
		return None

	client = soundcloud.Client(client_id= api_key, client_secret= api_secret)

	try:	
		tracks = client.get('/tracks', genres = inp)
		track = random.choice(tracks)
		return "\x02{}\x02, genre: {}, url: {}".format(track.title, track.genre, track.permalink_url).decode('UTF-8') 
	except (IndexError, ValueError):
		return 'Error no tracks found'


@hook.command('stracks', autohelp=False)
@hook.command('strack', autohelp=False)
@hook.command(autohelp=False)
def searchtracks(inp, nick=None, conn=None, chan=None,db=None, paraml=None, bot=None):
	api_key = bot.config.get("api_keys", {}).get("soundcloud")
	api_secret = bot.config.get("api_keys", {}).get("soundcloud_secret")

	if not api_key or not api_secret:
		print "Error: no api key set"
		return None

	client = soundcloud.Client(client_id= api_key, client_secret= api_secret)

	try:	
		tracks = client.get('/tracks', q = inp)
		track = tracks[0] 
		return "\x02{}\x02, genre: {}, url: {}".format(track.title, track.genre, track.permalink_url).decode('UTF-8') 
	except (IndexError, ValueError):
		return 'Error no tracks found'

@hook.command('rtracks', autohelp=False)
@hook.command('rtrack', autohelp=False)
@hook.command(autohelp=False)
def randomsearchtracks(inp, nick=None, conn=None, chan=None,db=None, paraml=None, bot=None):
	api_key = bot.config.get("api_keys", {}).get("soundcloud")
	api_secret = bot.config.get("api_keys", {}).get("soundcloud_secret")

	if not api_key or not api_secret:
		print "Error: no api key set"
		return None

	client = soundcloud.Client(client_id= api_key, client_secret= api_secret)


	try:	
		tracks = client.get('/tracks', q = inp)
		track = random.choice(tracks) 
		return "\x02{}\x02, genre: {}, url: {}".format(track.title, track.genre, track.permalink_url).decode('UTF-8') 
	except (IndexError, ValueError):
		return 'Error no tracks found'

