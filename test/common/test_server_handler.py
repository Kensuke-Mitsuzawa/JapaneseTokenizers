#! -*- coding: utf-8 -*-
# test module
from JapaneseTokenizer.common import sever_handler
# client module
import six
if six.PY2:
    from JapaneseTokenizer.jumanpp_wrapper.__jumanpp_wrapper_python2 import JumanppWrapper
else:
    from JapaneseTokenizer.jumanpp_wrapper.__jumanpp_wrapper_python3 import JumanppWrapper
# else
import sys
import unittest
import os
import time

__author__ = 'kensuke-mi'


class TestServerHandler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if six.PY3:
            cls.test_senetence = '紗倉 まな（さくらまな、1993年3月23日 - ）は、日本のAV女優。'
        else:
            cls.test_senetence = u'紗倉 まな（さくらまな、1993年3月23日 - ）は、日本のAV女優。'

        cls.jumanpp_command = "/usr/local/bin/jumanpp"


    def test_jumanpp_process_hanlder_normal(self):
        """It tests jumanpp process handler"""
        # normal test #
        jumanpp_process_handler = sever_handler.JumanppHnadler(jumanpp_command=self.jumanpp_command)
        result_jumanpp_analysis = jumanpp_process_handler.query(input_string=self.test_senetence)
        self.assertTrue(isinstance(result_jumanpp_analysis,six.text_type))
        ## stop process ##
        jumanpp_process_handler.stop_process()
        ## delete instance ##
        del jumanpp_process_handler

    def test_jumanpp_process_handler_timeout_exception(self):
        """It tests the case which causes timeout exception"""
        with self.assertRaises(Exception) as exc:
            jumanpp_process_handler = sever_handler.JumanppHnadler(jumanpp_command=self.jumanpp_command,
                                                                   timeout_second=1)
            result_jumanpp_analysis = jumanpp_process_handler.query(input_string=self.test_senetence*100)
        exception_message = exc.exception
        jumanpp_process_handler.stop_process()

    def test_jumanpp_process_handler_init_exception(self):
        with self.assertRaises(Exception) as exc:
            jumanpp_process_handler = sever_handler.JumanppHnadler(jumanpp_command='hoge',
                                                                   timeout_second=1)
        exception_message = exc.exception

    def test_jumanpp_process_handler_huge_request(self):
        """It tests the case where a user sends too much request"""
        input_huge_request = [self.test_senetence] * 100
        jumanpp_process_handler = sever_handler.JumanppHnadler(jumanpp_command=self.jumanpp_command)
        seq_result_jumanpp_analysis = [jumanpp_process_handler.query(input_string=sentence)
                                       for sentence in input_huge_request]
        self.assertTrue(isinstance(seq_result_jumanpp_analysis, list))


if __name__ == '__main__':
    unittest.main()