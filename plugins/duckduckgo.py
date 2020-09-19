from util import hook
from json import loads as json_loads
from utilities import request

__version__ = 0.243


def query(query,
          useragent='python-duckduckgo ' + str(__version__),
          safesearch=False,
          html=False,
          meanings=True,
          **kwargs):
    """
    Query DuckDuckGo, returning a Results object.

    Here's a query that's unlikely to change:

    >>> result = query('1 + 1')
    >>> result.type
    'nothing'
    >>> result.answer.text
    '1 + 1 = 2'
    >>> result.answer.type
    'calc'

    Keword arguments:
    useragent: UserAgent to use while querying. Default: "python-duckduckgo %d" (str)
    safesearch: True for on, False for off. Default: True (bool)
    html: True to allow HTML in output. Default: False (bool)
    meanings: True to include disambiguations in results (bool)
    Any other keyword arguments are passed directly to DuckDuckGo as URL params.
    """ % __version__

    safesearch = '1' if safesearch else '-1'
    html = '0' if html else '1'
    meanings = '0' if meanings else '1'
    params = {
        'q': query.encode('utf-8'),
        'o': 'json',
        'kp': safesearch,
        'no_redirect': '1',
        'no_html': html,
        'd': meanings,
    }
    params.update(kwargs)

    response = request.get('https://api.duckduckgo.com/', params=params, headers={'User-Agent': useragent})
    json = json_loads(response)
    return Results(json)


class Results(object):

    def __init__(self, json):
        self.type = {
            'A': 'answer',
            'D': 'disambiguation',
            'C': 'category',
            'N': 'name',
            'E': 'exclusive',
            '': 'nothing'
        }.get(json.get('Type', ''), '')

        self.json = json
        self.api_version = None    # compat

        self.heading = json.get('Heading', '')

        self.results = [Result(elem) for elem in json.get('Results', [])]
        self.related = [
            Result(elem) for elem in json.get('RelatedTopics', [])
        ]

        self.abstract = Abstract(json)
        self.redirect = Redirect(json)
        self.definition = Definition(json)
        self.answer = Answer(json)

        self.image = Image({'Result': json.get('Image', '')})


class Abstract(object):

    def __init__(self, json):
        self.html = json.get('Abstract', '')
        self.text = json.get('AbstractText', '')
        self.url = json.get('AbstractURL', '')
        self.source = json.get('AbstractSource')


class Redirect(object):

    def __init__(self, json):
        self.url = json.get('Redirect', '')


class Result(object):

    def __init__(self, json):
        self.topics = json.get('Topics', [])
        if self.topics:
            self.topics = [Result(t) for t in self.topics]
            return
        self.html = json.get('Result')
        self.text = json.get('Text')
        self.url = json.get('FirstURL')

        icon_json = json.get('Icon')
        if icon_json is not None:
            self.icon = Image(icon_json)
        else:
            self.icon = None


class Image(object):

    def __init__(self, json):
        self.url = json.get('Result')
        self.height = json.get('Height', None)
        self.width = json.get('Width', None)


class Answer(object):

    def __init__(self, json):
        self.text = json.get('Answer')
        self.type = json.get('AnswerType', '')


class Definition(object):

    def __init__(self, json):
        self.text = json.get('Definition', '')
        self.url = json.get('DefinitionURL')
        self.source = json.get('DefinitionSource')


def get_zci(q,
            web_fallback=True,
            priority=['answer', 'abstract', 'related.0', 'definition'],
            urls=True,
            **kwargs):
    '''A helper method to get a single (and hopefully the best) ZCI result.
    priority=list can be used to set the order in which fields will be checked for answers.
    Use web_fallback=True to fall back to grabbing the first web result.
    passed to query. This method will fall back to 'Sorry, no results.'
    if it cannot find anything.'''

    ddg = query(q, **kwargs)
    response = ''

    for p in priority:
        ps = p.split('.')
        type = ps[0]
        index = int(ps[1]) if len(ps) > 1 else None

        result = getattr(ddg, type)
        if index is not None:
            if not hasattr(result, '__getitem__'):
                raise TypeError('%s field is not indexable' % type)
            result = result[index] if len(result) > index else None
        if not result: continue

        if result.text: response = result.text
        if result.text and hasattr(result, 'url') and urls:
            if result.url: response += ' (%s)' % result.url
        if response: break

    # if there still isn't anything, try to get the first web result
    if not response and web_fallback:
        if ddg.redirect.url:
            response = ddg.redirect.url

    # final fallback
    if not response:
        response = 'Sorry, no results.'

    return response


@hook.command
def ddg(inp):
    if len(inp) < 2:
        return 'Usage: .ddg <query>'

    return get_zci(inp)
