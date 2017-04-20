from util import hook, http
import re
import urllib2

kataLetters = range(0x30A0, 0x30FF)
hiraLetters = range(0x3040, 0x309F)
kataPunctuation = range(0x31F0,0x31FF)
all_letters = kataLetters+kataPunctuation+hiraLetters
japanese_characters = ''.join([unichr(aLetter) for aLetter in all_letters])
japanese_characters = (r'.*((['+japanese_characters+'])).*', re.UNICODE)	


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
    return '%s' % (result)


@hook.command
def translate(inp, chan=None, notice=None):
    "translate [from language] [to language] <text> -- Will usually autotranslate from other languages to english."

    langs = {'auto': '',
             'afrikaans': 'af',
             'albanian': 'sq',
             'amharic': 'am',
             'arabic': 'ar',
             'armenian': 'hy',
             'azerbaijani': 'az',
             'basque': 'e',
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
             'gujarati': 'g',
             'hebrew': 'iw',
             'hindi': 'hi',
             'hungarian': 'h',
             'icelandic': 'is',
             'indonesian': 'id',
             'inuktitut': 'i',
             'irish': 'ga',
             'italian': 'it',
             'japanese': 'ja',
             'kannada': 'kn',
             'kazakh': 'kk',
             'khmer': 'km',
             'korean': 'ko',
             'kurdish': 'k',
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
             'russian': 'r',
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
             'telug': 'te',
             'thai': 'th',
             'tibetan': 'bo',
             'turkish': 'tr',
             'uighur': 'ug',
             'ukrainian': 'uk',
             'urd': 'ur',
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
    result = google_translate(to_translate, to_language, from_language)
    return '[%s to %s]: %s' %  (from_language, to_language, http.decode_html(result))


@hook.regex(*(japanese_characters)) 
def autotranslate(inp,bot=None,chan=None):
    "Automatically translates any japanese text detected."

    try: 
        if 'autotrans' in database.get(db,'channels','disabled','chan',chan): return None
    except: 
        pass

    if 'translate' in inp.group(0): return None
    if ']:' in inp.group(0).strip(): return None

    result = translate(inp.group(0))
    if result.split(':')[1].strip() in inp.group(0).strip(): return None

    return '[%s]: %s' % (inp.group(0), result.split(':')[1].strip())


### This uses the mygengo_translate plugin located in the disabled_plugins folder. It is sometimes more accurate than google translate
# @hook.command
# def gwapanese(inp):
#     "wapanese <text> -- Translate english text into japanese romanji"
#     import mygengo_translate
#     print inp.strip()
#     jp_result = unicode(mygengo_translate.gengo_translate(inp.strip(), 'en', 'ja'))
#     
#     jp_result = jp_result.split(')')[1].strip()
#     print jp_result
#     rj_result = romaji(jp_result)
#     return '%s' %  (rj_result)


# @hook.command
# def wapanese(inp): #googletranslate
#     "wapanese <text> -- Translate english text into japanese romanji"
#     jp_result = google_translate(inp.replace(" ", "+").encode('utf-8'), 'ja', 'en')
#     rj_result = romaji(jp_result)
#     return '%s' %  (rj_result)


# @hook.command('romanji')
# @hook.command
# def romaji(inp):
#     "romaji <text> -- Translates japanese text (Kanji,Hiragana,Katakana) into Romaji"
#     agents = {'Content-Type':"application/x-www-form-urlencoded"}
#     before_trans = 'font color="red">'
#     link = "http://romaji.me/romaji.cgi?mode=2&text=%s" % inp.encode('cp932')
#     request = urllib2.Request(link, headers=agents)
#     page = urllib2.urlopen(request).read()
#     result = page[page.find(before_trans):]
#     result = result.split(">")[1].split("<")[0]
#     return '[%s]: %s' %  (inp, result)


hiragana={
#https://gist.github.com/711089
'あ':'a','い':'i','う':'','え':'e','お':'o',
'か':'ka','き':'ki','く':'k','け':'ke','こ':'ko',
'さ':'sa','し':'si','す':'s','せ':'se','そ':'so',
'た':'ta','ち':'chi','つ':'t','て':'te','と':'to',
'な':'na','に':'ni','ぬ':'n','ね':'ne','の':'no',
'は':'ha','ひ':'hi','ふ':'h','へ':'he','ほ':'ho',
'ま':'ma','み':'mi','む':'m','め':'me','も':'mo',
'や':'ya','ゆ':'y','よ':'yo',
'ら':'ra','り':'ri','る':'r','れ':'re','ろ':'ro',
'わ':'wa','を':'wo','ん':'n',

'が':'ga','ぎ':'gi','ぐ':'g','げ':'ge','ご':'go',
'ざ':'za','じ':'zi','ず':'z','ぜ':'ze','ぞ':'zo',
'だ':'da','ぢ':'di','づ':'d','で':'de','ど':'do',
'ば':'ba','び':'bi','ぶ':'b','べ':'be','ぼ':'bo',
'ぱ':'pa','ぴ':'pi','ぷ':'p','ぺ':'pe','ぽ':'po',

'ぁ':'xa','ぃ':'xi','ぅ':'x','ぇ':'xe','ぉ':'xo',
#'ゃ':'ya','ゅ':'y','ょ':'yo',
#'ゎ':'wa',

'ゐ':'wi','ゑ':'we',
'ー':'',

'っ':'sokuon',

'きゃ':'kya','きゅ':'ky','きょ':'kyo',
'しゃ':'sha','しゅ':'sh','しょ':'sho',
'ちゃ':'cha','ちゅ':'ch','ちょ':'cho',
'にゃ':'nya','にゅ':'ny','にょ':'nyo',
'ひゃ':'hya','ひゅ':'hy','ひょ':'hyo',
'みゃ':'mya','みゅ':'my','みょ':'myo',
'りゃ':'rya','りゅ':'ry','りょ':'ryo',
'ぎゃ':'gya','ぎゅ':'gy','ぎょ':'gyo',
'じゃ':'ja','じゅ':'j','じょ':'jo',
'びゃ':'bya','びゅ':'by','びょ':'byo',
'ぴゃ':'pya','ぴゅ':'py','ぴょ':'pyo',
'ゔ':'v'
}

alphanumerics={
'０':'0','１':'1','２':'2','３':'3','４':'4',
'５':'5','６':'6','７':'7','８':'8','９':'9',

'Ａ':'a','Ｂ':'b','Ｃ':'c','Ｄ':'d','Ｅ':'e','Ｆ':'f','Ｇ':'g','Ｈ':'h','Ｉ':'i',
'Ｊ':'j','Ｋ':'k','Ｌ':'l','Ｍ':'m','Ｎ':'n','Ｏ':'o','Ｐ':'p','Ｑ':'q','Ｒ':'r',
'Ｓ':'s','Ｔ':'t','Ｕ':'','Ｖ':'v','Ｗ':'w','Ｘ':'x','Ｙ':'y','Ｚ':'z',

'ａ':'a','ｂ':'b','ｃ':'c','ｄ':'d','ｅ':'e','ｆ':'f','ｇ':'g','ｈ':'h','ｉ':'i',
'ｊ':'j','ｋ':'k','ｌ':'l','ｍ':'m','ｎ':'n','ｏ':'o','ｐ':'p','ｑ':'q','ｒ':'r',
'ｓ':'s','ｔ':'t','ｕ':'','ｖ':'v','ｗ':'w','ｘ':'x','ｙ':'y','ｚ':'z',

'！':'!','＂':'"','＃':'#','＄':'$','％':'%','＆':'&','＇':"'",'（':'(','）':')','＊':'*','＋':'+','，':',','－':'-','．':'.','／':'/'

}
katakana={

'ア':'a','イ':'i','ウ':'','エ':'e','オ':'o','ン':'n',

'カ':'ka','キ':'ki','ク':'k','ケ':'ke','コ':'ko',
'サ':'sa','シ':'si','ス':'s','セ':'se','ソ':'so',
'タ':'ta','チ':'ti','ツ':'t','テ':'te','ト':'to',
'ナ':'na','ニ':'ni','ヌ':'n','ネ':'ne','ノ':'no',
'ハ':'ha','ヒ':'hi','フ':'f','ヘ':'he','ホ':'ho',
'マ':'ma','ミ':'mi','ム':'m','メ':'me','モ':'mo',
'ヤ':'ya','ユ':'y','ヨ':'yo',
'ラ':'ra','リ':'ri','ル':'r','レ':'re','ロ':'ro',
'ワ':'wa','ヲ':'wo',
'ガ':'ga','ギ':'gi','グ':'g','ゲ':'ge','ゴ':'go',
'ザ':'za','ジ':'zi','ズ':'z','ゼ':'ze','ゾ':'zo',
'ダ':'da','ヂ':'di','ヅ':'d','デ':'de','ド':'do',
'バ':'ba','ビ':'bi','ブ':'b','ベ':'be','ボ':'bo',
'パ':'pa','ピ':'pi','プ':'p','ペ':'pe','ポ':'po',
'ジャ':'ja','j':'ジュ','jo':'ジョ','ジ':'ji',
'ヴィ':'vi',

'ァ':'xa','ィ':'xi','ゥ':'x','ェ':'xe','ォ':'xo',

'キャ':'kya','キュ':'ky','キョ':'kyo',
'シャ':'sha','シュ':'sh','ショ':'sho','シ':'shi','ツ':'ts',
'チャ':'cha','チュ':'ch','チョ':'cho','チ':'chi',
'ニャ':'nya','ニュ':'ny','ニョ':'nyo',
'ヒャ':'hya','ヒュ':'hy','ヒョ':'hyo',
'ミャ':'mya','ミュ':'my','ミョ':'myo',
'リャ':'rya','リュ':'ry','リョ':'ryo',
'ギャ':'gya','ギュ':'gy','ギョ':'gyo',
'ビャ':'bya','ビュ':'by','ビョ':'byo',
'ピャ':'pya','ピュ':'py','ピョ':'pyo',

'ッ':'sokuon'}

romanizeText = ''

hiraganaReversed = dict((v,k) for k,v in hiragana.iteritems())
katakanaReversed = dict((v,k) for k,v in katakana.iteritems())
alphanumericsReversed = dict((v,k) for k,v in alphanumerics.iteritems())
dictionaries = [hiragana, katakana, alphanumerics]

def romanizer(romanizeMe):
    global romanizeText
    romanizeMe = romanizeMe.encode('ascii','ignore')
    for dictToUse in dictionaries:
        for char in romanizeMe: 
            try:
                value = dictToUse[char]
                romanizeMe = romanizeMe.replace(char, value)
            except KeyError, e:
                continue
    # romanizeMe = romanizeMe
    return romanizeMe #.decode('utf-8','ignore')

@hook.command
def romanize(inp):
    return romanizer(inp)
