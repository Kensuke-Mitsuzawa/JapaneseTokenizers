#! -*- coding: utf-8 -*-
from MeCab import Node
from typing import List, Union, Any, Tuple, Dict
from future.utils import string_types, text_type
from JapaneseTokenizer.common import filter
import sys
__author__ = 'kensuke-mi'

python_version = sys.version_info


class TokenizedResult(object):
    def __init__(self, node_obj, tuple_pos, word_stem, word_surface,
                 is_feature=True, is_surface=False, misc_info=None, analyzed_line=None):
        # type: (Union[Node, None], Union[str, Tuple[str, ...], str, str, bool, bool, Union[None, Dict[str, Any]], str])->None
        assert isinstance(node_obj, (Node, type(None)))
        assert isinstance(tuple_pos, (str, string_types, tuple))
        assert isinstance(word_stem, (str, string_types))
        assert isinstance(word_surface, (str, string_types))
        assert isinstance(misc_info, (type(None), dict))

        self.node_obj = node_obj
        self.word_stem = word_stem
        self.word_surface = word_surface
        self.is_surface = is_surface
        self.is_feature = is_feature
        self.misc_info = misc_info
        self.analyzed_line = analyzed_line

        if isinstance(tuple_pos, tuple):
            self.tuple_pos = tuple_pos
        elif isinstance(tuple_pos, (str, string_types)):
            self.tuple_pos = ('*', )
        else:
            raise Exception('Error while parsing feature object. {}'.format(self.tuple_pos))


class TokenizedSenetence(object):
    def __init__(self, sentence, tokenized_objects):
        # type: (str, List[TokenizedResult]) -> None
        assert isinstance(sentence, (str, string_types))
        assert isinstance(tokenized_objects, list)

        self.sentence = sentence
        self.tokenized_objects = tokenized_objects

    def __extend_token_object(self, token_object):
        """This method creates dict object from token object.
        """
        assert isinstance(token_object, TokenizedResult)

        if token_object.is_feature == True:
            if token_object.is_surface == True:
                token = (token_object.word_surface, token_object.tuple_pos)
            else:
                token = (token_object.word_stem, token_object.tuple_pos)
        else:
            if token_object.is_surface == True:
                token = token_object.word_surface
            else:
                token = token_object.word_stem

        return token

    def convert_list_object(self):
        # type: () -> List[Union[str, Tuple[str,str]]]
        sentence_in_list_obj = [
            self.__extend_token_object(token_object)
            for token_object
            in self.tokenized_objects
        ]

        return sentence_in_list_obj

    def __convert_str(self, p_c_tuple):
        # type: (Tuple[str, ...]) -> List[str]
        converted = []
        for item in p_c_tuple:
            if isinstance(item, str):
                converted.append(item)
            else:
                converted.append(item)
        return converted

    def __check_pos_condition_str(self, pos_condistion):
        # type: (List[Tuple[str, ...]]) -> List[Tuple[str, ...]]
        """* What you can do
        - Check your pos condition is correct or NOT

        * Input
        - pos_condistion
            - List of Tuple which has POS element to keep.
            - Keep in your mind, each tokenizer has different POS structure.
            >>> [('名詞', '固有名詞'), ('動詞', )]
        """
        assert isinstance(pos_condistion, list)
        # [ ('', '', '') ]

        return [
            tuple(self.__convert_str(p_c_tuple))
            for p_c_tuple
            in pos_condistion]

    def filter(self, pos_condition=None, stopwords=None):
        # type: (List[Tuple[str,...]], List[str]) ->  FilteredObject
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
            tokenized_obj=self,
            valid_pos=p_condition,
            stopwords=s_words
        )
        assert isinstance(filtered_object, FilteredObject)

        return filtered_object


class FilteredObject(TokenizedSenetence):
    def __init__(self, sentence, tokenized_objects, pos_condition, stopwords):
        # type: (str, List[TokenizedResult], List[str, ...], List[str]) -> None
        super(FilteredObject, self).__init__(
            sentence=sentence,
            tokenized_objects=tokenized_objects
        )
        self.pos_condition=pos_condition
        self.stopwords=stopwords




