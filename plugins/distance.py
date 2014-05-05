from util import hook, http
import re, math

def get_distance(origin, destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d

def get_location(location):
    location_data = http.get_json("http://maps.googleapis.com/maps/api/geocode/json?address={}&sensor=false".format(location))['results'][0]
    location_name = location_data['formatted_address']
    Location_latlong = [location_data['geometry']['location']['lat'], location_data['geometry']['location']['lng']]
    return (location_name, Location_latlong)

@hook.command
def distance(inp):
    """distance from <origin> to <dest> -- calculates the distance between any locations"""
    if 'from ' in inp: inp = inp.replace('from ','')
    inp = inp.replace(', ','+')
    orig = inp.split(" to ")[0].strip().replace(' ','+')
    dest = inp.split(" to ")[1].strip().replace(' ','+')
    try:
        orig_location, orig_latlong = get_location(orig)
        dest_location, dest_latlong = get_location(dest)
        distance_km = get_distance(orig_latlong, dest_latlong)
        distance_mile = distance_km * 0.621371

        return u"The distance from \x02%s\x02 to \x02%s\x02 is: %0.2f miles / %0.2f km" % (orig_location, dest_location, distance_mile, distance_km)
    except:
        return "Cannot get distance from {} to {}".format(orig,dest)