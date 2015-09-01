#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import unittest
from JapaneseTokenizer.mecab_wrapper import mecab_wrapper


class TestMecabWrapper(unittest.TestCase):
    def setUp(self):
        self.test_senetence = u'紗倉 まな（さくらまな、1993年3月23日 - ）は、日本のAV女優。'
        self.path_user_dict = '../resources/test/userdict.csv'


    def test_init_mecab_wrapper(self):
        dictType = "neologd"
        osType = "mac"
        mecab_obj = mecab_wrapper.MecabWrapper(dictType=dictType, osType="mac")
        assert isinstance(mecab_obj, mecab_wrapper.MecabWrapper)

        return mecab_obj


    def test_default_parse(self):
        mecab_obj = self.test_init_mecab_wrapper()
        parsed_obj = mecab_obj.tokenize(sentence=self.test_senetence)
        assert isinstance(parsed_obj, list)
        for morph in parsed_obj: assert isinstance(morph, unicode)


    def test_init_userdict(self):
        dictType = "user"
        osType = "mac"

        mecab_obj = mecab_wrapper.MecabWrapper(dictType=dictType, osType=osType, pathUserDictCsv=self.path_user_dict)
        assert isinstance(mecab_obj, mecab_wrapper.MecabWrapper)

        res = mecab_obj.tokenize(sentence=self.test_senetence)
        assert isinstance(res, list)
        assert u'さくらまな' in res







def suite():
    suite = unittest.TestSuite()
    suite.addTests(unittest.makeSuite(TestMecabWrapper))

    return suite


