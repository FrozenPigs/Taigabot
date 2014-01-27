from util import hook
# import re

# lastmessage = {}

# message_re = (r'.*', re.I)

# #add /g fpr all

# @hook.regex(*message_re)
# def substitution(inp,chan=None,say=None,bot=None):
#     try: disabled_channel_commands = bot.channelconfig[chan.lower()]['disabled_commands']
#     except: disabled_channel_commands = " "
#     if 'substitution' in disabled_channel_commands: return None

#     curmessage=inp.group(0)
#     regex = re.compile(r's/(.*)/(.*)', re.I)
#     result = regex.match(curmessage)

#     try: 
#         if result.group(1) in lastmessage[chan]: say(re.sub(result.group(1),result.group(2),lastmessage[chan]))
#     except: 
#         lastmessage[chan]=curmessage

@hook.regex(r'^(s|S)/.*/.*/\S*$')
def substitution(inp, message=None, input=None, notice=None, db=None):
    splitinput = input.msg.split("/")
    if splitinput[3]:
        nick = splitinput[3]
    else:
        nick = input.nick
    last_message = db.execute("select name, quote from seen_user where name"
                              " like ? and chan = ?", (nick.lower(), input.chan.lower())).fetchone()

    if last_message:
        splitinput = input.msg.split("/")
        find = splitinput[1]
        replace = splitinput[2]
        if find in last_message[1]:
            if "\x01ACTION" in last_message[1]:
                message = last_message[1].replace("\x01ACTION ", "/me ").replace("\x01", "")
            else:
                message = last_message[1]
            message(u"<{}> {}".format(message.replace(find, "\x02" + replace + "\x02"), nick))
        #else:
        #    notice(u"{} can't be found in your last message".format(find))
    else:
        if nick == input.nick:
            notice(u"I haven't seen you say anything here yet")
        else:
            notice(u"I haven't seen {} say anything here yet".format(nick))