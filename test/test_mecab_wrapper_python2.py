#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import sys
import unittest
from JapaneseTokenizer.mecab_wrapper.mecab_wrapper_python2 import MecabWrapper
import os
python_version = sys.version_info


class TestMecabWrapperPython2(unittest.TestCase):
    def setUp(self):
        self.test_senetence = u'紗倉 まな（さくらまな、1993年3月23日 - ）は、日本のAV女優。'
        self.path_user_dict = os.path.join(os.path.dirname(__file__), 'resources/test/userdict.csv')


    def test_init_mecab_wrapper(self):
        dictType = "neologd"
        mecab_obj = MecabWrapper(dictType=dictType)
        assert isinstance(mecab_obj, MecabWrapper)

        return mecab_obj


    def test_default_parse(self):
        mecab_obj = self.test_init_mecab_wrapper()
        parsed_obj = mecab_obj.tokenize(sentence=self.test_senetence, return_list=True)
        assert isinstance(parsed_obj, list)
        if python_version >= (3, 0, 0):
            for morph in parsed_obj: assert isinstance(morph, str)
            print(parsed_obj)
        else:
            for morph in parsed_obj: assert isinstance(morph, unicode)


    def test_init_userdict(self):
        dictType = "user"
        osType = "mac"

        mecab_obj = MecabWrapper(dictType=dictType, pathUserDictCsv=self.path_user_dict, osType=osType)
        assert isinstance(mecab_obj, MecabWrapper)

        res = mecab_obj.tokenize(sentence=self.test_senetence, return_list=True)
        assert isinstance(res, list)
        assert u'さくらまな' in res


if __name__ == '__main__':
    unittest.main()