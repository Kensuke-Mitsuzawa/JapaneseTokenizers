#! -*- coding: utf-8 -*-
import logging
import sys
__author__ = 'kensuke-mi'

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")
python_version = sys.version_info

if python_version > (3, 0, 0):
    raise SystemError('Kytea for python3 is not implemented yet')

else:
    from JapaneseTokenizer.kytea_wrapper.kytea_wrapper_python2 import KyteaWrapper
    KyteaWrapper = KyteaWrapper