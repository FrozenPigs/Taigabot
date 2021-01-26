from util import hook, database
import urllib
import json
from geopy.geocoders import Nominatim
from datetime import datetime
import pytz


def getlocation(db, location):
    print location
    try:
        location = location.decode("utf-8")
    except:
        pass
    latlong = database.get(db, 'location', 'latlong', 'location', location)
    address = database.get(db, 'location', 'address', 'location', location)
    if not latlong:
        location = location.encode('utf-8')
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
            weather_data['forecast'] = daily_current['summary'][:-1].encode('utf-8')
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

        for temp_type in ['temp', 'feel', 'high', 'low']:
            if (temp_type + '_f') in weather_data:
                try:
                    if int(weather_data[temp_type + '_f']) > 80:
                        weather_data[temp_type + '_f'] = '\x0304%s°F\x03' % weather_data[temp_type + '_f']
                        weather_data[temp_type + '_c'] = '\x0304%s°C\x03' % weather_data[temp_type + '_c']
                    elif int(weather_data[temp_type + '_f']) > 50:
                        weather_data[temp_type + '_f'] = '\x0303%s°F\x03' % weather_data[temp_type + '_f']
                        weather_data[temp_type + '_c'] = '\x0303%s°C\x03' % weather_data[temp_type + '_c']
                    else:
                        weather_data[temp_type + '_f'] = '\x0311%s°F\x03' % weather_data[temp_type + '_f']
                        weather_data[temp_type + '_c'] = '\x0311%s°C\x03' % weather_data[temp_type + '_c']
                except ValueError:
                    weather_data[temp_type + '_f'] = '%s°F' % weather_data[temp_type + '_f']
                    weather_data[temp_type + '_c'] = '%s°C' % weather_data[temp_type + '_c']

        if 'temp_f' in weather_data:
            output += ', \x02Currently:\x02 {temp_c} ({temp_f}), \x02Feels Like:\x02 {feel_c} ({feel_f})'.format(
                **weather_data)
        output += ", \x02High:\x02 {high_c} ({high_f}), \x02Low:\x02 {low_c} ({low_f}), \x02Humidity:\x02 {humidity}%, \x02Wind:\x02 {wind_text} ({wind_mph} mph/{wind_kph} kph {wind_direction}), \x02Pressure:\x02 {pressure} mb, \x02Sunrise/Sunset:\02 {sunrise}/{sunset}".format(
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
