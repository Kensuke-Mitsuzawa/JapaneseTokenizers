class WrapperBase(object):
    def tokenize(self, sentence, normalize=True, is_feature=False, is_surface=False, return_list=True):
        """* What you can do"""
        raise NotImplemented

    def filter(self, parsed_sentence, pos_condition=None, stopwords=None):
        raise NotImplemented