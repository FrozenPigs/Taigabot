# ScottSteiner 2014
from util import hook
from datetime import datetime
from pytz import timezone

@hook.command(autohelp=False)
def times(inp, bot=None):
    "times -- Shows times around the world."

    default_format = "%I:%M %p %Z"
    default_separator = " | "
    default_timezones = [
      ("Los Angeles", "America/Los_Angeles"),
      ("New York", "America/New_York"),
      ("London", "Europe/London"),
      ("Berlin", "Europe/Berlin"),
      ("Kiev", "Europe/Kiev"),
      ("Tokyo", "Asia/Tokyo")
    ]

    out = []
    utc = datetime.now(timezone('UTC'))

    tz_zones = bot.config["plugins"]["times"].get("time_zones", default_timezones)
    tz_format = bot.config["plugins"]["times"].get("format", default_format)
    tz_separator = bot.config["plugins"]["times"].get("separator", default_separator)

    for (location, tztext) in tz_zones:
      tzout = utc.astimezone(timezone(tztext)).strftime(tz_format)
      out.append("{} {}".format(location, tzout))

    return tz_separator.join(out)
