from util import hook
import time

countdown_is_running = False
countdown_nicks = []
countdown_timeout = 20


def set_countdown_to_true():
    global countdown_is_running
    countdown_is_running = True


def set_countdown_to_false():
    global countdown_is_running
    countdown_is_running = False


@hook.command(autohelp=False)
def countdown(inp, me=None):
    "countdown [seconds] [nick1 nick2 nick3] -- starts a countdown. It will begin when all the users type .ready"

    if countdown_is_running:
        return
    else:
        set_countdown_to_true()

    global countdown_nicks
    wait_count = 1
    inp = inp.lower().replace(',', '')
    count = 6

    try:
        if inp[0][0].isdigit():
            count = int(inp.split()[0]) + 1
            countdown_nicks = inp.split()[1:]
            if count > 6:
                count = 6
        else:
            countdown_nicks = inp.split()[0:]
            count = 6
    except Exception:
        pass

    if len(inp) > 6:
        nicks = ', '.join(countdown_nicks)
        me('Countdown started! Waiting for {}. Type \x02.ready\x02 when ready!'.format(nicks))

        # TODO fix: there can be only one countdown running per network
        # this chunk keeps the whole plugin busy
        while countdown_nicks:
            time.sleep(1)
            wait_count = int(wait_count) + 1
            if wait_count == countdown_timeout:
                set_countdown_to_false()
                return "Countdown expired."

        me('Ready! The countdown will begin in 2 seconds...')
        time.sleep(2)

    for cur in range(1, count):
        me('*** {} ***'.format(count - cur))
        time.sleep(1)
    else:
        set_countdown_to_false()
        return '\x02***\x02 GO \x02***\x02'


@hook.command(autohelp=False)
def ready(inp, me=None, nick=None):
    "ready -- when all users are ready the countdown will begin."
    global countdown_nicks
    nicks_size_start = len(countdown_nicks)
    try:
        countdown_nicks.remove(nick.lower())
    except Exception:
        pass

    if nicks_size_start > len(countdown_nicks):
        if len(countdown_nicks) > 0:
            me('Waiting for: ' + ', '.join(countdown_nicks))
