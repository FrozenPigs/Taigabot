from util import hook
import re


@hook.regex(r'^(?:s|S)/(.+/.*)\S*$')
def correction(inp, nick=None, chan=None, say=None, input=None, notice=None, db=None):

    # if inpsplit[3]: nick = inpsplit[3]
    # else: nick = nick

    last_message = db.execute("select name, quote from seen where name like ? and chan = ?", (nick.lower(), chan.lower())).fetchone()

    if last_message:
        message = last_message[1]
        inpsplit = inp.group(0).split("/")
        find = inpsplit[1]
        replace = inpsplit[2]
        if find in message:
            if "\x01ACTION" in message: message = message.replace("\x01ACTION ", "/me ").replace("\x01", "")
            say(u"<{}> {}".format(nick, message.replace(find, "\x02" + replace + "\x02")))
        #else:
        #    notice(u"{} can't be found in your last message".format(find))
    else:
        if nick == input.nick:
            notice(u"I haven't seen you say anything here yet")
        else:
            notice(u"I haven't seen {} say anything here yet".format(nick))
