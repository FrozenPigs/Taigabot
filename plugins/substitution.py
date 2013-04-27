from util import hook
import re

lastmessage = {}

message_re = (r'.*', re.I)

@hook.regex(*message_re)
def getMessage(inp,chan=None,say=None):
    curmessage=inp.group(0)
    regex = re.compile(r's/(.*)/(.*)', re.I)
    result = regex.match(curmessage)
    try: say(re.sub(result.group(1),result.group(2),lastmessage[chan]))
    except: lastmessage[chan]=curmessage