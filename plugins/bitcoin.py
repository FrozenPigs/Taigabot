from util import http, hook
#import lxml
import urllib, urllib2
from bs4 import BeautifulSoup
#from lxml.html import parse 

@hook.command('bitcoin',autohelp=False)
@hook.command('buttcoin',autohelp=False)
@hook.command(autohelp=False)
def bc(inp, say=None):
    "bitcoin -- gets current exchange rate for bitcoins from mtgox"
    data = http.get_json("https://data.mtgox.com/api/2/BTCUSD/money/ticker")
    data = data['data']
    ticker = {
        'buy': data['buy']['display_short'],
        'high': data['high']['display_short'],
        'low': data['low']['display_short'],
        'vol': data['vol']['display_short'],
    }

    data = http.get_json("https://data.mtgox.com/api/1/generic/order/lag")
    data = data['return']
    lag = {
        'lag': data['lag_text']
    }

    result = ("Current: \x0307%(buy)s\x0f - High: \x0307%(high)s\x0f"
        " - Low: \x0307%(low)s\x0f - Volume: %(vol)s" % ticker)
    result_lag = ("Lag: %(lag)s" % lag)

    say("%s - %s" % (result, result_lag))