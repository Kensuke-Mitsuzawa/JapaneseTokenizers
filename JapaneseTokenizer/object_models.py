#! -*- coding: utf-8 -*-
from typing import Callable
from six import text_type

class WrapperBase(object):
    def tokenize(self,
                 sentence,
                 normalize,
                 is_feature,
                 is_surface,
                 return_list,
                 func_normalizer=None):
        # type: (text_type, bool, bool, bool, bool, Callable[[text_type], text_type])->None
        """* What you can do"""
        raise NotImplemented

    def filter(self, parsed_sentence, pos_condition=None, stopwords=None):
        raise NotImplemented
