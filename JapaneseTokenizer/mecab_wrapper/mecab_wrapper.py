#! -*- coding: utf-8 -*-
import sys
import logging
__author__ = 'kensuke-mi'

python_version = sys.version_info


if python_version >= (3, 0, 0):
    from JapaneseTokenizer.mecab_wrapper.mecab_wrapper_python3 import MecabWrapper
else:
    from JapaneseTokenizer.mecab_wrapper.mecab_wrapper_python2 import MecabWrapper