# geoip plugin by ine (2020)
import re
from socket import gethostbyname
from util import hook
from utilities import request


dumb_ip_re = r'(\d+\.\d+\.\d+\.\d+)'
dumb_domain_re = r'([a-zA-Z0-9]+\.[a-zA-Z0-9]+)'


@hook.command
def geoip(inp):
    "geoip <host/ip> -- Gets the location of <host/ip>"

    if re.match(dumb_ip_re, inp):
        return parse_ip(inp)
    elif re.match(dumb_domain_re, inp):
        try:
            ip = gethostbyname(inp)
            return parse_ip(ip)
        except IOError:
            return "[IP] cant resolve that domain to ipv4"
    else:
        return "[IP] doesnt look like a valid ip or domain"


def parse_ip(ip):
    ip = request.urlencode(ip)
    data = request.get_json('https://ipinfo.io/' + ip, headers={'Accept': 'application/json'})

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
