# -*- coding: utf-8 -*-
from JapaneseTokenizer.kytea_wrapper import KyteaWrapper
from JapaneseTokenizer.datamodels import TokenizedResult, TokenizedSenetence, FilteredObject
import unittest

class TestKyteaWrapperPython3(unittest.TestCase):

    def setUp(self):
        pass

    def test_tokenization(self):
        input_sentence = "紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        kytea_wrapper = KyteaWrapper()
        tokenized_result = kytea_wrapper.tokenize(
            sentence=input_sentence,
            normalize=True,
            return_list=False,
            is_feature=True
        )
        assert isinstance(tokenized_result, TokenizedSenetence)
        for t_obj in tokenized_result.tokenized_objects:
            assert isinstance(t_obj, TokenizedResult)

        #print('-'*30)
        tokenized_result_list = tokenized_result.convert_list_object()
        assert isinstance(tokenized_result_list, list)
        for t_obj_tuple in tokenized_result_list:
            assert isinstance(t_obj_tuple, tuple)

    def test_filter_pos(self):
        """
        """
        # 'Filtering Test. POS condition is only 名詞')
        test_sentence = "紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        kytea_wrapper = KyteaWrapper()
        tokenized_result = kytea_wrapper.tokenize(
            sentence=test_sentence,
            normalize=True,
            return_list=False,
            is_feature=True
        )
        pos_condition = [('名詞', )]
        filtered_result = kytea_wrapper.filter(
            parsed_sentence=tokenized_result,
            pos_condition=pos_condition
        )

        assert isinstance(filtered_result, FilteredObject)
        for t_obj in filtered_result.tokenized_objects:
            assert isinstance(t_obj, TokenizedResult)
            assert isinstance(t_obj.word_surface, str)
            assert isinstance(t_obj.word_stem, str)
            assert isinstance(t_obj.tuple_pos, tuple)
            assert isinstance(t_obj.misc_info, dict)

            assert t_obj.tuple_pos[0] == '名詞'

        for stem_posTuple in filtered_result.convert_list_object():
            assert isinstance(stem_posTuple, tuple)
            word_stem = stem_posTuple[0]
            word_posTuple = stem_posTuple[1]
            assert isinstance(word_stem, str)
            assert isinstance(word_posTuple, tuple)

    def test_stopwords(self):
        stopword = ['女優']
        # ('Stopwords Filtering Test. Stopwords is {}'.format(','.join(stopword)))
        test_sentence = "紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        kytea_wrapper = KyteaWrapper()
        token_objects = kytea_wrapper.tokenize(sentence=test_sentence,
                                               return_list=False,
                                               is_feature=True
                                               )
        filtered_result = kytea_wrapper.filter(
            parsed_sentence=token_objects,
            stopwords=stopword
        )

        check_flag = True
        for stem_posTuple in filtered_result.convert_list_object():
            assert isinstance(stem_posTuple, tuple)
            word_stem = stem_posTuple[0]
            word_posTuple = stem_posTuple[1]
            assert isinstance(word_stem, str)
            assert isinstance(word_posTuple, tuple)
            if word_stem in stopword: check_flag = False
        assert check_flag


if __name__ == '__main__':
    unittest.main()
