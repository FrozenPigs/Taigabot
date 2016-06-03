from util import hook, http, web, database
import json
import urllib

base_url = 'https://query.yahooapis.com/v1/public/yql?'
def query(query):
        url = base_url + urllib.urlencode(query)
        response = urllib.urlopen(url)
        data = response.read()
	return data 

@hook.command('w', autohelp=False)
@hook.command('we', autohelp=False)
@hook.command(autohelp=False)
def weather(inp, nick=None, reply=None, db=None, notice=None):
    "weather | <location> [save] | <@ user> -- Gets weather data for <location>."
    save = True
    
    if '@' in inp:
        save = False
        nick = inp.split('@')[1].strip()
        loc = database.get(db,'users','location','nick',nick)
        if not loc: return "No location stored for {}.".format(nick.encode('ascii', 'ignore'))
    else:
        loc = database.get(db,'users','location','nick',nick)
        if not inp:
            if not loc:
                notice(weather.__doc__)
                return
        else:
            # if not loc: save = True
            if " dontsave" in inp: 
                inp = inp.replace(' dontsave','')
                save = False
            loc = inp.replace(' ','_') #.split()[0]

    location = http.quote_plus(loc)
    # location = location.replace(',','').replace(' ','-')

    # now, to get the actual weather
    try:

	    q ={
		'q': 'select title, units.temperature, item.forecast from weather.forecast where woeid in (select woeid from geo.places where text="'+ location+'") limit 1',
		 'format': 'json',
		 'env': 'store://datatables.org/alltableswithkeys'
		}

	    result = query(q)
	    data = json.loads(result)
	    weather = data["query"]["results"]["channel"]
	    average_F =  float((int(weather['item']['forecast']['high']) + int(weather['item']['forecast']['low']))/2)
	    average_C = round(float((average_F - 32) * (5.0/9.0)), 2)
    except KeyError:
        return "Could not get weather for that location."

    if location and save: database.set(db,'users','location',location,'nick',nick)

    # put all the stuff we want to use in a dictionary for easy formatting of the output
    weather_data = {
	'title': weather["title"].replace("Yahoo! Weather -", ""), 
	'current': weather['item']['forecast']['text'],
	'temp_f': average_F,
	'temp_c': average_C
    }
 
    reply("\x02{title}\x02 - \x02Current:\x02 {current}, {temp_f}F/{temp_c}C".format(**weather_data))

@hook.command(autohelp=False)
def save(inp, nick=None, reply=None, db=None, notice=None):
    "weather | <location> [save] | <@ user> -- Gets weather data for <location>."
    save = True
    loc = database.get(db,'users','location','nick',nick)
        if not inp:
            if not loc:
                notice(weather.__doc__)
                return
        else:
            # if not loc: save = True
            if " dontsave" in inp: 
                inp = inp.replace(' dontsave','')
                save = False
            loc = inp.replace(' ','_') #.split()[0]

    if location and save: database.set(db,'users','location',location,'nick',nick)
