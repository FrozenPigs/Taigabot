from util import hook, scheduler


@hook.command('remind')
@hook.command()
def reminder(inp, nick=None, conn=None):
    """reminder <time sec/min/hour/day/month/year> <message> --- reminds you of <message>."""
    inp = inp.replace('second', 'sec').replace('minute', 'min').replace('minutes', 'min').replace('hours', 'hour').replace('days', 'day').replace('weeks', 'week').replace('years', 'year').replace('seconds', 'second')
    timer = scheduler.check_for_timers(inp, 'reminder')
    inp = ' '.join(inp.split()[2:])
    if timer > 0:
        scheduler.schedule(timer, 1, "NOTICE {} :{}".format(nick, inp), conn)
