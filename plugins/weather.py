from util import hook, http, web, database
import urllib
import urllib2
import json
import yql
from bs4 import BeautifulSoup
from requests_oauthlib import OAuth1
import requests
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz
import time

def getlocation(db, location):
    latlong = database.get(db, 'location', 'latlong', 'location', location)
    address = database.get(db, 'location', 'address', 'location', location)
    if not latlong:
        locator = Nominatim(user_agent="Taiga").geocode(location)
        latlong = (locator.latitude, locator.longitude)
        database.set(db, 'location', 'latlong', '{},{}'.format(latlong[0], latlong[1]),
                     'location', location)
        address = locator.address.replace('United States of America', 'USA').replace(
            'United Kingdom', 'UK').encode('utf-8')
        database.set(db, 'location', 'address', address, 'location', location)
    else:
        latlong = latlong.split(',')
    return latlong, address
    


@hook.command('alerts', autohelp=False)
@hook.command('time', autohelp=False)
@hook.command('t', autohelp=False)
@hook.command('w', autohelp=False)
@hook.command('forecast', autohelp=False)
@hook.command(autohelp=False)
def weather(inp, bot=None, reply=None, db=None, nick=None, notice=None, paraml=None):
    "weather/time/alerts | <location> [save] | <@ user> -- Gets weather data for <location>."
    save = True
    command = paraml[-1].split(' ')[0][1:].lower()
    if '@' in inp:
        save = False
        nick = inp.split('@')[1].strip()
        userloc = database.get(db, 'users', 'location', 'nick', nick)
        latlong, address = getlocation(db, userloc)
        if not userloc:
            return "No location stored for {}.".format(
                nick.encode('ascii', 'ignore'))
    else:
        userloc = database.get(db, 'users', 'location', 'nick', nick)
        try:
            latlong, address = getlocation(db, userloc)
        except AttributeError:
            pass
        if not inp:
            if userloc == 'None':
                userloc = None
            if not userloc or userloc is None:
                notice(weather.__doc__)
                return
        else:
            if " dontsave" in inp:
                inp = inp.replace(' dontsave', '')
                save = False

    if inp and '@' not in inp:
        try:
            latlong, address = getlocation(db, inp)
        except AttributeError:
            notice("Could not find your location, try again.")
            notice(weather.__doc__)
            return

    if inp and save:
        database.set(db, 'users', 'location', inp.encode('utf-8'), 'nick',
                     nick)
        
    secret = bot.config.get("api_keys", {}).get("darksky")
    baseurl = 'https://api.darksky.net/forecast/{}/{},{}?exclude=minutely,flags,hourly'.format(
        secret, latlong[0], latlong[1])
    reply = json.loads(urllib.urlopen(baseurl).read())
    current = reply['currently']
    daily_current = reply['daily']['data'][0]

    if command == 'forecast':
        current = reply['daily']['data'][1]
        daily_current = reply['daily']['data'][1]
    if command == 'alerts':
        output = ''
        if 'alerts' not in reply:
            return 'No alerts for your location.'
        else:
            for alert in reply['alerts']:
                tz = pytz.timezone(reply['timezone'])
                output += '\x02{}\x02: \x02Starts:\x02 {}, \x02Ends:\x02 {}, \x02Severity:\x02 {}'.format(alert['title'].encode('utf-8'), datetime.fromtimestamp(alert['time'], tz).strftime('%Y-%m-%d %H:%M:%S'), datetime.fromtimestamp(alert['expires'], tz).strftime('%Y-%m-%d %H:%M:%S'), alert['severity'])
                if len(reply['alerts']) > 1 and reply['alerts'].index(alert) != len(reply['alerts']) -1:
                    output += ', '
                
            return output
    elif command == 'time' or command == 't':
        tz = pytz.timezone(reply['timezone'])
        time = datetime.fromtimestamp(current['time'], tz)
        return '\x02{}\x02: {}/{}'.format(address, time.strftime('%Y-%m-%d %I:%M:%S %p'), time.strftime('%H:%M:%S'))
    else: 
        tz = pytz.timezone(reply['timezone'])
        weather_data = {
            'place': address,
            'summary': current['summary'],
            'high_f': int(round(daily_current['temperatureMax'])),
            'high_c': int(round((daily_current['temperatureMax'] - 32) * 5 / 9)),
            'low_f': int(round(daily_current['temperatureMin'])),
            'low_c': int(round((daily_current['temperatureMin'] - 32) * 5 / 9)),
            'humidity': (str(current['humidity'])[2:] if len(str(current['humidity'])) >3 else ('100' if current['humidity'] == 1 else str(current['humidity'])[2:] + '0')),
            'wind_text': wind_type(current['windSpeed']),
            'wind_mph': int(round(current['windSpeed'])),
            'wind_kph': int(round(current['windSpeed'] * 1.609)),
            'wind_direction': wind_dir(current['windBearing']),
            'pressure': int(round(current['pressure'])),
            'uv_index': current['uvIndex']
        }
        try:
            weather_data['forecast'] = daily_current['summary'][:-1]
            weather_data['sunrise'] = datetime.fromtimestamp(daily_current['sunriseTime'], tz).strftime('%I:%M:%S %p')
            weather_data['sunset'] = datetime.fromtimestamp(daily_current['sunsetTime'], tz).strftime('%I:%M:%S %p')

        except KeyError:
            weather_data['forecast'] = 'no forecast'
            weather_data['sunrise'] = 'no sunrise'
            weather_data['sunset'] = 'no sunset'

        if command != 'forecast':
            weather_data['temp_f'] = int(round(current['temperature']))
            weather_data['temp_c'] = int(round((current['temperature'] - 32) * 5 / 9))
            weather_data['feel_f'] = int(round(current['apparentTemperature']))
            weather_data['feel_c'] = int(round((current['apparentTemperature'] - 32) * 5 / 9, 1))
        #uv index, moon phase, cloud cover, preasure, dew point, wind gust, sunset time, sunrise time, ozone,
        # precip intencity, precip probabilyty, precip type, precip intencity max
        output = "\x02{place}\x02: {summary}, {forecast}".format(
            **weather_data)
        if 'temp_f' in weather_data:
            output += ', \x02Currently:\x02 {temp_c}°C ({temp_f}°F), \x02Feels Like:\x02 {feel_c}°C ({feel_f}°F)'.format(
                **weather_data)
        output += ", \x02High:\x02 {high_c}°C ({high_f}°F), \x02Low:\x02 {low_c}°C ({low_f}°F), \x02Humidity:\x02 {humidity}%, \x02Wind:\x02 {wind_text} ({wind_mph} mph/{wind_kph} kph {wind_direction}), \x02Pressure:\x02 {pressure} mb, \x02Sunrise/Sunset:\02 {sunrise}/{sunset}".format(
            **weather_data)
        if weather_data['uv_index']:
            output += ', \x02UV:\x02 {uv_index}'.format(
                **weather_data)
        if 'alerts' in reply:
            output += ', \x0304\x02Alerts:\x02 {} (.alerts)\x03'.format(len(reply['alerts']))
        return output

