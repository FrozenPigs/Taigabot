from util import hook


@hook.command("stfu", adminonly=True)
@hook.command("silence", adminonly=True)
@hook.command(adminonly=True)
def shutup(inp, conn=None, chan=None, notice=None):
    "shutup [channel] <user> -- Shuts the user up. "

    users = inp.split(" ")

    if inp[0][0] == "#":
        chan = inp.split(" ")[0]
        users = inp.split(" ")[1:]

    for user in users:
        out = u"MODE %s +m-voh %s %s %s" % (chan, user, user, user)
        conn.send(out)
        notice(u"Shut up %s from %s..." % (user, chan))


@hook.command(adminonly=True)
def speak(inp, conn=None, chan=None, notice=None):
    "speak [channel] <user> -- Shuts the user up. "

    users = inp.split(" ")

    if inp[0][0] == "#":
        chan = inp.split(" ")[0]
        users = inp.split(" ")[1:]

    for user in users:
        out = u"MODE %s -m" % (chan)
        conn.send(out)
        notice(u"hey %s you can speak in %s again" % (user, chan))
