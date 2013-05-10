from util import hook, http

@hook.command
def calc(inp):
    "calc <term> -- Calculate <term> with Google Calc."

    soup = http.get_soup('http://www.google.com/search', q=inp)


    result = soup.find('span', {'class': 'cwcot'})
    formula = soup.find('span', {'class': 'cwclet'})
    if not result:
        return "Could not calculate '%s'" % inp

    return "%s %s" % (formula.contents[0].strip(),result.contents[0].strip())
