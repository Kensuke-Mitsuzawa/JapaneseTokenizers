#! -*- coding: utf-8 -*-
import logging
import sys
__author__ = 'kensuke-mi'

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")
python_version = sys.version_info

if python_version > (3, 0, 0):
    from JapaneseTokenizer.kytea_wrapper.kytea_wrapper_python3 import KyteaWrapper
    KyteaWrapper = KyteaWrapper

else:
    from JapaneseTokenizer.kytea_wrapper.kytea_wrapper_python2 import KyteaWrapper
    KyteaWrapper = KyteaWrapper
