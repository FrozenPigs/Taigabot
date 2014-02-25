from util import http, hook
#import lxml
#from lxml.html import parse 

## CONSTANTS

exchanges = {
    "blockchain": {
        "api_url": "https://blockchain.info/ticker",
        "func": lambda data: u"[Blockchain] Buy: \x0307${:,.2f}\x0f - Sell: \x0307${:,.2f}\x0f".format(data["USD"]["buy"], \
                               data["USD"]["sell"])
    },
    "mtgox": {
        "api_url": "https://mtgox.com/api/1/BTCUSD/ticker",
        "func": lambda data: u"[MtGox] Current: \x0307{}\x0f - High: \x0307{}\x0f - Low: \x0307{}\x0f - Best Ask: \x0307{}\x0f - Volume: {}".format(data['return']['last']['display'], \
                               data['return']['high']['display'], data['return']['low']['display'], data['return']['buy']['display'], \
                               data['return']['vol']['display'])
    },
    "coinbase":{
        "api_url": "https://coinbase.com/api/v1/prices/spot_rate",
        "func": lambda data: u"[Coinbase] Current: \x0307${:,.2f}\x0f".format(float(data['amount']))
    },
    "bitpay": {
        "api_url": "https://bitpay.com/api/rates",
        "func": lambda data: u"[Bitpay] Current: \x0307${:,.2f}\x0f".format(data[0]['rate'])
    },
    "bitstamp": {
        "api_url": "https://www.bitstamp.net/api/ticker/",
        "func": lambda data: u"[BitStamp] Current: \x0307${:,.2f}\x0f - High: \x0307${:,.2f}\x0f - Low: \x0307${:,.2f}\x0f - Volume: {:,.2f} BTC".format(float(data['last']), float(data['high']), float(data['low']), \
                               float(data['volume']))
    }
}


## HOOK FUNCTIONS

@hook.command("btc", autohelp=False)
@hook.command(autohelp=False)
def bitcoin(inp):
    """bitcoin <exchange | list> -- Gets current exchange rate for bitcoins from several exchanges, default is MtGox. Supports MtGox, Blockchain, Bitpay, Coinbase and BitStamp."""
    
    inp = inp.lower()

    if inp:
        if inp in exchanges:
            exchange = exchanges[inp]
        else:
            return "Available exchanges: {}".format(", ".join(exchanges.keys()))
    else:
        exchange = exchanges["mtgox"]

    data = http.get_json(exchange["api_url"])
    func = exchange["func"]
    return func(data)

    # try:
    #     data = http.get_json("http://data.mtgox.com/api/1/generic/order/lag")
    #     data = data['return']
    #     lag = {
    #         'lag': data['lag_text']
    #     }
    #     result_lag = ("Lag: %(lag)s" % lag)
    #     result = "{} {}".format(result,result_lag)
    # except:
    #     result = result



@hook.command("ltc", autohelp=False)
@hook.command(autohelp=False)
def litecoin(inp, message=None):
    """litecoin -- gets current exchange rate for litecoins from BTC-E"""
    data = http.get_json("https://btc-e.com/api/2/ltc_usd/ticker")
    ticker = data['ticker']
    message("Current: \x0307${:,.2f}\x0f - High: \x0307${:,.2f}\x0f"
        " - Low: \x0307${:,.2f}\x0f - Volume: {:,.2f} LTC".format(ticker['buy'], ticker['high'], ticker['low'], ticker['vol_cur']))



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
    lotsadoge = 10000 * result

    result = ("Price: \x0307$%s\x0f - $1=\x0307%s\x0f Doge - 10,000 DOGE=\x0307$%s\x0f - BTC: \x0307%s\x0f" % (result,dollar_result,lotsadoge,current['buy']))
    result2 = ("Average: \x0307%(avg)s\x0f - High: \x0307%(high)s\x0f - Low: \x0307%(low)s\x0f" % average)
    say("%s - %s" % (result, result2))