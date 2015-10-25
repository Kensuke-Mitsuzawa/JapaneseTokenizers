#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import unicodedata
import re
import sys

try:
    unicode # python2
    def u(str): return str.decode("utf-8")
    def b(str): return str
    pass
except: # python3
    def u(str): return str
    def b(str): return str.encode("utf-8")
    pass


kanji = u(r'[一-龠]+')
hiragana = u(r'[ぁ-ん]+')
zenkaku_katakana = u(r'[ァ-ヴ]+')
hankaku_symbol_prefix = u(r'[^A-Za-z]')
hankaku_symbol_seq = u(r'[A-Za-z]')


def normalize_text(text):
    """
    :param text:
    :return:
    """
    python_version = sys.version_info
    if python_version >= (3, 0, 0):
        assert isinstance(text, str)
    else:
        assert isinstance(text, unicode)

    try:
        text = unicodedata.normalize('NFKC', text)
    except TypeError:
        sys.exit("argument should be coded in UTF-8")

    text = re.sub(u(r'˗|֊|‐|‑|‒|–|⁃|⁻|₋|−'), '-', text)
    text = re.sub(u(r'﹣|－|ｰ|—|―|─|━'), 'ー', text)
    text = re.sub(u(r'~|∼|∾|〜|〰|～'), '', text)

    text = re.sub(u(r' +'), u(' '), text)
    text = re.sub(u(r'^\s+(.+)$'), u(r'\1'), text)
    text = re.sub(u(r'(.+)\s+$'), u(r'\1'), text)


    # 半角カタカナはすでに全角カタカナに正規化されている
    # 全角英数はすでに半角英数に正規化されている前提
    pattern = u'{}|{}|{}|{}'.format(hiragana, zenkaku_katakana, hankaku_symbol_prefix, kanji)

    while re.findall(u(r'({})\s+({})').format(pattern, pattern), text) != []:
        text = re.sub(u(r'({})\s+({})').format(pattern, pattern), r'\1\2', text)

    pattern = u('{}|{}|{}').format(hiragana, zenkaku_katakana, kanji)
    while re.findall(u(r'({})\s+({})').format(pattern, hankaku_symbol_seq), text) != []:
        text = re.sub(u(r'({})\s+({})').format(pattern, hankaku_symbol_seq), u(r'\1\2'), text)


    return text


def test():
    text = u('あるBさんとCさんがーで〜で-ーだった。   やばい   。＆＊（）＆％。　　プログラミング　Cは難しい。でもLanguage C＋＋はそんなに難しくない。')
    res = normalize_text(text)
    print(res)
    print([res])



if __name__ == '__main__':
    import sys
    import codecs
    test()
    sys.exit()

    path_to_text = sys.argv[1]
    #path_to_text = '../fuman_pipeline/resources/input/fuman_hotel.tsv'
    with codecs.open(path_to_text, 'r', 'utf-8') as f_obj:
        for line in f_obj.readlines():
            print(normalize_text(line).encode('utf-8'))