# w3c validator plugin by ine (2020)
from util import hook
from utilities import request
from bs4 import BeautifulSoup


@hook.command('w3c')
@hook.command
def validate(inp):
    """validate <url> -- Runs url through the w3c markup validator."""

    if not inp.startswith('http'):
        inp = 'https://' + inp

    url = 'https://validator.w3.org/nu/?doc=' + request.urlencode(inp)
    html = request.get(url)
    soup = BeautifulSoup(html, 'lxml')
    results = soup.find('div', attrs={'id': 'results'})

    errors = len(results.find_all('li', attrs={'class': 'error'}))
    warns = len(results.find_all('li', attrs={'class': 'warning'}))
    info = len(results.find_all('li', attrs={'class': 'info'}))

    if errors == 0 and warns == 0 and info == 0:
        return "[w3c] Successfully validated with no errors"

    return "[w3c] Found {} errors, {} warnings and {} notices.".format(errors, warns, info)
