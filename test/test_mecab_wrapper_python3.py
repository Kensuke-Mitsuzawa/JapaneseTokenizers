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
        # test using neologd dictionary
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
        # test default status
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

    def test_parse_jumandic(self):
        mecab_obj = MecabWrapper(dictType='jumandic')
        assert isinstance(mecab_obj, MecabWrapper)

        parsed_obj = mecab_obj.tokenize(sentence=self.test_senetence, return_list=False)
        assert isinstance(parsed_obj, TokenizedSenetence)
        for tokenized_obj in parsed_obj.tokenized_objects:
            if tokenized_obj.word_stem == '女優':
                # ドメイン:文化・芸術 is special output only in Jumandic
                assert 'ドメイン:文化・芸術' in tokenized_obj.analyzed_line

    def test_parse_userdic(self):
        pass

    def test_parse_dictionary_path(self):
        # put path to dictionary and parse sentence.
        path_default_ipadic = '/usr/local/lib/mecab/dic/mecab-ipadic-neologd'
        if os.path.exists(path_default_ipadic):
            mecab_obj = MecabWrapper(dictType=None, path_dictionary=path_default_ipadic)
            assert mecab_obj._path_dictionary == path_default_ipadic
            parsed_obj = mecab_obj.tokenize(sentence=self.test_senetence, return_list=False)
            assert isinstance(parsed_obj, TokenizedSenetence)

    def test_init_userdict(self):
        # this test should be error response.
        mecab_obj = MecabWrapper(dictType='ipadic', pathUserDictCsv=self.path_user_dict)
        assert isinstance(mecab_obj, MecabWrapper)
        parsed_obj = mecab_obj.tokenize(sentence=self.test_senetence, return_list=False)
        assert isinstance(parsed_obj, TokenizedSenetence)
        is_ok = False
        for tokenized_obj in parsed_obj.tokenized_objects:
            if tokenized_obj.word_stem == 'さくらまな':
                is_ok = True
        assert is_ok


if __name__ == '__main__':
    unittest.main()



