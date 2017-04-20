from util import hook, http


@hook.command()
def distro(inp, reply=None, bot=None):
    url = 'https://distrowatch.com/random.php'
    soup = http.get_soup(url)
    description =  filter(None, soup.find_all('body')[0].text.split('DistroWatch.com')[2].split('\n'))[4]
    url = soup.find_all('table', {'class': 'Info'})[0].find_all('a')[0].text 
    return url + ' - ' + description
