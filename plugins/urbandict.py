from util import hook, request

base_url = 'https://api.urbandictionary.com/v0/define?term='


def search(input):
    json = request.get_json(base_url + request.urlencode(input))

    if json is None or "error" in json or "errors" in json:
        return ["the server fucked up"]

    data = []
    for item in json['list']:
        definition = item['definition']
        word = item['word']
        example = item['example']
        votes_up = item['thumbs_up']
        votes_down = item['thumbs_down']

        output = '\x02%s\x02 ' % word

        try:
            votes = int(votes_up) - int(votes_down)
            if votes > 0:
                votes = '+' + str(votes)
        except:
            votes = 0

        if votes != 0:
            output = output + '(%s) ' % votes

        output = output + definition.replace('[', '').replace(']', '')

        if example:
            output = output + ' \x02Example:\x02 ' + example.replace('\n', ' ')

        data.append(output)

    return data


@hook.command('u')
@hook.command('ud')
@hook.command('nig')
@hook.command('ebonics')
@hook.command
def urban(inp):
    "urban <phrase> -- Looks up <phrase> on urbandictionary.com."

    inp = inp.strip()
    results = search(inp)

    for result in results:
        return "[ud] " + result

    return "[ud] Not found"
