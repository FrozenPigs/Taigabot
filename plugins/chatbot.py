import urllib
import urllib2
import xml.dom.minidom
import re
import socket
from util import hook

chatbot_re = (r'(^.*\b(taiga|taigabot)\b.*$)', re.I)
@hook.regex(*chatbot_re)
@hook.command
def chatbot(inp, reply=None, nick=None, conn=None):
    inp = inp.group(1).lower().replace('taigabot', '').replace('taiga', '').replace(':', '')
    args = {'bot_id': '6', 'say': inp.strip(), 'convo_id': conn.nick, 'format': 'xml'}
    data = urllib.urlencode(args)
    resp = False
    url_response = urllib2.urlopen('http://api.program-o.com/v2/chatbot/?', data)
    response = url_response.read()
    response_dom = xml.dom.minidom.parseString(response)
    text = response_dom.getElementsByTagName('response')[0].childNodes[0].data.strip()
    return nick + ': ' + str(text.lower().replace('programo', 'taiga').replace('program-o', 'taigabot').replace('elizabeth', 'wednesday'))
