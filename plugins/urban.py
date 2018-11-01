from util import hook, http, text

base_url = 'http://www.urbandictionary.com/iphone/search/define'

@hook.command('u')
@hook.command('ud')
@hook.command('nig')
@hook.command('ebonics')
@hook.command
def urban(inp):
    "urban <phrase> [id] -- Looks up <phrase> on urbandictionary.com."

    # clean and split the input
    input = inp.lower().strip()
    parts = input.split()

    # fetch the definitions
    page = http.get_json(base_url, term=input, referer="http://m.urbandictionary.com")
    defs = page['list']

    print defs
    # if the last word is a number, set the ID to that number
    if parts[-1].isdigit():
	print "hi1"
        id = int(parts[-1])
        # remove the ID from the input string
        del parts[-1]
        input = " ".join(parts)
    else:
	try:
	    id = 0
	    print "hi"
            for i in page['list']:
                if i['word'].lower() == input.lower():
	    	    id = page['list'].index(i)
                    break
        except:
            id = 1


    print id
    print page
    if page['list'] == []:
        return 'Not found.'

    # try getting the requested definition
    try:
        output = u"[%i/%i] \x02%s\x02: %s - %s" % \
              (id, len(defs), defs[id]['word'],
              defs[id]['definition'].replace('\r\n', ' '),defs[id]['example'].replace('\r\n', ' '))
    except IndexError:
        return 'Not found.'

    #return text.truncate_str(output, 250)
    return output
