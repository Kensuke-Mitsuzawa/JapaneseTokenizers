#-*- encoding: utf-8 -*-
# this test file does not work under pycharm
# do your test with command line
from pyknp import Juman
from JapaneseTokenizer.datamodels import TokenizedResult, TokenizedSenetence, FilteredObject
from JapaneseTokenizer.juman_wrapper.juman_wrapper_python3 import JumanWrapper
import pyknp
import unittest
import os


class TestJumanWrapperPython3(unittest.TestCase):
    def setUp(self):
        # this is under MacOSX10
        self.path_to_juman_command = '/usr/local/bin/juman'
        if not os.path.exists(self.path_to_juman_command): self.path_to_juman_command = 'juman'

    def test_juman_wrapper(self):
        juman = Juman(command=self.path_to_juman_command)
        result = juman.analysis("これはペンです。")
        print(','.join(mrph.midasi for mrph in result))

        for mrph in result.mrph_list():
            assert isinstance(mrph, pyknp.Morpheme)
            print("見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s" \
                  % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))

    def test_tokenize(self):
        """This test case checks juman_wrapper.tokenize
        """

        print('Tokenize Test')
        test_sentence = "紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        juman_wrapper = JumanWrapper(command=self.path_to_juman_command)
        token_objects = juman_wrapper.tokenize(sentence=test_sentence,
                                               return_list=False,
                                               is_feature=True
                                               )

        assert isinstance(token_objects, TokenizedSenetence)
        for t_obj in token_objects.tokenized_objects:
            assert isinstance(t_obj, TokenizedResult)
            print("word_surafce:{}, word_stem:{}, pos_tuple:{}, misc_info:{}".format(
                t_obj.word_surface,
                t_obj.word_stem,
                ' '.join(t_obj.tuple_pos),
                t_obj.misc_info
            ))
            assert isinstance(t_obj.word_surface, str)
            assert isinstance(t_obj.word_stem, str)
            assert isinstance(t_obj.tuple_pos, tuple)
            assert isinstance(t_obj.misc_info, dict)

        token_objects_list = token_objects.convert_list_object()
        assert isinstance(token_objects_list, list)
        print('-'*30)
        for stem_posTuple in token_objects_list:
            assert isinstance(stem_posTuple, tuple)
            word_stem = stem_posTuple[0]
            word_posTuple = stem_posTuple[1]
            assert isinstance(word_stem, str)
            assert isinstance(word_posTuple, tuple)

            print('word_stem:{} word_pos:{}'.format(word_stem, ' '.join(word_posTuple)))

    def test_filter_pos(self):
        """
        """
        print('Filtering Test. POS condition is only 名詞')
        test_sentence = "紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        juman_wrapper = JumanWrapper(command=self.path_to_juman_command)
        token_objects = juman_wrapper.tokenize(sentence=test_sentence,
                                               return_list=False,
                                               is_feature=True)
        pos_condition = [('名詞', )]
        filtered_result = juman_wrapper.filter(
            parsed_sentence=token_objects,
            pos_condition=pos_condition
        )

        assert isinstance(filtered_result, FilteredObject)
        for t_obj in filtered_result.tokenized_objects:
            assert isinstance(t_obj, TokenizedResult)
            print("word_surafce:{}, word_stem:{}, pos_tuple:{}, misc_info:{}".format(
                t_obj.word_surface,
                t_obj.word_stem,
                ' '.join(t_obj.tuple_pos),
                t_obj.misc_info
            ))
            assert isinstance(t_obj.word_surface, str)
            assert isinstance(t_obj.word_stem, str)
            assert isinstance(t_obj.tuple_pos, tuple)
            assert isinstance(t_obj.misc_info, dict)

            assert t_obj.tuple_pos[0] == '名詞'

        print('-'*30)
        for stem_posTuple in filtered_result.convert_list_object():
            assert isinstance(stem_posTuple, tuple)
            word_stem = stem_posTuple[0]
            word_posTuple = stem_posTuple[1]
            assert isinstance(word_stem, str)
            assert isinstance(word_posTuple, tuple)

            print('word_stem:{} word_pos:{}'.format(word_stem, ' '.join(word_posTuple)))

    def test_stopwords(self):
        stopword = ['ＡＶ', '女優']
        print ('Stopwords Filtering Test. Stopwords is {}'.format(','.join(stopword)))
        test_sentence = "紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        juman_wrapper = JumanWrapper(command=self.path_to_juman_command)
        token_objects = juman_wrapper.tokenize(sentence=test_sentence,
                                               return_list=False,
                                               is_feature=True
                                               )
        filtered_result = juman_wrapper.filter(
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

            print('word_stem:{} word_pos:{}'.format(word_stem, ' '.join(word_posTuple)))
            if word_stem in stopword: check_flag = False
        assert check_flag


if __name__ == '__main__':
    unittest.main()