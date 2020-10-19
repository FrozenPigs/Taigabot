from util import formatting, hook, http, web
import re
import requests

gateway = 'http://open.spotify.com/{}/{}'  # http spotify gw address
spuri = 'spotify:{}:{}'

spotify_re = (r'(spotify:(track|album|artist|user):([a-zA-Z0-9]+))', re.I)
http_re = (r'(open\.spotify\.com\/(track|album|artist|user)\/'
           '([a-zA-Z0-9]+))', re.I)


def get_access_token(client_id, client_secret):
    """ Get Spotify access token based on client_id and client_secret
    Required to use Spotify's search APIs
    """

    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    auth_response_data = auth_response.json()
    access_token = auth_response_data['access_token']
    return access_token


@hook.command('sp')
@hook.command('song')
@hook.command
def spotify(inp, bot=None):
    """spotify <song> -- Search Spotify for <song>"""

    # Get access token
    try:
        access_token = get_access_token(bot.config['api_keys']['spotify_client_id'],
                                        bot.config['api_keys']['spotify_client_secret'])
    except Exception as e:
        return "Could not get Spotify access token: {}".format(e)

    # Query track
    try:
        headers = {'Authorization': 'Bearer ' + access_token}
        params = {'q': inp, 'type': 'track', 'limit': 1}
        data = requests.get('https://api.spotify.com/v1/search',
                            headers=headers,
                            params=params)
        data = data.json()
    except Exception as e:
        return "Could not get track information: {}".format(e)

    # Parsing data and returning
    try:
        first_result = data["tracks"]["items"][0]
        artists = []
        for a in first_result["artists"]:
            artists.append(a["name"])
        artist = ', '.join(artists).encode("utf-8")
        track = first_result["name"].encode("utf-8")
        album = first_result["album"]["name"].encode("utf-8")
        url = first_result["external_urls"]["spotify"]
        uri = first_result["uri"]
        song_query_output = "\"{}\" by \x02{}\x02 from the album \x02{}\x02 - {} ({})".format(
            track, artist, album, url, uri)
    except IndexError:
        return "Could not find track."

    return formatting.output('Spotify', [song_query_output])


@hook.command('album')
@hook.command
def spalbum(inp, bot=None):
    """spalbum <album> -- Search Spotify for <album>"""

    # Get access token
    try:
        access_token = get_access_token(bot.config['api_keys']['spotify_client_id'],
                                        bot.config['api_keys']['spotify_client_secret'])
    except Exception as e:
        return "Could not get Spotify access token: {}".format(e)

    # Query artist
    try:
        headers = {'Authorization': 'Bearer ' + access_token}
        params = {'q': inp, 'type': 'album', 'limit': 1}
        data = requests.get('https://api.spotify.com/v1/search',
                            headers=headers,
                            params=params)
        data = data.json()

    except Exception as e:
        return "Could not get album information: {}".format(e)

    # Parsing data and returning
    try:
        first_result = data["albums"]["items"][0]
        artists = []
        for a in first_result["artists"]:
            artists.append(a["name"])
        artist = ', '.join(artists).encode("utf-8")
        album = first_result["name"].encode("utf-8")
        url = first_result["external_urls"]["spotify"]
        uri = first_result["uri"]
        album_query_output = "\x02{}\x02 - \x02{}\x02 - {} ({})".format(
            artist, album, url, uri)
    except IndexError:
        return "Could not find album."

    return formatting.output('Spotify', [album_query_output])


