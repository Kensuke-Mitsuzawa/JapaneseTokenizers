# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from six import text_type
import jaconv
import six
import re
import unicodedata
from JapaneseTokenizer import init_logger
import logging
logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
__author__ = 'kensuke-mi'

if six.PY2:
    def u(str): return str.decode("utf-8")
    def b(str): return str
    pass
else: # python3
    def u(str): return str
    def b(str): return str.encode("utf-8")
    pass

try:
    import neologdn
    is_neologdn_valid = True
except:
    logger.warning("neologdn package is not installed yet. You could not call neologd dictionary.")
    is_neologdn_valid = False

STRING_EXCEPTION = set([u('*')])


def denormalize_text(input_text):
    # type: (text_type)->text_type
    """* What you can do
    - It converts text into standard japanese writing way

    * Note
    - hankaku-katakana is to zenkaku-katakana
    - zenkaku-eisu is to hankaku-eisu
    """
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
    # type: (text_type,text_type,text_type,bool,bool,bool,bool)->text_type
    """* What you can do
    - It converts input-text into normalized-text which is good for tokenizer input.

    * Params
    - new_line_replaced: a string which replaces from \n string.
    """
    if is_replace_eos:
        without_new_line = input_text.replace('\n', new_line_replaced)
    else:
        without_new_line = new_line_replaced

    if dictionary_mode=='neologd' and is_neologdn_valid:
        return neologdn.normalize(normalize_text_normal_ipadic(without_new_line))
    elif dictionary_mode=='neologd' and is_neologdn_valid == False:
        raise Exception("You could not call neologd dictionary bacause you do NOT install the package neologdn.")
    else:
        return normalize_text_normal_ipadic(without_new_line, kana=is_kana, ascii=is_ascii, digit=is_digit)


def normalize_text_normal_ipadic(input_text, kana=True, ascii=True, digit=True):
    # type: (text_type,bool,bool,bool)->text_type
    """
    * All hankaku Katanaka is converted into Zenkaku Katakana
    * All hankaku English alphabet and numberc string are converted into Zenkaku one
    """
    return jaconv.h2z(input_text, kana=kana, ascii=ascii, digit=digit)
