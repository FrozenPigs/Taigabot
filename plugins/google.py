from util import hook, http, database, web

imp_reg = (r'^\>(.*\.(gif|GIF|jpg|JPG|jpeg|JPEG|png|PNG|tiff|TIFF|bmp|BMP))'
           r'\s?(\d+)?')


def api_get(kind, query):
    """Use the RESTful Google Search API."""
    if kind == 'image':
        url = ('https://www.googleapis.com/customsearch/v1?key={}&cx={}'
               '&searchType={}&num=1&safe=off&q={}')
        return http.get_json(url.format(query[0], query[1], kind, query[2]))
    elif kind == 'images':
        url = ('https://www.googleapis.com/customsearch/v1?key={}&cx={}'
               '&searchType={}&num=1&safe=off&q={}&fileType="{}"')
        return http.get_json(url.format(query[0], query[1], 'image', query[2], query[3]))
    else:
        url = ('https://www.googleapis.com/customsearch/v1?key={}&cx={}'
               '&num=1&safe=off&q={}')
        return http.get_json(url.format(query[0], query[1], query[2].encode('utf-8')))
        # url = ('http://ajax.googleapis.com/ajax/services/search/{}?'
        #        'v=1.0&safe=off&q={}')
        # return http.get_json(url.format(kind, query))



@hook.command('search')
@hook.command('g')
@hook.command
def google(inp, bot=None, db=None, chan=None):
    """google <query> -- Returns first google search result for <query>."""
    trimlength = database.get(db,'channels','trimlength','chan',chan)
    if not trimlength: trimlength = 9999
    try:
        cx = bot.config['api_keys']['googleimage']
        key = bot.config['api_keys']['google']
        query = [key, cx, '+'.join(inp.split())]
        result = api_get('None', query)['items'][0]
    except:
        cx = bot.config['api_keys']['googleimage']
        key = bot.config['api_keys']['google2']
        query = [key, cx, '+'.join(inp.split())]
        result = api_get('None', query)['items'][0]
    title = result['title']
    content = http.html.fromstring(result['snippet'].replace('\n', '')).text_content()
    link = result['link']
    try:
        return u'{} -- \x02{}\x02: "{}"'.format(web.isgd(link), title, content)
    except:
        return u'{} -- \x02{}\x02: "{}"'.format(link, title, content)

    # parsed = api_get('web', '+'.join(inp.split()))
    # if not 200 <= parsed['responseStatus'] < 300:
    #     raise IOError('error searching for pages: {}: {}'.format(parsed['responseStatus'], ''))
    # if not parsed['responseData']['results']:
    #     return 'No results found.'

    # result = parsed['responseData']['results'][0]
    # title = http.unescape(result['titleNoFormatting'])
    # content = http.unescape(result['content'])

    # if not content: content = "No description available."
    # else: content = http.html.fromstring(content.replace('\n', '')).text_content()

    # try:
    #     return u'{} -- \x02{}\x02: "{}"'.format(web.isgd(result['unescapedUrl']), title, content)
    # except:
    #     return u'{} -- \x02{}\x02: "{}"'.format(result['unescapedUrl'], title, content)



@hook.command('gi')
def image(inp, reply=None, bot=None):
    """image <query> -- Returns the first Google Image result for <query>."""
    try:
        cx = bot.config['api_keys']['googleimage']
        key = bot.config['api_keys']['google']
        query = [key, cx, '+'.join(inp.split())]
        image = api_get('image', query)['items'][0]['link']
    except:
        cx = bot.config['api_keys']['googleimage']
        key = bot.config['api_keys']['google2']
        query = [key, cx, '+'.join(inp.split())]
        image = api_get('image', query)['items'][0]['link']
        #url = ('https://www.google.co.uk/search?tbm=isch&hl=en-GB&source=hp&bi'
        #       'w=&bih=&q={0}&gbv=2&oq={0}&gs_l=img.3..0l10.1471.1673.0.1792.3'
        #       '.3.0.0.0.0.86.231.3.3.0....0...1ac.1.34.img..0.3.231.tFWV7YPBE'
        #       'c8')
        #url = url.format('+'.join(inp.split()))
        #soup = http.get_soup(url)
        #for link in soup.find_all('a'):
        #    try:
        #        if link.get('class')[0] == 'rg_l':
        #            image = link.get('href')[15:].split('&')[0]
        #            break
        #    except TypeError:
        #        pass
    try:
        reply(web.isgd(image))
    except:
        reply(image)


@hook.regex(imp_reg)
def implying(inp, reply=None, bot=None):
    """><query>.jpg -- Returns the first Google Image result for <query>.jpg"""
    inp = inp.string[1:].split('.')
    filetype = inp[1]
    cx = bot.config['api_keys']['googleimage']
    key = bot.config['api_keys']['google']
    query = [key, cx, '+'.join(inp[0].split()), filetype]
    image = api_get('images', query)['items'][0]['link']
    try:
        reply(web.isgd(image))
    except:
        reply(image)