@hook.command('artist')
@hook.command
def spartist(inp, bot=None):
    """spartist <artist> -- Search Spotify for <artist>"""

    # Get access token
    try:
        access_token = get_access_token(bot.config['api_keys']['spotify_client_id'],
                                        bot.config['api_keys']['spotify_client_secret'])
    except Exception as e:
        return "Could not get Spotify access token: {}".format(e)

    # Query artist
    try:
        headers = {'Authorization': 'Bearer ' + access_token}
        params = {'q': inp, 'type': 'artist', 'limit': 1}
        data = requests.get('https://api.spotify.com/v1/search',
                            headers=headers,
                            params=params)
        data = data.json()
        print(data)
    except Exception as e:
        return "Could not get artist information: {}".format(e)

    # Parsing data and returning
    try:
        first_result = data["artists"]["items"][0]
        artist = first_result["name"].encode("utf-8")

        genres = ', '.join(first_result["genres"]).encode("utf-8")
        url = first_result["external_urls"]["spotify"]
        uri = first_result["uri"]

        # Spotify has genre tags for many artists but not all
        if genres:
            artist_query_output = "\x02{}\x02, \x02Genres\x02: {} - {} ({})".format(
                artist, genres, url, uri)
        else:
            artist_query_output = "\x02{}\x02 - {} ({})".format(
                artist, url, uri)

    except IndexError:
        return "Could not find artist."

    return formatting.output('Spotify', [artist_query_output])


@hook.regex(*http_re)
@hook.regex(*spotify_re)
def spotify_url(match, bot=None):
    """ Match spotify urls and provide blurb and track
    """

    # Regex match on spotify urls and see if url links to track/album/artist
    type = match.group(2)
    spotify_id = match.group(3)
    url = spuri.format(type, spotify_id)

    # Get access token
    try:
        access_token = get_access_token(bot.config['api_keys']['spotify_client_id'],
                                        bot.config['api_keys']['spotify_client_secret'])
    except Exception as e:
        return "Could not get Spotify access token: {}".format(e)

    # Set appropriate headers
    headers = {'Authorization': 'Bearer ' + access_token}

    # Parse track link and retrieve data for blurb
    if type == "track":
        try:
            data = requests.get('https://api.spotify.com/v1/tracks/{}'.format(spotify_id),
                                headers=headers)
            data = data.json()
        except Exception as e:
            return "Could not get album information: {}".format(e)

        try:
            first_result = data
            artists = []
            for a in first_result["artists"]:
                artists.append(a["name"])
            artist = ', '.join(artists).encode("utf-8")
            track = first_result["name"].encode("utf-8")
            album = first_result["album"]["name"].encode("utf-8")
            song_query_output = "\"{}\" by \x02{}\x02 from the album \x02{}\x02".format(
                track, artist, album)
        except IndexError:
            return "Could not find track."

        return formatting.output('Spotify', [song_query_output])

    # Parse album link and retrieve data for blurb
    if type == "album":
        try:
            data = requests.get('https://api.spotify.com/v1/albums/{}'.format(spotify_id),
                                headers=headers)
            data = data.json()
        except Exception as e:
            return "Could not get album information: {}".format(e)

        try:
            first_result = data
            artists = []
            for a in first_result["artists"]:
                artists.append(a["name"])
            artist = ', '.join(artists).encode("utf-8")
            album = first_result["name"].encode("utf-8")
            album_query_output = "\x02{}\x02 - \x02{}\x02".format(
                artist, album)
        except IndexError:
            return "Could not find album."

        return formatting.output('Spotify', [album_query_output])

    # Parse artist link and retrieve data for blurb
    if type == "artist":
        try:
            data = requests.get('https://api.spotify.com/v1/artists/{}'.format(spotify_id),
                                headers=headers)
            data = data.json()
        except Exception as e:
            return "Could not get artist information: {}".format(e)

        try:
            first_result = data
            artist = first_result["name"].encode("utf-8")
            genres = ', '.join(first_result["genres"]).encode("utf-8")
            # Spotify has genre tags for many artists but not all
            if genres:
                artist_query_output = "\x02{}\x02, \x02Genres\x02: {}".format(
                    artist, genres)
            else:
                artist_query_output = "\x02{}\x02".format(
                    artist)
        except IndexError:
            return "Could not find artist."

        return formatting.output('Spotify', [artist_query_output])
