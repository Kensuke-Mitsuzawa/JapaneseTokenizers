#-*- encoding: utf-8 -*-
# this test file does not work under pycharm
# do your test with command line
from pyknp import Juman
from JapaneseTokenizer.datamodels import TokenizedResult, TokenizedSenetence, FilteredObject
from JapaneseTokenizer.jumanpp_wrapper.jumanpp_wrapper import JumanppWrapper, JumanppClient
from JapaneseTokenizer.common.sever_handler import JumanppHnadler
import pyknp
import socket
import unittest
import os
import logging
logger = logging.getLogger(__file__)
logger.level = logging.INFO


class TestJumanppWrapperPython2(unittest.TestCase):
    def setUp(self):
        # this is under MacOSX10
        self.path_to_juman_command = '/usr/local/bin/jumanpp'
        if not os.path.exists(self.path_to_juman_command): self.path_to_juman_command = 'jumanpp'

    def test_JumanppClient(self):
        test_sentence = u'外国人参政権を欲しい。'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = 'localhost'
        PORT = 12000
        try:
            s.connect((HOST, PORT))
            s.close()
        except:
            logger.warning("SKip server mode test because server is not working.")
        else:
            client_obj = JumanppClient(hostname='localhost', port=12000)
            res = client_obj.query(sentence=test_sentence, pattern=r'EOS')
            del res

    def test_jumanpp_servermode(self):
        ### test with list return object ###
        test_sentence = u'外国人参政権を欲しい。'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = 'localhost'
        PORT = 12000
        try:
            s.connect((HOST, PORT))
            s.close()
        except:
            logger.warning("SKip server mode test because server is not working.")
        else:
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
        test_sentence = u'外国人参政権を欲しい。'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = 'localhost'
        PORT = 12000
        try:
            s.connect((HOST, PORT))
            s.close()
        except:
            logger.warning("SKip server mode test because server is not working.")
        else:
            jumanpp_tokenizer = JumanppWrapper(server='localhost', port=12000)
            for i in range(0, 1000):
                list_tokens = jumanpp_tokenizer.tokenize(sentence=test_sentence, return_list=True)
                assert isinstance(list_tokens, list)
                assert u'外国' in test_sentence
            del jumanpp_tokenizer


    def test_jumanpp_localmode_pyexpect(self):
        test_sentence = u'外国人参政権を欲しい。'
        jumanpp_tokenizer = JumanppWrapper(command=self.path_to_juman_command, is_use_pyknp=False)
        self.assertTrue(isinstance(jumanpp_tokenizer.jumanpp_obj, JumanppHnadler))
        list_tokens = jumanpp_tokenizer.tokenize(sentence=test_sentence, return_list=True)
        assert isinstance(list_tokens, list)

        jumanpp_tokenizer = JumanppWrapper(command=self.path_to_juman_command, is_use_pyknp=False)
        self.assertTrue(isinstance(jumanpp_tokenizer.jumanpp_obj, JumanppHnadler))
        tokenized_obj = jumanpp_tokenizer.tokenize(sentence=test_sentence, return_list=False)
        assert isinstance(tokenized_obj, TokenizedSenetence)

    def test_jumanpp_huge_amount_text(self):
        """pexpectを利用した大量テキスト処理 & テキスト処理中のプロセス再起動"""
        logger.info('under testing of processing huge amount of text...')
        seq_test_sentence = [u'外国人参政権を欲しい。'] * 500
        jumanpp_tokenizer = JumanppWrapper(is_use_pyknp=False, command=self.path_to_juman_command)
        self.assertTrue(isinstance(jumanpp_tokenizer.jumanpp_obj, JumanppHnadler))
        for i, test_s in enumerate(seq_test_sentence):
            tokenized_obj = jumanpp_tokenizer.tokenize(sentence=test_s)
            self.assertTrue(isinstance(tokenized_obj, TokenizedSenetence))
            if not i == 0 and i % 100 == 0:
                """強制的にプロセスを殺して再起動"""
                logger.info('It forces stop unix process.')
                jumanpp_tokenizer.jumanpp_obj.restart_process()
        else:
            pass


if __name__ == '__main__':
    unittest.main()