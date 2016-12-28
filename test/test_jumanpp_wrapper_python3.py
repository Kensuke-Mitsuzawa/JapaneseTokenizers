#-*- encoding: utf-8 -*-
# this test file does not work under pycharm
# do your test with command line
from pyknp import Juman
from JapaneseTokenizer.datamodels import TokenizedResult, TokenizedSenetence, FilteredObject
from JapaneseTokenizer.jumanpp_wrapper.jumanpp_wrapper_python3 import JumanppWrapper, JumanppClient
import pyknp
import unittest
import os
import logging
logger = logging.getLogger(__file__)
logger.level = logging.DEBUG


class TestJumanppWrapperPython3(unittest.TestCase):
    def setUp(self):
        # this is under MacOSX10
        self.path_to_juman_command = '/usr/local/bin/juman'
        if not os.path.exists(self.path_to_juman_command): self.path_to_juman_command = 'juman'

    def test_JumanppClient(self):
        test_sentence = '外国人参政権を欲しい。'
        client_obj = JumanppClient(hostname='localhost', port=12000)
        res = client_obj.query(sentence=test_sentence, pattern=rb'EOS')

        del res

    def test_jumanpp_servermode(self):
        ### test with list return object ###
        test_sentence = '外国人参政権を欲しい。'
        jumanpp_tokenizer = JumanppWrapper(server='localhost', port=12000)
        list_tokens = jumanpp_tokenizer.tokenize(sentence=test_sentence, return_list=True)
        assert isinstance(list_tokens, list)

        ### test with TokenizedSenetence return object ###
        tokenized_obj = jumanpp_tokenizer.tokenize(sentence=test_sentence, return_list=False)
        assert isinstance(tokenized_obj, TokenizedSenetence)

        ### test with TokenizedSenetence return object and filter by chain expression ###
        pos_condtion = [('名詞', )]
        filtered_res = jumanpp_tokenizer.tokenize(sentence=test_sentence, return_list=False).filter(pos_condition=pos_condtion)
        assert isinstance(filtered_res, FilteredObject)
        assert isinstance(filtered_res.convert_list_object(), list)

    def test_jumanpp_servermode_stress(self):
        ### test with severmode with much stress ###
        test_sentence = '外国人参政権を欲しい。'
        jumanpp_tokenizer = JumanppWrapper(server='localhost', port=12000)
        for i in range(0, 1000):
            list_tokens = jumanpp_tokenizer.tokenize(sentence=test_sentence, return_list=True)
            assert isinstance(list_tokens, list)
            assert '外国' in test_sentence
        del jumanpp_tokenizer


    def test_jumanpp_localmode(self):
        test_sentence = '外国人参政権を欲しい。'
        jumanpp_tokenizer = JumanppWrapper()
        list_tokens = jumanpp_tokenizer.tokenize(sentence=test_sentence, return_list=True)
        assert isinstance(list_tokens, list)

        jumanpp_tokenizer = JumanppWrapper()
        tokenized_obj = jumanpp_tokenizer.tokenize(sentence=test_sentence, return_list=False)
        assert isinstance(tokenized_obj, TokenizedSenetence)


if __name__ == '__main__':
    unittest.main()