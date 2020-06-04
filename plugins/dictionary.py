# dictionary and etymology plugin by ine (2020)
from util import hook
from utilities import request, formatting
from bs4 import BeautifulSoup

dict_url = 'http://ninjawords.com/'
eth_url = 'https://www.etymonline.com/word/'


@hook.command('dictionary')
@hook.command
def define(inp):
    "define <word> -- Fetches definition of <word>."

    html = request.get(dict_url + request.urlencode(inp))
    soup = BeautifulSoup(html, 'lxml')

    definitions = soup.find_all('dd')

    if len(definitions) == 0:
        return "Definition not found"

    output = 'Definition of "' + inp + '":'

    # used to number the many definitions
    i = 1

    for definition in definitions:
        if 'article' in definition['class']:
            text = formatting.compress_whitespace(definition.text.strip())
            output = output + ' \x02' + text + '\x02'
            i = 1

        elif 'entry' in definition['class']:
            definition = definition.find('div', attrs={'class': 'definition'})
            text = formatting.compress_whitespace(definition.text.strip())
            output = output + text.replace(u'\xb0', ' \x02{}.\x02 '.format(i))
            i = i + 1

        # theres 'synonyms' and 'examples' too

    # arbitrary length limit
    if len(output) > 360:
        output = output[:360] + '\x0f... More at https://en.wiktionary.org/wiki/' + inp

    return output


@hook.command
def etymology(inp):
    "etymology <word> -- Retrieves the etymology of <word>."

    html = request.get(eth_url + request.urlencode(inp))
    soup = BeautifulSoup(html, 'lxml')
    # the page uses weird class names like "section.word__definatieon--81fc4ae"
    # if it breaks change the selector to [class~="word_"]
    results = soup.select('div[class^="word"] section[class^="word__def"] > p')

    if len(results) == 0:
        return 'No etymology found for ' + inp

    output = u'Ethymology of "' + inp + '":'
    i = 1

    for result in results:
        text = formatting.compress_whitespace(result.text.strip())
        output = output + u' \x02{}.\x02 {}'.format(i, text)
        i = i + 1

    if len(output) > 400:
        output = output[:400] + '\x0f... More at https://www.etymonline.com/word/select'

    return output
