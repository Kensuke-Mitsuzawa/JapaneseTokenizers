#-*- encoding: utf-8 -*-
# this test file does not work under pycharm
# do your test with command line
from pyknp import Juman
from JapaneseTokenizer.datamodels import TokenizedResult, TokenizedSenetence, FilteredObject
from JapaneseTokenizer.juman_wrapper import JumanWrapper
import pyknp
import unittest
import os
import logging
import socket
logger = logging.getLogger(__file__)
logger.level = logging.INFO


class TestJumanWrapperPython3(unittest.TestCase):
    def setUp(self):
        # this is under MacOSX10
        self.path_to_juman_command = '/usr/local/bin/juman'
        if not os.path.exists(self.path_to_juman_command): self.path_to_juman_command = 'juman'

    def test_juman_wrapper(self):
        try:
            juman = Juman(command=self.path_to_juman_command)
            result = juman.analysis("これはペンです。")
            logger.debug(','.join(mrph.midasi for mrph in result))

            for mrph in result.mrph_list():
                assert isinstance(mrph, pyknp.Morpheme)
                logger.debug("見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s" \
                      % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))
        except ImportError:
            print('skip test_juman_wrapper')

    def test_tokenize(self):
        """This test case checks juman_wrapper.tokenize
        """
        logger.debug('Tokenize Test')
        test_sentence = "紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        juman_wrapper = JumanWrapper(command=self.path_to_juman_command)
        token_objects = juman_wrapper.tokenize(sentence=test_sentence,
                                               return_list=False,
                                               is_feature=True)

        assert isinstance(token_objects, TokenizedSenetence)
        for t_obj in token_objects.tokenized_objects:
            assert isinstance(t_obj, TokenizedResult)
            logger.debug("word_surafce:{}, word_stem:{}, pos_tuple:{}, misc_info:{}".format(
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
        logger.debug('-'*30)
        for stem_posTuple in token_objects_list:
            assert isinstance(stem_posTuple, tuple)
            word_stem = stem_posTuple[0]
            word_posTuple = stem_posTuple[1]
            assert isinstance(word_stem, str)
            assert isinstance(word_posTuple, tuple)

            logger.debug('word_stem:{} word_pos:{}'.format(word_stem, ' '.join(word_posTuple)))

    def test_filter_pos(self):
        """POS filteringのテスト
        """
        logger.debug('Filtering Test. POS condition is only 名詞')
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
            logger.debug("word_surafce:{}, word_stem:{}, pos_tuple:{}, misc_info:{}".format(
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

        logger.debug('-'*30)
        for stem_posTuple in filtered_result.convert_list_object():
            assert isinstance(stem_posTuple, tuple)
            word_stem = stem_posTuple[0]
            word_posTuple = stem_posTuple[1]
            assert isinstance(word_stem, str)
            assert isinstance(word_posTuple, tuple)

            logger.debug('word_stem:{} word_pos:{}'.format(word_stem, ' '.join(word_posTuple)))

    def test_stopwords(self):
        """stopword除去のテスト"""
        stopword = ['ＡＶ', '女優']
        logger.debug ('Stopwords Filtering Test. Stopwords is {}'.format(','.join(stopword)))
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

            logger.debug('word_stem:{} word_pos:{}'.format(word_stem, ' '.join(word_posTuple)))
            if word_stem in stopword: check_flag = False
        assert check_flag

    def test_juman_severmode(self):
        """* What you can do
        - juman server modeのテストを実施する
        """
        logger.debug('Tokenize test with server mode')
        test_sentence = "紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        # check socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        HOST = 'localhost'
        PORT = 32000
        try:
            s.connect((HOST, PORT))
            s.close()
        except:
            logger.warning("SKip server mode test because server is not working.")
        else:
            juman_wrapper = JumanWrapper(command=self.path_to_juman_command, server=HOST, port=PORT)
            token_objects = juman_wrapper.tokenize(sentence=test_sentence,
                                                   return_list=False,
                                                   is_feature=True)
            assert isinstance(token_objects, TokenizedSenetence)

            test_sentence = "ペルシア語（ペルシアご、ペルシア語: فارسی‌‎, پارسی‌; Fārsī, Pārsī）は、イランを中心とする中東地域で話される言語。"
            juman_wrapper = JumanWrapper(command=self.path_to_juman_command, server=HOST, port=PORT)
            list_token = juman_wrapper.tokenize(sentence=test_sentence,
                                                   return_list=True,
                                                   is_feature=True)
            assert isinstance(list_token, list)


if __name__ == '__main__':
    unittest.main()