import re

from util import hook, http, text, web
import random

# @hook.command('math')
# @hook.command('calc')
# @hook.command('wa')
# @hook.command
# def wolframalpha(inp, bot=None):
#     """wa <query> -- Computes <query> using Wolfram Alpha."""

#     api_key = bot.config.get("api_keys", {}).get("wolframalpha", None)

#     if not api_key:
#         return "error: missing api key"

#     url = 'http://api.wolframalpha.com/v2/query?format=plaintext'

#     result = http.get_xml(url, input=inp, appid=api_key)

#     # get the URL for a user to view this query in a browser
#     query_url = "http://www.wolframalpha.com/input/?i=" + \
#                 http.quote_plus(inp.encode('utf-8'))
#     short_url = web.try_isgd(query_url)

#     pod_texts = []
#     for pod in result.xpath("//pod[@primary='true']"):
#         title = pod.attrib['title']
#         if pod.attrib['id'] == 'Input':
#             continue

#         results = []
#         for subpod in pod.xpath('subpod/plaintext/text()'):
#             subpod = subpod.strip().replace('\\n', '; ')
#             subpod = re.sub(r'\s+', ' ', subpod)
#             if subpod:
#                 results.append(subpod)
#         if results:
#             pod_texts.append(title + u': ' + u', '.join(results))

#     ret = u' - '.join(pod_texts)

#     if not pod_texts:
#         return 'No results.'

#     ret = re.sub(r'\\(.)', r'\1', ret)

#     def unicode_sub(match):
#         return unichr(int(match.group(1), 16))

#     ret = re.sub(r'\\:([0-9a-z]{4})', unicode_sub, ret)

#     ret = text.truncate_str(ret, 250)

#     if not ret:
#         return 'No results.'

#     return u"{} - {}".format(ret, short_url)


#!/usr/bin/python
#
# Copyright 2009 Derik Pereira. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''A library that provides a python interface to the Wolfram|Alpha API'''

__author__ = 'derik66@gmail.com'
__version__ = '1.1-devel'

import urllib2
from xml.dom import minidom
import simplejson as json

class WolframAlphaEngine:

  def __init__(self, appid='', server=''):
    self.appid = appid
    self.server = server
    self.ScanTimeout = ''
    self.PodTimeout = ''
    self.FormatTimeout = ''
    self.Async = ''

  def CreateQuery(self, query=''):
    waeq = WolframAlphaQuery(query)
    waeq.appid = self.appid
    waeq.ScanTimeout = self.ScanTimeout
    waeq.PodTimeout = self.PodTimeout
    waeq.FormatTimeout = self.FormatTimeout
    waeq.Async = self.Async
    waeq.ToURL()
    return waeq.Query

  def PerformQuery(self, query=''):

    try:
      result = urllib2.urlopen(self.server, query)
      result = result.read()
    except:
      result = '<error>urllib2.urlopen ' + self.server + ' ' + query + '</error>'
    return result

class WolframAlphaQuery:

  def __init__(self, query='', appid=''):
    self.Query = query
    self.appid = appid
    self.ScanTimeout = ''
    self.PodTimeout = ''
    self.FormatTimeout = ''
    self.Async = ''
 
  def ToURL(self):
    self.Query = 'input=' + self.Query
    self.Query = self.Query + '&appid=' + self.appid
    if self.ScanTimeout:
      self.Query = self.Query + '&scantimeout=' + self.ScanTimeout
    if self.PodTimeout:
      self.Query = self.Query + '&podtimeout=' + self.PodTimeout
    if self.FormatTimeout:
      self.Query = self.Query + '&formattimeout=' + self.FormatTimeout
    if self.Async:
      self.Query = self.Query + '&async=' + self.Async
    return

  def AddPodTitle(self, podtitle=''):
    self.Query = self.Query + '&podtitle=' + podtitle        
    return

  def AddPodIndex(self, podindex=''):
    self.Query = self.Query + '&podindex=' + podindex
    return

  def AddPodScanner(self, podscanner=''):
    self.Query = self.Query + '&podscanner=' + podscanner
    return

  def AddPodState(self, podstate=''):
    self.Query = self.Query + '&podstate=' + podstate
    return

  def AddAssumption(self, assumption=''):
    self.Query = self.Query + '&assumption=' + assumption
    return

class WolframAlphaQueryResult:

  def __init__(self, result=''):
    self.XmlResult = result
    self.dom = minidom.parseString(result)
    self.tree = runtree(self.dom.documentElement)

  def JsonResult(self):
    return json.dumps(self.tree)

  def IsSuccess(self):
    return scanbranches(self.tree, 'success')

  def IsError(self):
    try:
      return [scanbranches(self.tree, 'error')[0]]
    except:
      return scanbranches(self.tree, 'error')

  def NumPods(self):
    return scanbranches(self.tree, 'numpods')

  def DataTypes(self):
    return scanbranches(self.tree, 'datatypes')

  def TimedoutScanners(self):
    return scanbranches(self.tree, 'timedout')

  def Timing(self):
    return scanbranches(self.tree, 'timing')

  def ParseTiming(self):
    return scanbranches(self.tree, 'parsetiming')

  def Error(self):
    try:
      return scanbranches(self.tree, 'error')[1]
    except:
      return []

  def ErrorCode(self):
    try:
      return [scanbranches(self.Error(), 'code')[0]]
    except:
      return []

  def ErrorMessage(self):
    try:
      return [scanbranches(self.Error(), 'msg')[0]]
    except:
      return []

  def Pods(self):
    return scanbranches(self.tree, 'pod')

  def XMLPods(self):
    return asxml(self.dom, 'pod')

  def Assumptions(self):
    assumptions = scanbranches(self.tree, 'assumptions')
    try:
      return scanbranches(assumptions[0], 'assumption')
    except:
      return []

  def Warnings(self):
    return scanbranches(self.tree, 'warnings')

  def Sources(self):
    return scanbranches(self.tree, 'sources')

