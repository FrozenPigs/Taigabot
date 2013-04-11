from util import hook, http
import re

@hook.command
def distance(inp):
    "distance <start> to <end> -- Calculate the distance between 2 places."
    if 'from ' in inp: inp = inp.replace('from ','')
    inp = inp.replace(', ','+')
    start = inp.split(" to ")[0].strip().replace(' ','+')
    dest = inp.split(" to ")[1].strip().replace(' ','+')
    url = "http://www.travelmath.com/flying-distance/from/%s/to/%s" % (start, dest)
    print url
    soup = http.get_soup(url)
    query = soup.find('h1', {'class': re.compile('flight-distance')})
    distance = soup.find('h3', {'class': 'space'})
    result = "%s %s" % (query, distance)
    result = http.strip_html(result)
    result = unicode(result, "utf8").replace('flight ','')

    if not distance:
        return "Could not calculate the distance from %s to %s." % (start, dest)

    return result