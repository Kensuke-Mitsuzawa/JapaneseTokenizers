#! -*- coding: utf-8 -*-
import sys
import unittest
from JapaneseTokenizer.mecab_wrapper import MecabWrapper
from JapaneseTokenizer.datamodels import TokenizedSenetence, FilteredObject, TokenizedResult
import os
__author__ = 'kensuke-mi'


class TestFilter(unittest.TestCase):
    def setUp(self):
        '''紗倉 まな（さくらまな、１９９３年３月２３日 - ）は、日本のAV女優みたいだ。'''
        self.test_senetence = u'紗倉 まなは、日本のAV女優みたいで、うつくしい。\nそこで、ぼくはその１枚のはなやかな作品を見たいと思った。'
        self.stopword = ['AV']
        self.pos_condition = [('名詞', '一般',), ('名詞', '固有名詞'), ('形容詞', '自立',), ('助詞', '格助詞', '引用')]
        self.path_user_dict = os.path.join(os.path.dirname(__file__), 'resources/test/userdict.csv')

    def test_filtering(self):
        mecab_obj = MecabWrapper(dictType='ipadic')
        tokenized_sentence = mecab_obj.tokenize(sentence=self.test_senetence,is_feature=True).\
            filter(pos_condition=self.pos_condition, stopwords=self.stopword)
        assert isinstance(tokenized_sentence, TokenizedSenetence)

        seq_except_pos = [(u'動詞',), (u'名詞', u'代名詞'), (u'名詞', u'接尾')]
        seq_match_pos = [(u'名詞',), (u'名詞', u'固有名詞',), (u'形容詞',), (u'形容詞', u'自立'),(u'助詞', u'格助詞', u'引用')]

        for token_obj in tokenized_sentence.tokenized_objects:
            assert isinstance(token_obj, TokenizedResult)

            pos_tuple = token_obj.tuple_pos
            # 結果に入っているべきではない品詞 #
            for except_pos in seq_except_pos:
                self.assertTrue(not set(except_pos).issubset(set(pos_tuple)))
            # 結果に入っているべき品詞 #
            bool_any = any(set(match_pos).issubset(set(pos_tuple)) for match_pos in seq_match_pos)
            self.assertTrue(bool_any)


if __name__ == '__main__':
    unittest.main()