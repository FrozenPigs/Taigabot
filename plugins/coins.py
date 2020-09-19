# crypto coins plugin by ine
import json
from util import hook
from utilities import request

# update this like once a month
# https://api.coingecko.com/api/v3/coins/list
json_data = open("plugins/data/coingecko-coins.json", "r")
supported_coins = json.loads(json_data.read())
json_data.close()


base_url = 'https://api.coingecko.com/api/v3/coins/'
query_string = 'localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=false'


def consume_api(id):
    json = request.get_json(base_url + id + '?' + query_string)
    return json


def find_coin_id(inp):
    for coin in supported_coins:
        # it could be "if inp in coin:" but i want to search name (Bitcoin)
        # or code (BTC) only, because coingecko ids are nasty
        coin_id = coin[0]
        coin_symbol = coin[1]
        coin_name = coin[2]

        # dumb api sometimes returns nothing
        if "" in coin:
            continue

        # match name/symbol only
        if inp.lower() == coin_name.lower() or inp.lower() == coin_symbol:
            return coin

    return False


@hook.command('cg', autohelp=False)
@hook.command(autohelp=False)
def cryptocoin(inp):
    if inp == "":
        return "[coin] Search a coin with .cryptocoin <name> (or .cg eth)"

    coin = find_coin_id(inp)

    if coin is False:
        return "[coin] cryptocoin " + inp + " not found"

    data = consume_api(coin[0])

    # change this to support other (real) coins like eur, jpy, gbp, nok
    real_coin = 'usd'
    current = data['market_data']['current_price'][real_coin]
    high = data['market_data']['high_24h'][real_coin]
    low = data['market_data']['low_24h'][real_coin]
    volume = data['market_data']['total_volume'][real_coin]
    cap = data['market_data']['market_cap'][real_coin]
    change_24h = data['market_data']['price_change_percentage_24h']
    change_7d = data['market_data']['price_change_percentage_7d']
    # change_14d = data['market_data']['price_change_percentage_14d']
    change_30d = data['market_data']['price_change_percentage_30d']
    #change_60d = data['market_data']['price_change_percentage_60d']
    #change_200d = data['market_data']['price_change_percentage_200d']

    output = "[coin] {} ({}) Current: \x0307${:,}\x03, High: \x0307${:,}\x03, Low: \x0307${:,}\x03, Vol: ${:,}, Cap: ${:,}".format(coin[2], coin[1].upper(), current, high, low, volume, cap)

    if change_24h < 0:
        output = output + ", 24h: \x0304{:.2f}%\x03".format(change_24h)
    else:
        output = output + ", 24h: \x0303+{:.2f}%\x03".format(change_24h)

    if change_7d < 0:
        output = output + ", 7d: \x0304{:.2f}%\x03".format(change_7d)
    else:
        output = output + ", 7d: \x0303+{:.2f}%\x03".format(change_7d)

    if change_30d < 0:
        output = output + ", 30d: \x0304{:.2f}%\x03".format(change_30d)
    else:
        output = output + ", 30d: \x0303+{:.2f}%\x03".format(change_30d)

    return output


@hook.command('bitcoin', autohelp=False)
@hook.command(autohelp=False)
def btc(inp):
    return cryptocoin('bitcoin')


# <wednesday> .doge
# <Taigabot> Error: Doge is worthless.
# <wednesday> inex: keep .doge
# <wednesday> I like that
@hook.command(autohelp=False)
def doge(inp):
    return "Error: Doge is worthless."
