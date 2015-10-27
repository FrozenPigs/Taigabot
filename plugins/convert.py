from util import hook, http, urlnorm
import urllib, urllib2
import re
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.215 Safari/535.1"};

@hook.command
def convert(inp,conn=None,chan=None):
    "gconvert <val1> <val2> -- converts a measurement or currency"\
    "gconvert 1000 usd to yen"\
    "gconvert 100 miles to km"

    if 'btc' in inp.lower() or 'bitcoin' in inp.lower():
        convert_btc(inp,conn,chan)
        return None
    elif 'ltc' in inp.lower() or 'litecoin' in inp.lower():
        convert_ltc(inp,conn,chan)
        return None
    
    url = "http://www.google.com/search?q=convert+{}".format(urllib.quote_plus(inp))

    request = urllib2.Request(url, None, headers)
    page = urllib2.urlopen(request).read()
    soup = BeautifulSoup(page,'lxml')


    soup = soup.find('div', attrs={'id': re.compile('ires')})
    is_currency = soup.find('li', attrs={'class': re.compile('currency')})
    if is_currency:
        conv_inp = http.strip_html(soup.find('div', attrs={'class': re.compile('vk_sh')}).renderContents().strip())
        conv_out = http.strip_html(soup.find('div', attrs={'class': re.compile('vk_ans')}).renderContents().strip())
        return "{} {}".format(conv_inp.replace("equals","="),conv_out)
    else:
        conv_inp = soup.find('div', attrs={'id': re.compile('_Aif')})
        inp_value = conv_inp.find('input', attrs={'class': re.compile('_eif')})['value'].strip()
        inp_unit = http.strip_html(conv_inp.find('select', attrs={'class': re.compile('_dif')}).find_all('option', selected=True)[0])

        conv_out = soup.find('div', attrs={'id': re.compile('_Cif')})
        out_value = conv_out.find('input', attrs={'class': re.compile('_eif')})['value'].strip()
        out_unit = http.strip_html(conv_out.find('select', attrs={'class': re.compile('_dif')}).find_all('option', selected=True)[0])


    return "{} {}s = {} {}s".format(inp_value, inp_unit, out_value, out_unit)

def convert_btc(inp,conn=None,chan=None):
    inp = inp.lower().replace(',','').split()
    inp_amount = inp[0]
    amount = inp_amount
    #get btc price
    data = http.get_json("http://data.mtgox.com/api/2/BTCUSD/money/ticker")
    data = data['data']
    ticker = { 'buy': data['buy']['display_short'] }
    btc_price = ("%(buy)s" % ticker).replace('$','')

    if 'btc' in inp[3]:
        currency = inp[1]
        if not 'usd' in currency: amount = convert('%s %s to usd' % (amount,currency)).split('=')[1].split()[0]
        result = (float(amount) / float(btc_price))
    elif 'btc' in inp[1]:
        currency = inp[3]
        if not 'usd' in currency: 
            conversion_rate = (float(convert('10000 usd to %s' % currency).split('=')[1].split()[0]) / 10000)
            result = ((float(conversion_rate) * float(btc_price)) * float(amount))
        else: result = (float(amount) * float(btc_price))

    #result = "%.2f" % result
    message = '%s %s = %s %s' % ('{:20,.2f}'.format(float(amount)).strip(),inp[1],'{:20,.2f}'.format(float(result)).strip(),inp[3])
    out = "PRIVMSG %s :%s" % (chan, message)
    conn.send(out)

def convert_ltc(inp,conn=None,chan=None):
    inp = inp.lower().replace(',','').split()
    inp_amount = inp[0]
    amount = inp_amount
    #get ltc price
    data = http.get_json("https://btc-e.com/api/2/ltc_usd/ticker")
    data = data['ticker']
    ticker = {'buy': data['buy']}

    ltc_price = ("%(buy)s" % ticker).replace('$','')

    if 'ltc' in inp[3]:
        currency = inp[1]
        if not 'usd' in currency: amount = convert('%s %s to usd' % (amount,currency)).split('=')[1].split()[0]
        result = (float(amount) / float(ltc_price))
    elif 'ltc' in inp[1]:
        currency = inp[3]
        if not 'usd' in currency: 
            conversion_rate = (float(convert('10000 usd to %s' % currency).split('=')[1].split()[0]) / 10000)
            result = ((float(conversion_rate) * float(ltc_price)) * float(amount))
        else: result = (float(amount) * float(ltc_price))

    #result = "%.2f" % result
    message = '%s %s = %s %s' % ('{:20,.2f}'.format(float(amount)).strip(),inp[1],'{:20,.2f}'.format(float(result)).strip(),inp[3])
    out = "PRIVMSG %s :%s" % (chan, message)
    conn.send(out)