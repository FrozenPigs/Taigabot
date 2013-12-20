from util import http, hook
#import lxml
#from lxml.html import parse 

@hook.command('bitcoin',autohelp=False)
@hook.command('buttcoin',autohelp=False)
@hook.command(autohelp=False)
def btc(inp, say=None):
    "bitcoin -- gets current exchange rate for bitcoins from mtgox"
    data = http.get_json("http://data.mtgox.com/api/2/BTCUSD/money/ticker")
    data = data['data']
    ticker = {
        'buy': data['buy']['display_short'],
        'high': data['high']['display_short'],
        'low': data['low']['display_short'],
        'vol': data['vol']['display_short'],
    }

    data = http.get_json("http://data.mtgox.com/api/1/generic/order/lag")
    data = data['return']
    lag = {
        'lag': data['lag_text']
    }

    result = ("Current: \x0307%(buy)s\x0f - High: \x0307%(high)s\x0f"
        " - Low: \x0307%(low)s\x0f - Volume: %(vol)s" % ticker)
    result_lag = ("Lag: %(lag)s" % lag)

    say("%s - %s" % (result, result_lag))


@hook.command('litecoin',autohelp=False)
@hook.command(autohelp=False)
def ltc(inp, say=None):
    "litecoin -- gets current exchange rate for litecoins from mtgox"
    data = http.get_json("https://btc-e.com/api/2/ltc_usd/ticker")
    data = data['ticker']
    ticker = {
        'buy': data['buy'],
        'high': data['high'],
        'low': data['low'],
        'vol': data['vol'],
    }

    result = ("Current: \x0307%(buy)s\x0f - High: \x0307%(high)s\x0f"
        " - Low: \x0307%(low)s\x0f - Volume: %(vol)s" % ticker)

    say("%s" % (result))


@hook.command(autohelp=False)
def doge(inp, say=None):
    ".doge -- Returns the value of a dogecoin."
    # get btc price
    data = http.get_json("http://data.mtgox.com/api/2/BTCUSD/money/ticker")
    data = data['data']
    ticker = {'buy': data['buy']['display_short']}
    bitcoin_price = ("%(buy)s" % ticker).split('$')[1]

    # get doge->btc price
    try:
        url = "https://www.coins-e.com/api/v2/markets/data/"
        data = http.get_json(url)
        data = data['markets']
        data = data['DOGE_BTC']
        data = data['marketstat']
        current = {'buy': data['ltp']}

        data = data['24h']
        average = {
            'volume': data['volume'],
            'high': data['h'],
            'avg': data['avg_rate'],
            'low': data['l'],
    }
    except:
        return 'Error: Doge is worthless.'
        
    result = float(bitcoin_price) * float(current['buy'])
    dollar_result = 1 / float(result)

    result = ("Price: \x0307$%s\x0f - $1=\x0307%s\x0f Doge - BTC Price: \x0307%s\x0f" % (result,dollar_result,current['buy']))
    result2 = ("Average: \x0307%(avg)s\x0f - High: \x0307%(high)s\x0f - Low: \x0307%(low)s\x0f - Volume: %(volume)s" % average)
    say("%s - %s" % (result, result2))