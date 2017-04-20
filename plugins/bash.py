from util import hook, http
import random

bash_cache = []

def refresh_cache():
    "gets a page of random bash.org quotes and puts them into a dictionary "
    num = 0
    soup = http.get_soup('http://bash.org/?random')
    quote_infos = soup.find_all('p', {'class': 'quote'})
    quotes = soup.find_all('p', {'class': 'qt'})

    while num < len(quotes):
        quote_info = quote_infos[num].text
        quote = quotes[num].text.replace('\n', ' ').replace('\r', ' |')
        bash_cache.append((quote_info.split()[0].replace('#',''),quote_info.split()[1].split('(')[1].split(')')[0].strip(), quote))
        num += 1


def get_bash_quote(inp):
    try:
        soup = http.get_soup('http://bash.org/?%s' % inp)
        quote_info = soup.find('p', {'class': 'quote'}).text
        quote = soup.find('p', {'class': 'qt'}).text
        return (u'\x02#{}\x02 ({}): {}'.format(quote_info.split()[0].replace('#',''), quote_info.split()[1].split('(')[1].split(')')[0].strip(), quote.replace('\n', ' ').replace('\r', ' |')))
    except:
        return "No quote found."


#do an initial refresh of the cache
refresh_cache()

@hook.command(autohelp=False)
def bash(inp, reply=None):
    "bash <id> -- Gets a random quote from Bash.org, or returns a specific id."
    if inp: return get_bash_quote(inp)
    #grab the last item in the mlia cache and remove it
    id, votes, text = bash_cache.pop()
    # reply with the bash we grabbed
    reply(u'\x02#{}\x02 ({}): {}'.format(id, votes, text))
    # refresh bash cache if its getting empty
    if len(bash_cache) < 3:
        refresh_cache()
