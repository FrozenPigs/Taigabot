from util import hook, http
import re
import urllib2

kataLetters = range(0x30A0, 0x30FF)
hiraLetters = range(0x3040, 0x309F)
kataPunctuation = range(0x31F0, 0x31FF)
all_letters = kataLetters + kataPunctuation + hiraLetters
japanese_characters = ''.join([unichr(aLetter) for aLetter in all_letters])
japanese_characters = (r'.*(([' + japanese_characters + '])).*', re.UNICODE)


def google_translate(to_translate, to_language="auto", from_language="auto"):
    header = {
        'User-Agent':
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)"
    }
    before_trans = 'class="t0">'
    link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s&ie=UTF-8&oe=UTF-8" % (
        to_language, from_language, urllib2.quote(
            to_translate.encode('utf-8')))
    request = urllib2.Request(link, headers=header)
    page = urllib2.urlopen(request).read().decode('utf-8')
    result = page[page.find(before_trans) + len(before_trans):]
    result = result.split("<")[0]
    return '%s' % (result)


@hook.command
def translate(inp, chan=None, notice=None):
    "translate [from language] [to language] <text> -- Will usually autotranslate from other languages to english."

    # how to update this list:
    # go to https://translate.google.com/m?sl=auto&tl=auto&mui=tl&hl=en
    # and run this shady ass code in ur browser console:
    # copy(Array.prototype.map.call(document.querySelector('div.small').querySelectorAll('a'), e => ' '.repeat(8)+'\'' + e.textContent.trim().toLowerCase().replace(/[\(\)]/g, '').replace(/\s+/g, '_') + '\': \'' + e.href.split('&tl=')[1].split('&')[0] + '\'').join(',\n'))
    langs = {
        'afrikaans': 'af',
        'albanian': 'sq',
        'amharic': 'am',
        'arabic': 'ar',
        'armenian': 'hy',
        'azerbaijani': 'az',
        'basque': 'eu',
        'belarusian': 'be',
        'bengali': 'bn',
        'bosnian': 'bs',
        'bulgarian': 'bg',
        'catalan': 'ca',
        'cebuano': 'ceb',
        'chichewa': 'ny',
        'chinese_simplified': 'zh-CN',
        'chinese_traditional': 'zh-TW',
        'corsican': 'co',
        'croatian': 'hr',
        'czech': 'cs',
        'danish': 'da',
        'dutch': 'nl',
        'english': 'en',
        'esperanto': 'eo',
        'estonian': 'et',
        'filipino': 'tl',
        'finnish': 'fi',
        'french': 'fr',
        'frisian': 'fy',
        'galician': 'gl',
        'georgian': 'ka',
        'german': 'de',
        'greek': 'el',
        'gujarati': 'gu',
        'haitian_creole': 'ht',
        'hausa': 'ha',
        'hawaiian': 'haw',
        'hebrew': 'iw',
        'hindi': 'hi',
        'hmong': 'hmn',
        'hungarian': 'hu',
        'icelandic': 'is',
        'igbo': 'ig',
        'indonesian': 'id',
        'irish': 'ga',
        'italian': 'it',
        'japanese': 'ja',
        'javanese': 'jw',
        'kannada': 'kn',
        'kazakh': 'kk',
        'khmer': 'km',
        'kinyarwanda': 'rw',
        'korean': 'ko',
        'kurdish_kurmanji': 'ku',
        'kyrgyz': 'ky',
        'lao': 'lo',
        'latin': 'la',
        'latvian': 'lv',
        'lithuanian': 'lt',
        'luxembourgish': 'lb',
        'macedonian': 'mk',
        'malagasy': 'mg',
        'malay': 'ms',
        'malayalam': 'ml',
        'maltese': 'mt',
        'maori': 'mi',
        'marathi': 'mr',
        'mongolian': 'mn',
        'myanmar_burmese': 'my',
        'nepali': 'ne',
        'norwegian': 'no',
        'oriya': 'or',
        'pashto': 'ps',
        'persian': 'fa',
        'polish': 'pl',
        'portuguese': 'pt',
        'punjabi': 'pa',
        'romanian': 'ro',
        'russian': 'ru',
        'samoan': 'sm',
        'scots_gaelic': 'gd',
        'serbian': 'sr',
        'sesotho': 'st',
        'shona': 'sn',
        'sindhi': 'sd',
        'sinhala': 'si',
        'slovak': 'sk',
        'slovenian': 'sl',
        'somali': 'so',
        'spanish': 'es',
        'sundanese': 'su',
        'swahili': 'sw',
        'swedish': 'sv',
        'tajik': 'tg',
        'tamil': 'ta',
        'tatar': 'tt',
        'telugu': 'te',
        'thai': 'th',
        'turkish': 'tr',
        'turkmen': 'tk',
        'uighur': 'ug',
        'ukrainian': 'uk',
        'urdu': 'ur',
        'uzbek': 'uz',
        'vietnamese': 'vi',
        'welsh': 'cy',
        'xhosa': 'xh',
        'yiddish': 'yi',
        'yoruba': 'yo',
        'zulu': 'zu'
    }

    inp = inp.lower()
    if inp.startswith('from') and inp.split()[2] == 'to':
        from_language = inp.split()[1]
        to_language = inp.split()[3]
        to_translate = inp.split(to_language)[1].strip()
        if to_language in langs.keys():
            to_language = langs[to_language]
            from_language = langs[from_language]
    elif inp.startswith('from'):
        from_language = inp.split()[1]
        to_language = "auto"
        to_translate = inp.split(from_language)[1].strip()
        from_language = langs[from_language]
    elif inp.startswith('to'):
        from_language = "auto"
        to_language = inp.split()[1]
        to_translate = inp.split(to_language)[1].strip()
        to_language = langs[to_language]
    else:
        from_language = "auto"
        to_language = "auto"
        to_translate = inp

    to_translate = to_translate
    result = google_translate(to_translate, to_language, from_language)
    return '[%s to %s]: %s' % (from_language, to_language,
                               http.decode_html(result))


#@hook.regex(*(japanese_characters))
#def autotranslate(inp, bot=None, chan=None):
#    "Automatically translates any japanese text detected."

#    try:
#        if 'autotrans' in database.get(db, 'channels', 'disabled', 'chan',
#                                       chan):
#            return None
#    except:
#        pass

#    if 'translate' in inp.group(0): return None
#    if ']:' in inp.group(0).strip(): return None

#    result = translate(inp.group(0))
#    if result.split(':')[1].strip() in inp.group(0).strip(): return None

#    return '[%s]: %s' % (inp.group(0), result.split(':')[1].strip())
