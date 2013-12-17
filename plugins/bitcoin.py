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


import re
@hook.command(autohelp=False)
def doge(inp):
    ".doge -- Returns the value of a dogecoin."
    data = http.get_json("http://data.mtgox.com/api/2/BTCUSD/money/ticker")
    data = data['data']
    ticker = {
        'buy': data['buy']['display_short']
    }
    bitcoin_price = ("%(buy)s" % ticker).split('$')[1]

    try:
        url = "https://coinedup.com/OrderBook?market=DOGE&base=BTC"
        html = http.get_html(url)
        div_dogerate = html.xpath("//div[@id='elementDisplayLastPrice']/div/text()")[0]
        dogerate = http.unquote(re.search('.*last: (.*)\D', div_dogerate).group(1))
    except:
        return 'Error: Doge is worthless.'
        
    result = float(bitcoin_price) * float(dogerate)
    dollar_result = 1 / float(result)

    return ("Current Value: \x0307%s\x0f - 1 Doge=\x0307%s\x0f BTC - $1=\x0307%s\x0f Doges" % (result,dogerate,dollar_result))