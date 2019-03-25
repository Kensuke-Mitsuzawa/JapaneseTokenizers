#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import sys
import unittest
from JapaneseTokenizer.mecab_wrapper.mecab_wrapper import MecabWrapper
from JapaneseTokenizer.datamodels import TokenizedSenetence
from six import string_types
import os
python_version = sys.version_info


class TestMecabWrapperPython2(unittest.TestCase):
    def setUp(self):
        self.test_senetence = u'紗倉 まな（さくらまな、1993年3月23日 - ）は、日本のAV女優。'
        self.test_sentence2 = u'午前零時。午前3時。3時。'
        self.path_user_dict = os.path.join(os.path.dirname(__file__), 'resources/test/userdict.csv')

    def test_neologd_parse(self):
        """* Test case
        - neologd辞書で正しく分割できることを確認する
        """
        mecab_obj = MecabWrapper(dictType='neologd')
        parsed_obj = mecab_obj.tokenize(sentence=self.test_senetence)
        self.assertTrue(parsed_obj, TokenizedSenetence)
        self.assertTrue(isinstance(parsed_obj.convert_list_object(), list))
        self.assertTrue(all(isinstance(mrph, string_types) for mrph in parsed_obj.convert_list_object()))

        parsed_obj = mecab_obj.tokenize(sentence=self.test_sentence2)
        self.assertTrue(parsed_obj, TokenizedSenetence)
        self.assertTrue(isinstance(parsed_obj.convert_list_object(), list))
        self.assertTrue(all(isinstance(mrph, string_types) for mrph in parsed_obj.convert_list_object()))

    def test_default_parse(self):
        """* Test case
        - デフォルトの状態で動作を確認する
        """
        dictType = "ipadic"
        mecab_obj = MecabWrapper(dictType=dictType)
        assert isinstance(mecab_obj, MecabWrapper)
        parsed_obj = mecab_obj.tokenize(sentence=self.test_senetence, return_list=True)
        assert isinstance(parsed_obj, list)
        if python_version >= (3, 0, 0):
            for morph in parsed_obj:
                assert isinstance(morph, str)
        else:
            for morph in parsed_obj:
                assert isinstance(morph, string_types)

    def test_init_userdict(self):
        # test when user dictionary is called
        mecab_obj = MecabWrapper(dictType='ipadic', pathUserDictCsv=self.path_user_dict)
        assert isinstance(mecab_obj, MecabWrapper)
        parsed_obj = mecab_obj.tokenize(sentence=self.test_senetence, return_list=True)
        is_ok = False
        for morph in parsed_obj:
            if u'さくらまな' == morph:
                is_ok = True
        else:
            pass
        assert is_ok

    def test_parse_jumandic(self):
        with self.assertRaises(Exception):
            mecab_obj = MecabWrapper(dictType='jumandic')
            assert isinstance(mecab_obj, MecabWrapper)

    def test_init_alldict(self):
        """* Test case
        - すべての辞書を利用した場合の動作を確認する
        """
        with self.assertRaises(Exception):
            mecab_obj = MecabWrapper(dictType='all', pathUserDictCsv=self.path_user_dict)
            assert isinstance(mecab_obj, MecabWrapper)


if __name__ == '__main__':
    unittest.main()
