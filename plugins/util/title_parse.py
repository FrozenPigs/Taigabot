# Copyright (C) 2020  Anthony DeDominic <adedomin@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
from enum import auto, Enum
from sys import argv
from html.entities import html5 as char_entities


class TitleParserTokens(Enum):
    WHITESPACE = auto()
    TITLE = auto()
    WORDS = auto()
    DEC_CHAR_ENT = auto()
    HEX_CHAR_ENT = auto()
    WORD_CHAR_ENT = auto()
    OTHER_TAG = auto()
    INVALID = auto()


TitleTokenizer = re.compile(f'''(?x)
 (?P<{TitleParserTokens.WHITESPACE.name}>\\s+)
|(?P<{TitleParserTokens.TITLE.name}>[<][/]?\\s*[tT][iI][tT][lL][eE][^>]*[>])
|(?P<{TitleParserTokens.WORDS.name}>[^<>&"'\\s]+)
|(?P<{TitleParserTokens.DEC_CHAR_ENT.name}>
  [&][#]
   (?P<__internal_dec_code_value>\\d+)
  ;
 )
|(?P<{TitleParserTokens.HEX_CHAR_ENT.name}>
  [&][#]x
   (?P<__internal_hex_code_value>[a-fA-F0-9]+)
  ;
 )
|(?P<{TitleParserTokens.WORD_CHAR_ENT.name}>
  [&]
   (?P<__internal_word_code_value>\\w+;)
 )
|(?P<{TitleParserTokens.OTHER_TAG.name}>
  [<][/]?\\s*
   (?P<__internal_tag_name>[\\w!]+)
  [^>]*[>])
|(?P<{TitleParserTokens.INVALID.name}>.)
''')


def tokenize_title_chunk(html_chunk):
    for match_obj in re.finditer(TitleTokenizer, html_chunk):
        typeof = TitleParserTokens[match_obj.lastgroup]
        value = match_obj.group()
        if (typeof == TitleParserTokens.OTHER_TAG):
            value = match_obj.group('__internal_tag_name')
        elif (typeof == TitleParserTokens.WHITESPACE):
            value = ' '
        elif (typeof == TitleParserTokens.DEC_CHAR_ENT):
            value = match_obj.group('__internal_dec_code_value')
        elif (typeof == TitleParserTokens.HEX_CHAR_ENT):
            value = match_obj.group('__internal_hex_code_value')
        elif (typeof == TitleParserTokens.WORD_CHAR_ENT):
            value = match_obj.group('__internal_word_code_value')

        yield (typeof, value)


def parse_title_chunk(tokens):
    in_title = False
    reduce = []
    for tkn in tokens:
        if (not in_title and tkn[0] == TitleParserTokens.TITLE):
            in_title = True
        elif (in_title and tkn[0] == TitleParserTokens.TITLE):
            break
        elif (in_title):
            if (tkn[0] == TitleParserTokens.DEC_CHAR_ENT or
                    tkn[0] == TitleParserTokens.HEX_CHAR_ENT):
                try:
                    cvalue = chr(int(tkn[1],
                                     10
                                     if tkn[0] ==
                                        TitleParserTokens.DEC_CHAR_ENT
                                     else 16))
                except ValueError:
                    cvalue = '�'
                reduce.append(cvalue)
            elif (tkn[0] == TitleParserTokens.WORD_CHAR_ENT):
                try:
                    cvalue = char_entities[tkn[1]]
                except KeyError:
                    cvalue = '�'
                reduce.append(cvalue)
            elif (tkn[0] == TitleParserTokens.OTHER_TAG):
                tag = tkn[1].lower()
                if (tag == 'b'):
                    reduce.append('\x02')
                elif (tag == 'i'):
                    reduce.append('\x1d')
                elif (tag == 'u'):
                    reduce.append('\x1f')
                elif (tag == 's'):
                    reduce.append('\x1e')
            else:
                reduce.append(tkn[1])

    return ''.join(reduce)


if __name__ == '__main__':
    with open(argv[1], 'rb') as f:
        print(
            parse_title_chunk(
                tokenize_title_chunk(f.read()
                                      .decode('utf-8'))))
