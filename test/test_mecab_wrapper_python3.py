#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import sys
import unittest
from JapaneseTokenizer.mecab_wrapper.mecab_wrapper import MecabWrapper
from JapaneseTokenizer.datamodels import TokenizedSenetence
import os
python_version = sys.version_info


class TestMecabWrapperPython3(unittest.TestCase):
    def setUp(self):
        self.test_senetence = '紗倉 まな（さくらまな、1993年3月23日 - ）は、日本のAV女優。'
        self.test_sentence2 = '午前零時。午前3時。3時。'
        self.path_user_dict = os.path.join(os.path.dirname(__file__), 'resources/test/userdict.csv')

    def test_neologd_parse(self):
        """* Test case
        - neologd辞書で正しく分割できることを確認する
        """
        mecab_obj = MecabWrapper(dictType='neologd')
        parsed_obj = mecab_obj.tokenize(sentence=self.test_senetence)
        self.assertTrue(parsed_obj, TokenizedSenetence)
        self.assertTrue(isinstance(parsed_obj.convert_list_object(), list))
        self.assertTrue(all(isinstance(mrph, str) for mrph in parsed_obj.convert_list_object()))

        parsed_obj = mecab_obj.tokenize(sentence=self.test_sentence2)
        self.assertTrue(parsed_obj, TokenizedSenetence)
        self.assertTrue(isinstance(parsed_obj.convert_list_object(), list))
        self.assertTrue(all(isinstance(mrph, str) for mrph in parsed_obj.convert_list_object()))

    def test_default_parse(self):
        """* Test case
        - デフォルトの状態で動作を確認する
        """
        dictType = "ipadic"
        mecab_obj = MecabWrapper(dictType=dictType)
        assert isinstance(mecab_obj, MecabWrapper)
        
        parsed_obj = mecab_obj.tokenize(sentence=self.test_senetence, return_list=True)
        assert isinstance(parsed_obj, list)
        for morph in parsed_obj:
            assert isinstance(morph, str)

        parsed_obj = mecab_obj.tokenize(sentence=self.test_sentence2, return_list=True)
        assert isinstance(parsed_obj, list)
        for morph in parsed_obj:
            assert isinstance(morph, str)

    def test_init_userdict(self):
        """* Test case
        - すべての辞書を利用した場合の動作を確認する
        """
        mecab_obj = MecabWrapper(dictType='all', pathUserDictCsv=self.path_user_dict)
        assert isinstance(mecab_obj, MecabWrapper)

        res = mecab_obj.tokenize(sentence=self.test_senetence, return_list=True)
        assert isinstance(res, list)
        assert 'さくらまな' in res


if __name__ == '__main__':
    unittest.main()


