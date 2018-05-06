#! -*- coding: utf-8 -*-

"""This module is supposed to be called from python3.x only.
Because Sudachi-py does not work in python2.x
"""

# core module
from JapaneseTokenizer.object_models import WrapperBase
from JapaneseTokenizer.common.text_preprocess import normalize_text
from JapaneseTokenizer import init_logger
from JapaneseTokenizer.datamodels import TokenizedResult, TokenizedSenetence, FilteredObject
# else
import sys
import os
import logging
import subprocess
import six
from six import text_type
# typing
from typing import List, Dict, Tuple, Union, TypeVar, Callable
ContentsTypes = TypeVar('T')

__author__ = 'kensuke-mi'

logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
python_version = sys.version_info

try:
    import SudachiPy
except ImportError:
    logger.warning(msg='sudachipy is not ready to use. Install first if you would like to use sudachipy wrapper.')

if six.PY2:
    logger.warning(msg='sudachi wrapper does not work in python2.x environment.')

try:
    import neologdn
    is_neologdn_valid = True
except:
    logger.warning("neologdn package is not installed yet. You could not call neologd dictionary.")
    is_neologdn_valid = False


class SudachiWrapper(WrapperBase):
    def __init__(self, dictType, pathUserDictCsv='', path_mecab_config=None, string_encoding='utf-8'):
        """* What you can do
        """
        # type: (text_type, text_type, text_type, text_type)->None
        pass

    def __feature_parser(self, uni_feature, word_surface):
        """
        Parse the POS feature output by Mecab
        :param uni_feature unicode:
        :return ( (pos1, pos2, pos3), word_stem ):
        """
        list_feature_items = uni_feature.split((','))
        # if word has no feature at all
        if len(list_feature_items)==1: return ('*'), ('*')

        pos1 = list_feature_items[0]
        pos2 = list_feature_items[1]
        pos3 = list_feature_items[2]
        tuple_pos = ( pos1, pos2, pos3 )

        # if without constraint(output is normal mecab dictionary like)
        if len(list_feature_items) == 9:
            word_stem = list_feature_items[6]
        # if with constraint(output format depends on Usedict.txt)
        else:
            word_stem = word_surface

        return tuple_pos, word_stem

    def __postprocess_analyzed_result(self, string_mecab_parsed_result, is_feature, is_surface):
        """Extract surface word and feature from analyzed lines.
        Extracted results are returned with list, whose elements are TokenizedResult class
        [TokenizedResult]
        """
        # type: (text_type,bool,bool)->List[TokenizedResult]
        assert isinstance(string_mecab_parsed_result, str)
        check_tab_separated_line = lambda x: True if '\t' in x else False

        tokenized_objects = [
            self.__result_parser(analyzed_line=analyzed_line,
                                 is_feature=is_feature,
                                 is_surface=is_surface)
            for analyzed_line in string_mecab_parsed_result.split('\n')
            if not analyzed_line=='EOS' and check_tab_separated_line(analyzed_line)
        ]

        assert isinstance(tokenized_objects, list)
        return tokenized_objects

    def __result_parser(self, analyzed_line, is_feature, is_surface):
        """Extract surface word and feature from analyzed line.
        Extracted elements are returned with TokenizedResult class
        """
        # type: (text_type,bool,bool)->TokenizedResult
        assert isinstance(analyzed_line, str)
        assert isinstance(is_feature, bool)
        assert isinstance(is_surface, bool)

        surface, features = analyzed_line.split('\t', 1)
        tuple_pos, word_stem = self.__feature_parser(features, surface)
        tokenized_obj = TokenizedResult(
            node_obj=None,
            analyzed_line=analyzed_line,
            tuple_pos=tuple_pos,
            word_stem=word_stem,
            word_surface=surface,
            is_feature=is_feature,
            is_surface=is_surface
        )
        return tokenized_obj

    def tokenize(self, sentence,
                 normalized=True,
                 is_feature=False,
                 is_surface=False,
                 return_list=False,
                 func_normalizer=normalize_text):
        """* What you can do
        - Call mecab tokenizer, and return tokenized objects

        """
        # type: (text_type, bool, bool, bool, bool, Callable[[str], str])->Union[List[str], TokenizedSenetence]
        if six.PY2 and isinstance(sentence, str):
            sentence = sentence.decode(self.string_encoding)
        else:
            pass

        ### decide normalization function depending on dictType
        if func_normalizer is None and self._dictType == 'neologd' and is_neologdn_valid:
            normalized_sentence = neologdn.normalize(sentence)
        elif func_normalizer is None and self._dictType == 'neologd' and is_neologdn_valid == False:
            raise Exception("You could not call neologd dictionary bacause you do NOT install the package neologdn.")
        elif func_normalizer == normalize_text:
            normalized_sentence = normalize_text(sentence, dictionary_mode=self._dictType)
        elif func_normalizer is None:
            normalized_sentence = sentence
        else:
            normalized_sentence = func_normalizer(sentence)

        # don't delete this variable. The variable "encoded_text" protects sentence from deleting
        if six.PY2:
            encoded_text = normalized_sentence.encode(self.string_encoding)
        else:
            encoded_text = normalized_sentence

        if six.PY2:
            tokenized_objects = []
            node = self.mecabObj.parseToNode(encoded_text)
            node = node.next
            while node.next is not None:
                word_surface = node.surface.decode(self.string_encoding)

                tuple_pos, word_stem = self.__feature_parser(node.feature.decode(self.string_encoding), word_surface)

                tokenized_obj = TokenizedResult(
                    node_obj=node,
                    tuple_pos=tuple_pos,
                    word_stem=word_stem,
                    word_surface=word_surface,
                    is_feature=is_feature,
                    is_surface=is_surface
                )
                tokenized_objects.append(tokenized_obj)
                node = node.next

            tokenized_sentence = TokenizedSenetence(
                sentence=sentence,
                tokenized_objects=tokenized_objects)
        else:
            parsed_result = self.mecabObj.parse(encoded_text)
            tokenized_objects = self.__postprocess_analyzed_result(
                string_mecab_parsed_result=parsed_result,
                is_feature=is_feature,
                is_surface=is_surface
            )
            tokenized_sentence = TokenizedSenetence(
                sentence=sentence,
                tokenized_objects=tokenized_objects
            )  # type: TokenizedSenetence

        if return_list:
            return tokenized_sentence.convert_list_object()
        else:
            return tokenized_sentence

    def filter(self, parsed_sentence, pos_condition=None, stopwords=None):
        # type: (TokenizedSenetence, List[Tuple[str,...]], List[str]) -> FilteredObject
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))
        return parsed_sentence.filter(pos_condition, stopwords)