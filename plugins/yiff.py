from util import hook
import random

with open("plugins/data/yiffs.txt") as f:
    yiffs = [line.strip() for line in f.readlines()
             if not line.startswith("//")]

@hook.command
def yiff(inp, action=None, nick=None, conn=None, notice=None):
    """lart <user> -- yiffs <user>."""
    target = inp.strip()

    if " " in target:
        notice("Invalid username!")
        return

    # if the user is trying to make the bot slap itself, slap them
    if target.lower() == conn.nick.lower() or target.lower() == "itself":
        target = nick

    values = {"user": target}
    phrase = random.choice(yiffs)

    # act out the message
    action(phrase.format(**values))