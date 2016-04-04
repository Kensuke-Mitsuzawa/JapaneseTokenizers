#! -*- coding: utf-8 -*-
import logging
import sys
__author__ = 'kensuke-mi'

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")
python_version = sys.version_info

if python_version > (3, 0, 0):
    logging.warn('JUMAN wrapper for python3 is still under development.')
    from JapaneseTokenizer.JUMAN_wrapper.juman_wrapper_python3 import JumanWrapper
    JumanWrapper = JumanWrapper

else:
    from JapaneseTokenizer.JUMAN_wrapper.juman_wrapper_python2 import JumanWrapper
    JumanWrapper = JumanWrapper