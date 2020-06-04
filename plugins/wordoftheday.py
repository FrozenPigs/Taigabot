# word of the day plugin by ine (2020)
from util import hook
from utilities import request, iterable
from bs4 import BeautifulSoup


@hook.command()
def wordoftheday(inp):
    html = request.get('https://www.merriam-webster.com/word-of-the-day')
    soup = BeautifulSoup(html)

    word = soup.find('div', attrs={'class': 'word-and-pronunciation'}).find('h1').text
    paragraphs = soup.find('div', attrs={'class': 'wod-definition-container'}).find_all('p')

    definitions = []

    for paragraph in iterable.limit(4, paragraphs):
        definitions.append(paragraph.text.strip())

    output = u"The word of the day is \x02{}\x02: {}".format(word, '; '.join(definitions))

    if len(output) > 320:
        output = output[:320] + '... More at https://www.merriam-webster.com/word-of-the-day'

    return output
