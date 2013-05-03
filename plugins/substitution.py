from util import hook
import re

lastmessage = {}

message_re = (r'.*', re.I)

#add /g fpr all

@hook.regex(*message_re)
def substitution(inp,chan=None,say=None,bot=None):
    try: disabled_channel_commands = bot.channelconfig[chan.lower()]['disabled_commands']
    except: disabled_channel_commands = " "
    if 'substitution' in disabled_channel_commands: return None

    curmessage=inp.group(0)
    regex = re.compile(r's/(.*)/(.*)', re.I)
    result = regex.match(curmessage)

    try: 
        if result.group(1) in lastmessage[chan]: say(re.sub(result.group(1),result.group(2),lastmessage[chan]))
    except: 
        lastmessage[chan]=curmessage