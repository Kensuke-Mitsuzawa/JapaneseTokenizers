#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import sys
import unittest
from JapaneseTokenizer.mecab_wrapper.mecab_wrapper_python3 import MecabWrapper
import os
python_version = sys.version_info


class TestMecabWrapperPython3(unittest.TestCase):
    def setUp(self):
        self.test_senetence = '紗倉 まな（さくらまな、1993年3月23日 - ）は、日本のAV女優。'
        self.path_user_dict = os.path.join(os.path.dirname(__file__), 'resources/test/userdict.csv')

    def test_init_mecab_wrapper(self):
        dictType = "ipadic"
        mecab_obj = MecabWrapper(dictType=dictType)
        assert isinstance(mecab_obj, MecabWrapper)

        return mecab_obj

    def test_default_parse(self):
        mecab_obj = self.test_init_mecab_wrapper()
        parsed_obj = mecab_obj.tokenize(sentence=self.test_senetence, return_list=True)
        assert isinstance(parsed_obj, list)
        for morph in parsed_obj:
            assert isinstance(morph, str)

    def test_init_userdict(self):
        mecab_obj = MecabWrapper(dictType='all', pathUserDictCsv=self.path_user_dict)
        assert isinstance(mecab_obj, MecabWrapper)

        res = mecab_obj.tokenize(sentence=self.test_senetence, return_list=True)
        assert isinstance(res, list)
        assert 'さくらまな' in res


if __name__ == '__main__':
    unittest.main()


