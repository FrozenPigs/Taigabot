from util import hook
import requests
import json


def color(change):
    if change < 0:
        # Orange
        return "05"
    else:
        # Green
        return "03"


@hook.command
def stock(inp, bot=None):
    """stock <symbol> -- gets stock information"""
    symbols = inp.upper()
    base_url = "https://cloud.iexapis.com/v1"
    token = bot.config["api_keys"]["iex"]
    params = {"token": token, "symbols": symbols, "types": "quote,stats"}

    try:
        data = requests.get(base_url + "/stock/market/batch", params=params)
        data = data.json()

        # https://iexcloud.io/docs/api/#quote
        quote_data = data[symbols]["quote"]

        current_price = quote_data["latestPrice"]
        symbol = quote_data["symbol"]
        day_high_price = quote_data["high"]
        day_low_price = quote_data["low"]
        day_change_percent = float("{:.2f}".format(quote_data["changePercent"] * 100))
        day_change_color = color(day_change_percent)
        day_change_percent = "\x03{}{}%\x03".format(
            day_change_color, day_change_percent
        )

        # https://iexcloud.io/docs/api/#key-stats
        stats_data = data[symbols]["stats"]
        name = stats_data["companyName"]

        year1_change_percent = float(
            "{:.2f}".format(stats_data["year1ChangePercent"] * 100)
        )
        year1_change_color = color(float(year1_change_percent))
        year1_change_percent = "\x03{}{}%\x03".format(
            year1_change_color, year1_change_percent
        )

        month_6_change_percent = float(
            "{:.2f}".format(stats_data["month6ChangePercent"] * 100)
        )
        month_6_change_color = color(float(month_6_change_percent))
        month_6_change_percent = "\x03{}{}%\x03".format(
            month_6_change_color, month_6_change_percent
        )

        day_30_change_percent = float(
            "{:.2f}".format(stats_data["day30ChangePercent"] * 100)
        )
        day_30_change_color = color(float(day_30_change_percent))
        day_30_change_percent = "\x03{}{}%\x03".format(
            day_30_change_color, day_30_change_percent
        )

        day_5_change_percent = float(
            "{:.2f}".format(stats_data["day5ChangePercent"] * 100)
        )
        day_5_change_color = color(float(day_5_change_percent))
        day_5_change_percent = "\x03{}{}%\x03".format(
            day_5_change_color, day_5_change_percent
        )

        if day_high_price:
            response = "\x02{} ({})\x02, Current: ${}, High: ${}, Low: ${}, 24h: {}, 5d: {}, 30d: {}, 6m: {}, 1y: {}".format(
                name,
                symbol,
                current_price,
                day_high_price,
                day_low_price,
                day_change_percent,
                day_5_change_percent,
                day_30_change_percent,
                month_6_change_percent,
                year1_change_percent,
            )
        # Not in trading hours
        else:
            response = "\x02{} ({})\x02, Current: ${}, 24h: {}, 5d: {}, 30d: {}, 6m: {}, 1y: {}".format(
                name,
                symbol,
                current_price,
                day_change_percent,
                day_5_change_percent,
                day_30_change_percent,
                month_6_change_percent,
                year1_change_percent,
            )
    except Exception as e:
        return "Could not get stock information for {}".format(symbols)

    return "[Stock] " + response
