#! -*- coding: utf-8 -*-
# test module
from JapaneseTokenizer.common import sever_handler
# client module
import six
if six.PY2:
    from JapaneseTokenizer.jumanpp_wrapper.jumanpp_wrapper_python2 import JumanppWrapper
else:
    from JapaneseTokenizer.jumanpp_wrapper.jumanpp_wrapper_python3 import JumanppWrapper
# else
import sys
import unittest
import os

__author__ = 'kensuke-mi'

import time



class TestServerHandler(unittest.TestCase):
    def setUp(self):
        self.test_senetence = u'紗倉 まな（さくらまな、1993年3月23日 - ）は、日本のAV女優。'
        self.host = 'localhost'
        self.port = 9999

    def test_jumanpp_server(self):
        """It tests jumanpp server handler"""

        jumanpp_server_handler = sever_handler.JumanppServerHandler(
            host=self.host,
            port=self.port,
            command='jumanpp')
        jumanpp_server_handler.start_server()

        self.jumanpp_clinet = JumanppWrapper(server=self.host, port=self.port)
        res = self.jumanpp_clinet.call_juman_interface(self.test_senetence)




if __name__ == '__main__':
    unittest.main()