def wind_dir(direction):
    if direction == 0 or direction == 360:
        return 'N'
    elif direction > 0 and direction < 90:
        return 'NE'
    elif direction == 90:
        return 'E'
    elif direction > 90 and direction < 180:
        return 'SE'
    elif direction == 180:
        return 'S'
    elif direction > 180 and direction < 270:
        return 'SW'
    elif direction == 270:
        return 'W'
    else:
        return 'NW'
        
def wind_type(mph):
    if mph < 1:
        return 'Calm'
    elif mph <= 3:
        return 'Light Air'
    elif mph <= 7:
        return 'Light Breeze'
    elif mph <= 12:
        return 'Gentle Breeze'
    elif mph <= 18:
        return 'Moderate Breeze'
    elif mph <= 24:
        return 'Fresh Breeze'
    elif mph <= 31:
        return 'Strong Breeze'
    elif mph <= 38:
        return 'High Wind'
    elif mph <= 46:
        return 'Gale'
    elif mph <= 54:
        return 'Strong Gale'
    elif mph <= 63:
        return 'Storm'
    elif mph <= 72:
        return 'Violent Storm'
    else:
        return 'Hurricane Force'


# @hook.command('w', autohelp=False)
# @hook.command(autohelp=False)
# def weather(inp, bot=None, reply=None, db=None, nick=None, notice=None):
#     "weather | <location> [save] | <@ user> -- Gets weather data for <location>."
#     #    baseurl = "https://query.yahooapis.com/v1/public/yql?"
#     save = True
#     baseurl = "https://weather-ydn-yql.media.yahoo.com/forecastrss?"
#     if '@' in inp:
#         save = False
#         nick = inp.split('@')[1].strip()
#         dbloc = database.get(db, 'users', 'location', 'nick', nick)
#         locator = Nominatim(user_agent="Taigabot").geocode(dbloc)
#         latlong = (locator.latitude, locator.longitude)
#         if not dbloc:
#             return "No location stored for {}.".format(
#                 nick.encode('ascii', 'ignore'))
#     else:
#         dbloc = database.get(db, 'users', 'location', 'nick', nick)
#         if not inp:
#             locator = Nominatim(user_agent="Taigabot").geocode(dbloc)
#             latlong = (locator.latitude, locator.longitude)
#             if dbloc == 'None':
#                 dbloc = None
#             if not dbloc or dbloc is None:
#                 notice(weather.__doc__)
#                 return
#         else:
#             # if not loc: save = True
#             if " dontsave" in inp:
#                 inp = inp.replace(' dontsave', '')
#                 save = False

