#! -*- coding: utf-8 -*-
import logging
import sys
__author__ = 'kensuke-mi'

python_version = sys.version_info

if python_version > (3, 0, 0):
    from JapaneseTokenizer.jumanpp_wrapper.jumanpp_wrapper_python3 import JumanppWrapper
    JumanppWrapper = JumanppWrapper
else:
    from JapaneseTokenizer.jumanpp_wrapper.jumanpp_wrapper_python2 import JumanppWrapper
    JumanppWrapper = JumanppWrapper