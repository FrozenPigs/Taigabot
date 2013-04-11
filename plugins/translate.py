from util import hook, http
import re
import urllib2

def google_translate(to_translate, to_language="auto", from_language="auto"):
    '''Return the translation using google translate
    you must shortcut the langage you define (French = fr, English = en, Spanish = es, etc...)
    if you don't define anything it will detect it or use english by default
    Example:
    print(translate("salut tu vas bien?", "en"))
    hello you alright?'''
    agents = {'User-Agent':"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"}
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s&ie=UTF-8&oe=UTF-8" % (to_language, from_language, to_translate)

    request = urllib2.Request(link, headers=agents)
    page = urllib2.urlopen(request).read().decode('utf-8')
    result = page[page.find(before_trans)+len(before_trans):]
    result = result.split("<")[0]
    return '[%s to %s]: %s' %  (from_language, to_language, result)
	
@hook.command(autohelp=False)
def translate(inp, chan=None, notice=None):
    "translate [from lang] [to lang] <text> -- Lists bot's admins."
    langs = {'auto': '',
             'afrikaans': 'af',
             'albanian': 'sq',
             'amharic': 'am',
             'arabic': 'ar',
             'armenian': 'hy',
             'azerbaijani': 'az',
             'basque': 'eu',
             'belarusian': 'be',
             'bengali': 'bn',
             'bihari': 'bh',
             'bulgarian': 'bg',
             'burmese': 'my',
             'catalan': 'ca',
             'cherokee': 'chr',
             'chinese': 'zh',
             'chinese_simplified': 'zh-CN',
             'chinese_traditional': 'zh-TW',
             'croatian': 'hr',
             'czech': 'cs',
             'danish': 'da',
             'dhivehi': 'dv',
             'dutch': 'nl',
             'english': 'en',
             'esperanto': 'eo',
             'estonian': 'et',
             'filipino': 'tl',
             'finnish': 'fi',
             'french': 'fr',
             'galician': 'gl',
             'georgian': 'ka',
             'german': 'de',
             'greek': 'el',
             'guarani': 'gn',
             'gujarati': 'gu',
             'hebrew': 'iw',
             'hindi': 'hi',
             'hungarian': 'hu',
             'icelandic': 'is',
             'indonesian': 'id',
             'inuktitut': 'iu',
             'irish': 'ga',
             'italian': 'it',
             'japanese': 'ja',
             'kannada': 'kn',
             'kazakh': 'kk',
             'khmer': 'km',
             'korean': 'ko',
             'kurdish': 'ku',
             'kyrgyz': 'ky',
             'laothian': 'lo',
             'latvian': 'lv',
             'lithuanian': 'lt',
             'macedonian': 'mk',
             'malay': 'ms',
             'malayalam': 'ml',
             'maltese': 'mt',
             'marathi': 'mr',
             'mongolian': 'mn',
             'nepali': 'ne',
             'norwegian': 'no',
             'oriya': 'or',
             'pashto': 'ps',
             'persian': 'fa',
             'polish': 'pl',
             'portuguese': 'pt-PT',
             'punjabi': 'pa',
             'romanian': 'ro',
             'russian': 'ru',
             'sanskrit': 'sa',
             'serbian': 'sr',
             'sindhi': 'sd',
             'sinhalese': 'si',
             'slovak': 'sk',
             'slovenian': 'sl',
             'spanish': 'es',
             'swahili': 'sw',
             'swedish': 'sv',
             'tagalog': 'tl',
             'tajik': 'tg',
             'tamil': 'ta',
             'telugu': 'te',
             'thai': 'th',
             'tibetan': 'bo',
             'turkish': 'tr',
             'uighur': 'ug',
             'ukrainian': 'uk',
             'urdu': 'ur',
             'uzbek': 'uz',
             'vietnamese': 'vi',
             'welsh': 'cy',
             'yiddish': 'yi'}

    inp = inp.lower()
    if 'from ' in inp and 'to ' in inp: 
        from_language = inp.split()[1]
        to_language = inp.split()[3]
        to_translate = inp.split(to_language)[1].strip()
        to_language = langs[to_language]
        from_language = langs[from_language]
    elif 'from ' in inp: 
        from_language = inp.split()[1]
        to_language = "auto"
        to_translate = inp.split(from_language)[1].strip()
        from_language = langs[from_language]
    elif 'to ' in inp: 
        from_language = "auto"
        to_language = inp.split()[1]
        to_translate = inp.split(to_language)[1].strip()
        to_language = langs[to_language]
    else:
        from_language = "auto"
        to_language = "auto"
        to_translate = inp

    to_translate = to_translate.replace(" ", "+").encode('utf-8')
    return google_translate(to_translate, to_language, from_language)

