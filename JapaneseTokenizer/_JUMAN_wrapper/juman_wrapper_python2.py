# -*- coding: utf-8 -*-
from JapaneseTokenizer.common import text_preprocess
from JapaneseTokenizer.datamodels import FilteredObject, TokenizedResult, TokenizedSenetence
from JapaneseTokenizer.common import filter
from future.utils import string_types
import logging
import sys
__author__ = 'kensuke-mi'

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")
python_version = sys.version_info

try:
    import pyknp
except ImportError:
    logging.error(msg='pyknp is not ready to use. Check your installing log.')


class JumanWrapper:
    def __init__(self, command='juman', server=None, port=32000, timeout=30):
        self.juman = pyknp.Juman(command=command, server=server, port=port, timeout=timeout)

    def __extract_morphological_information(self, mrph_object, is_feature, is_surface):
        """This method extracts morphlogical information from token object.
        """
        assert isinstance(mrph_object, pyknp.Morpheme)
        assert isinstance(is_feature, bool)
        assert isinstance(is_surface, bool)

        surface = mrph_object.midasi
        word_stem = mrph_object.genkei

        tuple_pos = (mrph_object.hinsi, mrph_object.bunrui)

        misc_info = {
            'katuyou1': mrph_object.katuyou1,
            'katuyou2': mrph_object.katuyou2,
            'imis': mrph_object.imis,
            'repname': mrph_object.repname
        }

        token_object = TokenizedResult(
            node_obj=None,
            tuple_pos=tuple_pos,
            word_stem=word_stem,
            word_surface=surface,
            is_feature=is_feature,
            is_surface=is_surface,
            misc_info=misc_info
        )

        return token_object


    def call_juman_tokenize_api(self, sentence):
        """This method calls pyknp.juman.analysis
        Return object is `MList`

        :rtype: pyknp.MList
        """
        result = self.juman.analysis(sentence)
        assert isinstance(result, pyknp.MList)

        return result


    def tokenize(self, sentence, normalize=True, is_feature=False, is_surface=False, return_list=True):
        """This method returns tokenized result.
        If return_list==True(default), this method returns list whose element is tuple consisted with word_stem and POS.
        If return_list==False, this method returns TokenizedSenetence object.

        :param sentence: input sentence. unicode
        :param normalize: boolean flag to make string normalization before tokenization
        :param is_feature:
        :param is_surface:
        :param return_list:
        :return:
        """
        assert isinstance(normalize, bool)
        assert isinstance(sentence, string_types)
        if normalize:
            normalized_sentence = text_preprocess.normalize_text(sentence, dictionary_mode='ipadic')
        else:
            normalized_sentence = sentence

        result = self.juman.analysis(normalized_sentence)
        token_objects = [
            self.__extract_morphological_information(
                mrph_object=morph_object,
                is_surface=is_surface,
                is_feature=is_feature
            )
            for morph_object in result]

        if return_list:
            tokenized_objects = TokenizedSenetence(
                sentence=sentence,
                tokenized_objects=token_objects
            )
            return tokenized_objects.convert_list_object()
        else:
            tokenized_objects = TokenizedSenetence(
                sentence=sentence,
                tokenized_objects=token_objects)

            return tokenized_objects

    def convert_str(self, p_c_tuple):
        converted = []
        for item in p_c_tuple:
            if isinstance(item, str): converted.append(item)
            else: converted.append(item)
        return converted

    def __check_pos_condition_str(self, pos_condistion):
        assert isinstance(pos_condistion, list)
        # [ ('', '', '') ]

        return [
            tuple(self.convert_str(p_c_tuple))
            for p_c_tuple
            in pos_condistion
        ]

    def filter(self, parsed_sentence, pos_condition=None, stopwords=None):
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))

        if isinstance(stopwords, type(None)):
            s_words = []
        else:
            s_words = stopwords

        if isinstance(pos_condition, type(None)):
            p_condition = []
        else:
            p_condition = self.__check_pos_condition_str(pos_condition)

        filtered_object = filter.filter_words(
            tokenized_obj=parsed_sentence,
            valid_pos=p_condition,
            stopwords=s_words
        )
        assert isinstance(filtered_object, FilteredObject)

        return filtered_object
