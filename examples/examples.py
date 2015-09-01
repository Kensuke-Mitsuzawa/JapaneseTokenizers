#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'
import sys
import os

abs_path = os.path.abspath(sys.argv[0])
abs_path_dir = os.path.dirname(abs_path)
sys.path.append(abs_path_dir)
os.chdir(abs_path_dir)

sys.path.append('../JapaneseTokenizer/')
from mecab_wrapper.mecab_wrapper import MecabWrapper

def __example():

    example_user_dict = "../resources/test/userdict.csv"
    osType="mac"

    mecab_wrapper = MecabWrapper(dictType='all', osType=osType, pathUserDictCsv=example_user_dict)

    sentence = u'テヘラン（ペルシア語: تهران  ; Tehrān Tehran.ogg 発音[ヘルプ/ファイル]/teɦˈrɔːn/、英語:Tehran）は、西アジア、イランの首都でありかつテヘラン州の州都。人口12,223,598人。都市圏人口は13,413,348人に達する。'
    with_freature_res = mecab_wrapper.tokenize(sentence, is_feature=True, is_surface=False)
    without_freature_res = mecab_wrapper.tokenize(sentence, is_feature=False, is_surface=False)

    for token_tuple in with_freature_res:
        print u'{}_{}'.format(token_tuple[0], u'_'.join(token_tuple[1]))

    for surface in without_freature_res:
        print surface

if __name__ == "__main__":
    __example()