from util import hook, http, web, database
import urllib
import urllib2
import json
import yql
from bs4 import BeautifulSoup
from requests_oauthlib import OAuth1
import requests
from geopy.geocoders import Nominatim


@hook.command('w', autohelp=False)
@hook.command(autohelp=False)
def weather(inp, bot=None, reply=None, db=None, nick=None, notice=None):
    "weather | <location> [save] | <@ user> -- Gets weather data for <location>."
    #    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    save = True
    baseurl = "https://weather-ydn-yql.media.yahoo.com/forecastrss?"
    if '@' in inp:
        save = False
        nick = inp.split('@')[1].strip()
        dbloc = database.get(db, 'users', 'location', 'nick', nick)
        locator = Nominatim(user_agent="Taigabot").geocode(dbloc)
        latlong = (locator.latitude, locator.longitude)
        if not dbloc:
            return "No location stored for {}.".format(
                nick.encode('ascii', 'ignore'))
    else:
        dbloc = database.get(db, 'users', 'location', 'nick', nick)
        if not inp:
            locator = Nominatim(user_agent="Taigabot").geocode(dbloc)
            latlong = (locator.latitude, locator.longitude)
            if dbloc == 'None':
                dbloc = None
            if not dbloc or dbloc is None:
                if not woeid:
                    notice(weather.__doc__)
                    return
        else:
            # if not loc: save = True
            if " dontsave" in inp:
                inp = inp.replace(' dontsave', '')
                save = False

    if inp and '@' not in inp:
        try:
            locator = Nominatim(user_agent="Taigabot").geocode(inp)
            latlong = (locator.latitude, locator.longitude)
        except AttributeError:
            notice("Could not find your location, try again.")
            notice(weather.__doc__)
            return

    if inp and save:
        database.set(db, 'users', 'location', inp, 'nick', nick)

    url = baseurl + urllib.urlencode({
        'lat': latlong[0],
        'lon': latlong[1]
    }) + "&format=json"
    secret = bot.config.get("api_keys", {}).get("yahoo")
    id = bot.config.get("api_keys", {}).get("yahoo_id")
    oauth = OAuth1(id, client_secret=secret)
    result = requests.post(url=url, auth=oauth)
    data = json.loads(result.content)

    weather_data = {
        'place':
        data['location']['city'] + ',' + data['location']['region'] + ', ' +
        data['location']['country'],
        'conditions':
        data['current_observation']['condition']['text'],
        'temp_c':
        unicode(
            (int(data['current_observation']['condition']['temperature']) - 32)
            * 5 / 9),
        'temp_f':
        data['current_observation']['condition']['temperature'],
        'humidity':
        data['current_observation']['atmosphere']['humidity'],
        'wind_kph':
        unicode(int(data['current_observation']['wind']['speed']) * 1.609),
        'wind_mph':
        data['current_observation']['wind']['speed'],
        'forecast':
        data['forecasts'][0]['text'],
        'high_c':
        unicode((int(data['forecasts'][0]['high']) - 32) * 5 / 9),
        'low_c':
        unicode((int(data['forecasts'][0]['low']) - 32) * 5 / 9),
        'high_f':
        data['forecasts'][0]['high'],
        'low_f':
        data['forecasts'][0]['low'],
        '_forecast':
        data['forecasts'][1]['text'],
        '_high_c':
        unicode((int(data['forecasts'][1]['high']) - 32) * 5 / 9),
        '_low_c':
        unicode((int(data['forecasts'][1]['low']) - 32) * 5 / 9),
        '_high_f':
        data['forecasts'][1]['high'],
        '_low_f':
        data['forecasts'][1]['low']
    }
    return "\x02{place}\x02 - \x02Current:\x02 {conditions}, {temp_f}F/{temp_c}C, Humidity: {humidity}%, " \
        "Wind: {wind_kph}KPH/{wind_mph}MPH, \x02Today:\x02 {forecast}, " \
        "High: {high_f}F/{high_c}C, Low: {low_f}F/{low_c}C. " \
        "\x02Tomorrow:\x02 {_forecast}, High: {_high_f}F" \
        "/{_high_c}C, Low: {_low_f}F/{_low_c}C.".format(**weather_data)


#@hook.command('w', autohelp=False)
#@hook.command('we', autohelp=False)
#@hook.command(autohelp=False)
#def weather(inp, bot=None, reply=None, db=None, nick=None, notice=None):
#    """weather | <location> [dontsave] | <@ user> -- Gets weather data for <location>."""
#    inp = ','.join(inp.replace(',', '').split())

#    save = True
#    if '@' in inp:
#        save = False
#        nick = inp.split('@')[1].strip()
#        loc = database.get(db,'users','location','nick',nick)
#        if not loc: return "No location stored for {}.".format(nick.encode('ascii', 'ignore'))
#    else:
#        loc = database.get(db,'users','location','nick',nick)
#        if not inp:
#            if not loc:
#                notice(weather.__doc__)
#                return
#            else:
#                inp = loc
#                save = False
#        else:
#            # if not loc: save = True
#            if " dontsave" in inp:
#                inp = inp.replace(' dontsave','')
#                save = False
#
#    if inp and save:
#        database.set(db,'users','location',inp,'nick',nick)
#    try:
#        if int(inp) or int(inp.split(',')[0]):
#            url = 'http://api.openweathermap.org/data/2.5/weather?zip={}&appid={}'
#        else:
#            url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
#    except:
#        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
#    json = http.get_json(url.format(inp, apikey))
#    place = json['name'] + ', ' + json['sys']['country']
#    conditions = json['weather'][0]['description']
#    temp_f = (json['main']['temp'] - 273.15) * 1.8000 + 32.00
#    temp_c = (json['main']['temp'] - 273.15) * 1
#    humidity = json['main']['humidity']
#    wind_kph = json['wind']['speed'] * 3.60
#    wind_mph = json['wind']['speed'] * 2.24
#    response = ('\x02{place}\x02 - \x02Current:\x02 {conditions}, {temp_f}F/'
#                '{temp_c}C, Humidity: {humidity}%, Wind: {wind_kph}KPH/'
#                '{wind_mph}MPH')
#    weather_data = {
#        'place': place,
#        'conditions': conditions,
#        'temp_f': temp_f,
#        'temp_c': temp_c,
#        'humidity': humidity,
#        'wind_kph': wind_kph,
#        'wind_mph': wind_mph
#    }
#    reply(response.format(**weather_data))
