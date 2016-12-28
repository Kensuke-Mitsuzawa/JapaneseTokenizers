from typing import Callable

class WrapperBase(object):
    def tokenize(self, sentence,
                 normalize,
                 is_feature,
                 is_surface,
                 return_list,
                 func_normalizer=None):
        # type: (, str, bool, bool, bool, bool, Callable[[str], str])
        """* What you can do"""
        raise NotImplemented

    def filter(self, parsed_sentence, pos_condition=None, stopwords=None):
        raise NotImplemented