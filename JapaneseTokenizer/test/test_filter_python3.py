#! -*- coding: utf-8 -*-
import sys
import unittest
from JapaneseTokenizer.mecab_wrapper import MecabWrapper
from JapaneseTokenizer.datamodels import TokenizedSenetence, FilteredObject, TokenizedResult
import os
__author__ = 'kensuke-mi'


class TestFilter(unittest.TestCase):
    def setUp(self):
        self.test_senetence = '紗倉 まな（さくらまな、1993年3月23日 - ）は、日本のAV女優。'
        self.stopword = ['AV']
        self.pos_condition = [('名詞', '固有名詞'), ('形容詞', '自立', ),]
        self.path_user_dict = os.path.join(os.path.dirname(__file__), 'resources/test/userdict.csv')

    def test_filtering(self):
        mecab_obj = MecabWrapper(
            dictType='ipaddic',
            osType='generic'
        )
        tokenized_sentence = mecab_obj.tokenize(
            sentence=self.test_senetence,
            is_feature=True,
            return_list=False
        )
        assert isinstance(tokenized_sentence, TokenizedSenetence)

        filtered_obj = mecab_obj.filter(
            parsed_sentence=tokenized_sentence,
            pos_condition=self.pos_condition,
            stopwords=self.stopword
        )
        assert isinstance(filtered_obj, FilteredObject)

        except_pos = set(['動詞'])
        match_pos_1 = set(['名詞'])

        check_flag = False
        for token_obj in filtered_obj.tokenized_objects:
            assert isinstance(token_obj, TokenizedResult)

            pos_tuple = token_obj.tuple_pos
            if except_pos.issubset(set(pos_tuple)): raise Exception('Filtering Failed')
            if match_pos_1.issubset(set(pos_tuple)): check_flag=True

        if check_flag==False:
            raise Exception('Filtering works too much.')



if __name__ == '__main__':
    unittest.main()