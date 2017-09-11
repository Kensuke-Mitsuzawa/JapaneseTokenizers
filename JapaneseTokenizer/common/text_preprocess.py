# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from six import string_types
import jaconv
import six
import re
import unicodedata
import neologdn
__author__ = 'kensuke-mi'

if six.PY2:
    def u(str): return str.decode("utf-8")
    def b(str): return str
    pass
else: # python3
    def u(str): return str
    def b(str): return str.encode("utf-8")
    pass

STRING_EXCEPTION = set([u('*')])

def denormalize_text(input_text):
    """* What you can do
    - It converts text into standard japanese writing way

    * Note
    - hankaku-katakana is to zenkaku-katakana
    - zenkaku-eisu is to hankaku-eisu
    """
    # type: (str)->str
    if input_text in STRING_EXCEPTION:
        return input_text
    else:
        return jaconv.z2h(input_text, kana=False, ascii=True, digit=True)


def normalize_text(input_text,
                   dictionary_mode='ipadic',
                   new_line_replaced='。',
                   is_replace_eos=True,
                   is_kana=True,
                   is_ascii=True,
                   is_digit=True):
    """* What you can do
    - It converts input-text into normalized-text which is good for tokenizer input.

    * Params
    - new_line_replaced: a string which replaces from \n string.
    """
    # type: (string_types,string_types,string_types,bool,bool,bool,bool)->string_types
    if is_replace_eos:
        without_new_line = input_text.replace('\n', new_line_replaced)
    else:
        without_new_line = new_line_replaced

    if dictionary_mode=='neologd':
        return neologdn.normalize(normalize_text_normal_ipadic(without_new_line))
    else:
        return normalize_text_normal_ipadic(without_new_line, kana=is_kana, ascii=is_ascii, digit=is_digit)


def normalize_text_normal_ipadic(input_text, kana=True, ascii=True, digit=True):
    """
    * All hankaku Katanaka is converted into Zenkaku Katakana
    * All hankaku English alphabet and numberc string are converted into Zenkaku one
    """
    # type: (str,bool,bool,bool)->str
    return jaconv.h2z(input_text, kana=kana, ascii=ascii, digit=digit)