#     if inp and '@' not in inp:
#         try:
#             locator = Nominatim(user_agent="Taigabot").geocode(inp)
#             latlong = (locator.latitude, locator.longitude)
#         except AttributeError:
#             notice("Could not find your location, try again.")
#             notice(weather.__doc__)
#             return

#     if inp and save:
#         database.set(db, 'users', 'location', inp.encode('utf-8'), 'nick',
#                      nick)

#     url = baseurl + urllib.urlencode({
#         'lat': latlong[0],
#         'lon': latlong[1]
#     }) + "&format=json"
#     secret = bot.config.get("api_keys", {}).get("yahoo")
#     id = bot.config.get("api_keys", {}).get("yahoo_id")
#     oauth = OAuth1(id, client_secret=secret)
#     result = requests.post(url=url, auth=oauth)
#     data = json.loads(result.content)

#     weather_data = {
#         'place':
#         data['location']['city'] + ',' + data['location']['region'] + ', ' +
#         data['location']['country'],
#         'conditions':
#         data['current_observation']['condition']['text'],
#         'temp_c':
#         unicode((int(data['current_observation']['condition']
#                      ['temperature']) - 32) * 5 / 9),
#         'temp_f':
#         data['current_observation']['condition']['temperature'],
#         'humidity':
#         data['current_observation']['atmosphere']['humidity'],
#         'wind_kph':
#         unicode(int(data['current_observation']['wind']['speed']) * 1.609),
#         'wind_mph':
#         data['current_observation']['wind']['speed'],
#         'forecast':
#         data['forecasts'][0]['text'],
#         'high_c':
#         unicode((int(data['forecasts'][0]['high']) - 32) * 5 / 9),
#         'low_c':
#         unicode((int(data['forecasts'][0]['low']) - 32) * 5 / 9),
#         'high_f':
#         data['forecasts'][0]['high'],
#         'low_f':
#         data['forecasts'][0]['low'],
#         '_forecast':
#         data['forecasts'][0]['text'],
#         '_high_c':
#         unicode((int(data['forecasts'][0]['high']) - 32) * 5 / 9),
#         '_low_c':
#         unicode((int(data['forecasts'][0]['low']) - 32) * 5 / 9),
#         '_high_f':
#         data['forecasts'][0]['high'],
#         '_low_f':
#         data['forecasts'][0]['low']
#     }
#     return "\x02{place}\x02 - \x02Current:\x02 {conditions}, {temp_f}F/{temp_c}C, Humidity: {humidity}%, " \
#         "Wind: {wind_kph}KPH/{wind_mph}MPH, \x02Today:\x02 {forecast}, " \
#         "High: {high_f}F/{high_c}C, Low: {low_f}F/{low_c}C. " \
#         "\x02Tomorrow:\x02 {_forecast}, High: {_high_f}F" \
#         "/{_high_c}C, Low: {_low_f}F/{_low_c}C.".format(**weather_data)


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
