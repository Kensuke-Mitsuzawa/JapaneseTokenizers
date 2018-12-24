#-*- encoding: utf-8 -*-
# this test file does not work under pycharm
# do your test with command line
from __future__ import absolute_import
from __future__ import division
from future.utils import string_types, text_type
from JapaneseTokenizer.datamodels import TokenizedResult, TokenizedSenetence, FilteredObject
from JapaneseTokenizer.juman_wrapper import JumanWrapper
import pyknp
import unittest
import sys
import codecs
import logging
sys.stdin = codecs.getreader('utf_8')(sys.stdin)
sys.stdout = codecs.getwriter('utf_8')(sys.stdout)
logger = logging.getLogger(__file__)
logger.level = logging.INFO


class TestJumanWrapperPython2(unittest.TestCase):
    def setUp(self):
        pass

    def test_juman_wrapper(self):
        try:
            from pyknp import Juman

            juman = Juman(command='juman', jumanpp=False)
            result = juman.analysis(u"これはペンです。")
            logger.debug(','.join(mrph.midasi for mrph in result))

            for mrph in result.mrph_list():
                assert isinstance(mrph, pyknp.Morpheme)
                logger.debug(u"見出し:%s, 読み:%s, 原形:%s, 品詞:%s, 品詞細分類:%s, 活用型:%s, 活用形:%s, 意味情報:%s, 代表表記:%s" \
                  % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))
        except ImportError:
            logger.debug('skip test_juman_wrapper')

    def test_tokenize(self):
        """This test case checks juman_wrapper.tokenize
        """

        logger.debug (u'Tokenize Test')
        test_sentence = u"紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        juman_wrapper = JumanWrapper()
        token_objects = juman_wrapper.tokenize(sentence=test_sentence,
                                               return_list=False,
                                               is_feature=True)

        assert isinstance(token_objects, TokenizedSenetence)
        for t_obj in token_objects.tokenized_objects:
            assert isinstance(t_obj, TokenizedResult)
            logger.debug(u"word_surafce:{}, word_stem:{}, pos_tuple:{}, misc_info:{}".format(
                t_obj.word_surface,
                t_obj.word_stem,
                ' '.join(t_obj.tuple_pos),
                t_obj.misc_info
            ))
            assert isinstance(t_obj.word_surface, string_types)
            assert isinstance(t_obj.word_stem, string_types)
            assert isinstance(t_obj.tuple_pos, tuple)
            assert isinstance(t_obj.misc_info, dict)

        token_objects_list = token_objects.convert_list_object()
        assert isinstance(token_objects_list, list)
        logger.debug('-'*30)
        for stem_posTuple in token_objects_list:
            assert isinstance(stem_posTuple, tuple)
            word_stem = stem_posTuple[0]
            word_posTuple = stem_posTuple[1]
            assert isinstance(word_stem, string_types)
            assert isinstance(word_posTuple, tuple)

            logger.debug(u'word_stem:{} word_pos:{}'.format(word_stem, ' '.join(word_posTuple)))

    def test_filter_pos(self):
        """
        """
        logger.debug (u'Filtering Test. POS condition is only 名詞')
        test_sentence = u"紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        juman_wrapper = JumanWrapper()
        token_objects = juman_wrapper.tokenize(sentence=test_sentence,
                                               return_list=False,
                                               is_feature=True
                                               )
        pos_condition = [(u'名詞', )]
        filtered_result = juman_wrapper.filter(
            parsed_sentence=token_objects,
            pos_condition=pos_condition
        )

        assert isinstance(filtered_result, FilteredObject)
        for t_obj in filtered_result.tokenized_objects:
            assert isinstance(t_obj, TokenizedResult)
            logger.debug(u"word_surafce:{}, word_stem:{}, pos_tuple:{}, misc_info:{}".format(
                t_obj.word_surface,
                t_obj.word_stem,
                ' '.join(t_obj.tuple_pos),
                t_obj.misc_info
            ))
            assert isinstance(t_obj.word_surface, string_types)
            assert isinstance(t_obj.word_stem, string_types)
            assert isinstance(t_obj.tuple_pos, tuple)
            assert isinstance(t_obj.misc_info, dict)

            assert t_obj.tuple_pos[0] == u'名詞'

        logger.debug('-'*30)
        for stem_posTuple in filtered_result.convert_list_object():
            assert isinstance(stem_posTuple, tuple)
            word_stem = stem_posTuple[0]
            word_posTuple = stem_posTuple[1]
            assert isinstance(word_stem, string_types)
            assert isinstance(word_posTuple, tuple)

            logger.debug(u'word_stem:{} word_pos:{}'.format(word_stem, ' '.join(word_posTuple)))

    def test_stopwords(self):
        stopword = [u'ＡＶ', u'女優']
        logger.debug (u'Stopwords Filtering Test. Stopwords is {}'.format(u','.join(stopword)))
        test_sentence = u"紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        juman_wrapper = JumanWrapper()
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
            assert isinstance(word_stem, string_types)
            assert isinstance(word_posTuple, tuple)

            logger.debug(u'word_stem:{} word_pos:{}'.format(word_stem, ' '.join(word_posTuple)))
            if word_stem in stopword: check_flag = False
        assert check_flag

    def test_juman_server_mode(self):
        ### test with server mode ###

        ### Attention: this method causes Error if you don't start JUMAN SERVER mode ###
        test_sentence = u"紗倉 まな（さくら まな、1993年3月23日 - ）は、日本のAV女優。"
        juman_wrapper = JumanWrapper(server='localhost', port=32000)
        token_objects = juman_wrapper.tokenize(sentence=test_sentence,
                                               return_list=False,
                                               is_feature=True)
        self.assertTrue(isinstance(token_objects, TokenizedSenetence))


        list_tokens = juman_wrapper.tokenize(sentence=test_sentence,
                                               return_list=True,
                                               is_feature=True)
        self.assertTrue(isinstance(list_tokens, list))



if __name__ == '__main__':
    unittest.main()