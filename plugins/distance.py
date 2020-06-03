from util import hook
from utilities import request
from bs4 import BeautifulSoup


def fetch(start, dest):
    start = request.urlencode(start)
    dest = request.urlencode(dest)
    url = "http://www.travelmath.com/flying-distance/from/{}/to/{}".format(start, dest)
    html = request.get(url)
    return html


def parse(html):
    soup = BeautifulSoup(html, 'lxml')
    query = soup.find('h1', {'class': 'main'})
    distance = soup.find('h3', {'class': 'space'})

    if query:
        query = query.get_text().strip()

    if distance:
        distance = distance.get_text().strip()

    return query, distance


@hook.command
def distance(inp):
    "distance <start> to <end> -- Calculate the distance between 2 places."
    if 'from ' in inp:
        inp = inp.replace('from ', '')
    start = inp.split(" to ")[0].strip()
    dest = inp.split(" to ")[1].strip()

    html = fetch(start, dest)
    query, distance = parse(html)

    if not distance:
        return "Could not calculate the distance from {} to {}.".format(start, dest)

    result = u"Distance: {} {}".format(query, distance)
    return result
