# encyclopedia dramatica plugin by ine (2020)
from util import hook
from utilities import request
from bs4 import BeautifulSoup

api_url = "https://encyclopediadramatica.fyi/api.php?action=opensearch"
article_url = "https://encyclopediadramatica.fyi/index.php/"


@hook.command
def drama(inp):
    "drama <article> -- search an Encyclopedia Dramatica article"

    search = request.get_json(api_url + "&search=" + request.urlencode(inp))

    if not search[1]:
        return "No results found."

    title = search[1][0].replace(' ', '_').encode('utf8')

    html = request.get(article_url + request.urlencode(title))
    soup = BeautifulSoup(html, 'lxml')
    body = soup.find('div', attrs={'id': 'mw-content-text'})

    if body is None:
        return "Error finding the results"

    output = ''
    for paragraph in body.find_all('p'):
        output = output + " " + paragraph.text.strip()

    if len(output) > 320:
        output = output[:320] + '...'

    return title + " ::" + output
