from util import hook
from utilities import request
import re

kataLetters = range(0x30A0, 0x30FF)
hiraLetters = range(0x3040, 0x309F)
kataPunctuation = range(0x31F0, 0x31FF)
all_letters = kataLetters + kataPunctuation + hiraLetters
japanese_characters = ''.join([unichr(aLetter) for aLetter in all_letters])
japanese_characters = (r'.*(([' + japanese_characters + '])).*', re.UNICODE)


# how to update this mess:
# go to https://translate.google.com/m?sl=auto&tl=auto&mui=tl&hl=en
# and run this shady code in ur browser console:
#     copy(Array.prototype.map.call(document.querySelector('div.small').querySelectorAll('a'), e => ' '.repeat(8)+'\'' + e.textContent.trim().toLowerCase().replace(/[\(\)]/g, '').replace(/\s+/g, '_') + '\': \'' + e.href.split('&tl=')[1].split('&')[0] + '\'').join(',\n'))
# it'll fill your clipboard with stuff, paste it inside the { }
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
    'zulu': 'zu',
}


def google_translate(to_translate, to_language="auto", from_language="auto"):
    url = 'https://translate.google.com/m?'
    url = url + "hl=" + to_language
    url = url + "&sl=" + from_language
    url = url + "&tl=" + to_language
    url = url + "&ie=UTF-8&oe=UTF-8"
    url = url + "&q=" + request.urlencode(to_translate)

    page = request.get_text(url)
    # this will break super badly if google changes their html
    before_trans = 'class="result-container">'
    result = page[page.find(before_trans) + len(before_trans) :]
    result = result.split("<")[0]
    return '%s' % (result)


@hook.command
def translate(inp):
    "translate [from language] [to language] <text> -- Run text through google translate, translate to english by default"

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

    label = '%s to %s' % (from_language, to_language)

    if from_language == 'auto' and to_language == 'auto':
        label = 'translate'

    result = google_translate(to_translate, to_language, from_language)
    return '[%s] %s' % (label, result)
