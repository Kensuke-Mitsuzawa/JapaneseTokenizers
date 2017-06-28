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
import time
import daemon

__author__ = 'kensuke-mi'


class TestServerHandler(unittest.TestCase):
    @classmethod
    def setUp(cls):
        if six.PY3:
            cls.test_senetence = '紗倉 まな（さくらまな、1993年3月23日 - ）は、日本のAV女優。'
        else:
            cls.test_senetence = u'紗倉 まな（さくらまな、1993年3月23日 - ）は、日本のAV女優。'

        cls.host = 'localhost'
        cls.port = 9999

    def test_jumanpp_server(self):
        """It tests jumanpp server handler"""
        """やりたいこと
        hogehoge = クラス
        hogehoge.start_server()
        hogehoge.analyze()
        hogehoge.stop_server()
        """

        '''
        self.server_object = sever_handler.MultiprocessingSocketStreamServer(self.port, 5)
        jumanpp_server_handler = sever_handler.JumanppServerHandler(command='jumanpp')
        self.server_object.start(jumanpp_server_handler)

        import time
        time.sleep(3)
        self.jumanpp_clinet = JumanppWrapper(server=self.host, port=self.port)
        res = self.jumanpp_clinet.call_juman_interface(self.test_senetence)'''


if __name__ == '__main__':
    unittest.main()