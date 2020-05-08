# Plugin by GhettoWizard and Scaevolus
import re
from util import hook, request
from bs4 import BeautifulSoup

dict_url = 'http://ninjawords.com/'
eth_url = 'https://www.etymonline.com/word/'


# merges spaces into just one
def condense_spaces(text):
    while '  ' in text:
        text = text.replace('  ', ' ')

    return text


@hook.command('dictionary')
@hook.command
def define(inp):
    "define <word> -- Fetches definition of <word>."

    html = request.get_html(dict_url + request.urlencode(inp))
    soup = BeautifulSoup(html, 'lxml')

    definitions = soup.find_all('dd')

    if len(definitions) == 0:
        return "Definition not found"

    output = 'Definition of "' + inp + '":'

    i = 1

    for definition in definitions:
        if 'article' in definition['class']:
            text = condense_spaces(definition.text.strip())
            output = output + ' \x02' + text + '\x02'
            i = 1

        elif 'entry' in definition['class']:
            definition = definition.find('div', attrs={'class': 'definition'})
            text = condense_spaces(definition.text.strip())
            output = output + text.replace(u'\xb0', ' \x02%s.\x02 ' % i)
            i = i + 1

        # theres 'synonyms' and 'examples' too

    # arbitrary length limit
    if len(output) > 360:
        output = output[:360] + '\x0f... More at https://en.wiktionary.org/wiki/' + inp

    return output


@hook.command
def etymology(inp):
    "etymology <word> -- Retrieves the etymology of <word>."

    html = request.get_html(eth_url + request.urlencode(inp))
    soup = BeautifulSoup(html, 'lxml')
    # the page uses weird class names like section.word__definatieon--81fc4ae
    # try changing the whole selector to  [class~="word_"]  if it breaks
    results = soup.select('div[class^="word"] section[class^="word__def"] > p')

    if len(results) == 0:
        return 'No etymology found for ' + inp + ' :('

    output = 'Ethymology of "' + inp + '":'
    i = 1

    for result in results:
        text = condense_spaces(result.text.strip())
        output = output + ' \x02{}.\x02 {}'.format(i, text)
        i = i + 1

    if len(output) > 400:
        output = output[:400] + '\x0f... More at https://www.etymonline.com/word/select'

    return output