class Pod:

  def __init__(self, pod=''):
    self.pod = pod
    return

  def IsError(self):
    return scanbranches(self.pod, 'error')

  def NumSubpods(self):
    return scanbranches(self.pod, 'numsubpods')

  def Title(self):
    return scanbranches(self.pod, 'title')

  def Scanner(self):
    return scanbranches(self.pod, 'scanner')

  def Position(self):
    return scanbranches(self.pod, 'position')

  def AsynchURL(self):
    return scanbranches(self.pod, 'asynchurl')

  def Subpods(self):
    return scanbranches(self.pod, 'subpod')

  def PodStates(self):
    return scanbranches(self.pod, 'states')

  def Infos(self):
    return scanbranches(self.pod, 'infos')

  def AsXML(self):
    return self.pod

class Subpod:

  def __init__(self, subpod=''):
    self.subpod = subpod
    return

  def Title(self):
    return scanbranches(self.subpod, 'title')

  def Plaintext(self):
    return scanbranches(self.subpod, 'plaintext')

  def Img(self):
    return scanbranches(self.subpod, 'img')

class Assumption:

  def __init__(self, assumption=''):
    self.assumption = assumption
    return

  def Type(self):
    return scanbranches(self.assumption, 'type')

  def Word(self):
    return scanbranches(self.assumption, 'word')

  def Count(self):
    return scanbranches(self.assumption, 'count')

  def Value(self):
    return scanbranches(self.assumption, 'value')

def runtree(node):
  tree = []
  if node.nodeType != node.TEXT_NODE:
    tree = [node.nodeName]
    for index in range(node.attributes.length):
      attr = node.attributes.item(index)
      tree = tree + [(attr.nodeName, attr.nodeValue)]
  for child in node.childNodes:
    if child.nodeType != child.TEXT_NODE:
      tree = tree + [runtree(child)]
    else:
      if child.data[0] != '\n':
        tree = child.parentNode.nodeName, child.data
  return tree

def scanbranches(tree, name):
  branches = []
  for branch in tree:
    if branch[0] == name:
      if type(branch) == type(('', '')):
        branches = branches + [branch[1]]
      else:
        branches = branches + [branch[1:]]
  return branches

def asxml(dom, name):
    xml = []
    for child in dom.documentElement.childNodes:
      if child.nodeName == name:
        xml = xml + [child.toxml()]
    return xml

errors = ([
    ('I dont know.'),
    ('Try again later.'),
    ('Youre annoying.'),
    ('Are you serious?')
])

@hook.command('math')
@hook.command('calc')
@hook.command('convert')
@hook.command('wa')
@hook.command
def wolframalpha(inp, bot=None):
    """wa <query> -- Computes <query> using Wolfram Alpha."""
    server = 'http://api.wolframalpha.com/v2/query.jsp'
    api_key = bot.config.get("api_keys", {}).get("wolframalpha", None)

    if not api_key:
        return "error: missing api key"

    import time
    start = time.clock()

    scantimeout = '3.0'
    podtimeout = '4.0'
    formattimeout = '8.0'
    async = 'True'

    waeo = WolframAlphaEngine(api_key, server)

    waeo.ScanTimeout = scantimeout
    waeo.PodTimeout = podtimeout
    waeo.FormatTimeout = formattimeout
    waeo.Async = async

    query = waeo.CreateQuery(inp)
    result = waeo.PerformQuery(query)
    waeqr = WolframAlphaQueryResult(result)
    # xmlresult = waeqr.XmlResult
    # print '\n', type(xmlresult), 'xml=', xmlresult
    results = []
    pods = waeqr.Pods()
    for pod in pods:
        waep = Pod(pod)
        subpods = waep.Subpods()
        for subpod in subpods:
            waesp = Subpod(subpod)
            plaintext = waesp.Plaintext()
            results.append(plaintext)

    # return u'\x02[{}]\x02 {}'.format(results[0][0],results[1][0])
    try:
        return u'{}'.format(results[1][0].replace('Wolfram|Alpha','Uguu~~'))
    except: 
        return errors[random.randint(0, len(errors) - 1)]
    
# question_re = (r'(?:uguu|uguubot)\s(.+)', re.I)
# @hook.regex(*question_re)
# def wolframalpha_re(inp, bot=None):
#     return wolframalpha(inp.group(1),bot)