# geoip plugin by ine (2020)
from util import hook
from utilities import request


@hook.command
def geoip(inp):
    "geoip <host/ip> -- Gets the location of <host/ip>"

    inp = request.urlencode(inp)
    data = request.get_json('https://ipinfo.io/' + inp, headers={'Accept': 'application/json'})

    if data.get('error') is not None:
        if data['error'].get('title') == 'Wrong ip':
            return '[IP] That IP is not valid'
        else:
            return '[IP] Some error ocurred'

    # example for 8.8.8.8
    loc = data.get('loc')  # 37.40, -122.07
    city = data.get('city')  # Mountain View
    country = data.get('country')  # US
    region = data.get('region')  # California
    hostname = data.get('hostname')  # dns.google
    timezone = data.get('timezone')  # unreliable
    ip = data.get('ip')  # 8.8.8.8
    org = data.get('org')  # Google LLC

    return u"[IP] {} - {}, {}, {}".format(org, city, region, country)
