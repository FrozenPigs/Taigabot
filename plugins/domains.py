from util import hook, http
import urlparse
import re
# import whois

# @hook.command
# def whois(inp):
#     """whois <domain> - lookup domains information"""
#     w = whois('google.com')
#     print w.expiration_date    



    #for x in domain:
    #    print "{}: {}".format(x,domain[x])
    #{'expiration_date': datetime.datetime(2020, 9, 14, 0, 0), 'last_updated': datetime.datetime(2011, 7, 20, 0, 0), 'registrar': 'MARKMONITOR INC.', 'name': 'google.com', 'creation_date': datetime.datetime(1997, 9, 15, 0, 0)}
    # domain = pythonwhois.get_whois(inp)
    # print(domain.id)
    # print(domain.status)
    # print(domain.creation_date)
    # print(domain.expiration_date)
    # print(domain.registrar)
    # print(domain.nameservers)









# @hook.command
# def domain(inp):
#     url = "http://who.is/whois/{}".format(inp)
#     page = http.get_html(url)
#     server_type = page.xpath("//span@data-bind-domain='server_type']/text()")[0].strip()
#     return server_type

@hook.command
def domainr(inp):
    """domainr <domain> - Use domain.nr's API to search for a domain, and similar domains."""
    try:
        data = http.get_json('http://domai.nr/api/json/search?q=' + inp)
    except (http.URLError, http.HTTPError) as e:
        return "Unable to get data for some reason. Try again later."
    if data['query'] == "":
        return "An error occurrred: {status} - {message}".format(**data['error'])
    domains = ""
    for domain in data['results']:
        domains += ("\x034" if domain['availability'] == "taken" else (
            "\x033" if domain['availability'] == "available" else "\x031")) + domain['domain'] + "\x0f" + domain[
            'path'] + ", "
    return "Domains: " + domains


@hook.command('isup')
@hook.command
def isdown(inp):
    "isdown <url> -- Checks if the site at <url> is up or down."

    if 'http://' not in inp:
        inp = 'http://' + inp

    inp = 'http://' + urlparse.urlparse(inp).netloc

    # http://mail.python.org/pipermail/python-list/2006-December/589854.html
    try:
        http.get(inp, get_method='HEAD')
        return inp + ' seems to be up'
    except http.URLError:
        return inp + ' seems to be down'
