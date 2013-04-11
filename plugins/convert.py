from util import hook, http, urlnorm
import urllib, urllib2
import re
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.215 Safari/535.1"};

@hook.command
def convert(inp):
    "title <url> -- gets the title of a web page"

    conv_left = None
    conv_right = None
    result = None
    url = "http://www.google.com/search?q=convert+%s&num=100&hl=en&start=0" % (urllib.quote_plus(inp))
    request = urllib2.Request(url, None, headers)
    page = urllib2.urlopen(request).read()
    soup = BeautifulSoup(page)
    #soup = soup.find('div', attrs={'id': re.compile('ires')})
    is_currency = soup.find('li', attrs={'class': re.compile('currency')})
    if is_currency:
      conv_left = soup.find('input', id='pair_base_input')
      conv_right = soup.find('input', id='pair_targ_input')
      if not (conv_left is None or conv_right is None):
        left_value = conv_left['value'].strip()
        left_unit = conv_left.findNext('option').renderContents().strip()
        right_value = conv_right['value'].strip()
        right_unit = conv_right.findNext('option').renderContents().strip()
    else:
      conv_left = soup.find('input', id='ucw_lhs_d')
      conv_right = soup.find('input', id='ucw_rhs_d')
      if not (conv_left is None or conv_right is None):
        left_value = conv_left['value'].strip()
        left_unit = conv_left.findNext('option').renderContents().strip()
        right_value = conv_right['value'].strip()
        right_unit = conv_right.findNext('option').renderContents().strip()

    try:
      result = left_value + " " + left_unit + "s = " + right_value + " " + right_unit + "s"
    except StandardError:
      pass

    if result:
        return result
