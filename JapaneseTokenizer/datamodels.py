#! -*- coding: utf-8 -*-
# normalize module #
from JapaneseTokenizer.common.text_preprocess import normalize_text, denormalize_text
# datemodels #
from MeCab import Node
# typing #
from typing import List, Union, Any, Tuple, Dict, Callable, Optional
from future.utils import text_type, string_types
import sys
import six
__author__ = 'kensuke-mi'

python_version = sys.version_info


def __is_sotpwords(token, stopwords):
    """This function filters out stopwords. If token is in stopwords list, return True; else return False
    """
    if token in stopwords:
        return True
    else:
        return False


def __is_valid_pos(pos_tuple, valid_pos):
    # type: (Tuple[text_type,...],List[Tuple[text_type,...]])->bool
    """This function checks token's pos is with in POS set that user specified.
    If token meets all conditions, Return True; else return False
    """
    def is_valid_pos(valid_pos_tuple):
        # type: (Tuple[text_type,...])->bool
        length_valid_pos_tuple = len(valid_pos_tuple)
        if valid_pos_tuple == pos_tuple[:length_valid_pos_tuple]:
            return True
        else:
            return False

    seq_bool_flags = [is_valid_pos(valid_pos_tuple) for valid_pos_tuple in valid_pos]

    if True in set(seq_bool_flags):
        return True
    else:
        return False


def filter_words(tokenized_obj, valid_pos, stopwords, check_field_name='stem'):
    # type: (TokenizedSenetence, List[Tuple[text_type,...]], List[text_type],text_type) -> FilteredObject
    """This function filter token that user don't want to take.
    Condition is stopword and pos.

    * Input
    - valid_pos
        - List of Tuple which has POS element to keep.
        - Keep in your mind, each tokenizer has different POS structure.
         >>> [('名詞', '固有名詞'), ('動詞', )]
    - stopwords
        - List of str, which you'd like to remove
        >>> ['残念', '今日']
    """
    assert isinstance(tokenized_obj, TokenizedSenetence)
    assert isinstance(valid_pos, list)
    assert isinstance(stopwords, list)

    filtered_tokens = []
    for token_obj in tokenized_obj.tokenized_objects:
        assert isinstance(token_obj, TokenizedResult)
        if check_field_name=='stem':
            res_stopwords = __is_sotpwords(token_obj.word_stem, stopwords)
        else:
            res_stopwords = __is_sotpwords(token_obj.word_surface, stopwords)

        res_pos_condition = __is_valid_pos(token_obj.tuple_pos, valid_pos)

        # case1: only pos filtering is ON
        if valid_pos != [] and stopwords == []:
            if res_pos_condition: filtered_tokens.append(token_obj)
        # case2: only stopwords filtering is ON
        if valid_pos == [] and stopwords != []:
            if res_stopwords is False: filtered_tokens.append(token_obj)
        # case3: both condition is ON
        if valid_pos != [] and stopwords != []:
            if res_stopwords is False and res_pos_condition: filtered_tokens.append(token_obj)

    filtered_object = FilteredObject(
        sentence=tokenized_obj.sentence,
        tokenized_objects=filtered_tokens,
        pos_condition=valid_pos,
        stopwords=stopwords
    )

    return filtered_object


class TokenizedResult(object):
    def __init__(self,
                 node_obj,
                 tuple_pos,
                 word_stem,
                 word_surface,
                 is_feature=True,
                 is_surface=False,
                 misc_info=None,
                 analyzed_line=None):
        # type: (Optional[Node], Tuple[text_type, ...], str, str, bool, bool, Optional[Dict[str, Any]], str)->None
        assert isinstance(node_obj, (Node, type(None)))
        assert isinstance(tuple_pos, (string_types, tuple))
        assert isinstance(word_stem, (string_types))
        assert isinstance(word_surface, text_type)
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
        elif isinstance(tuple_pos, string_types):
            self.tuple_pos = ('*', )
        else:
            raise Exception('Error while parsing feature object. {}'.format(tuple_pos))


class TokenizedSenetence(object):
    def __init__(self, sentence, tokenized_objects, string_encoding='utf-8'):
        # type: (text_type, List[TokenizedResult], text_type)->None
        """* Parameters
        - sentence: sentence
        - tokenized_objects: list of TokenizedResult object
        - string_encoding: Encoding type of string type. This option is used only under python2.x
        """
        assert isinstance(sentence, text_type)
        assert isinstance(tokenized_objects, list)

        self.sentence = sentence
        self.tokenized_objects = tokenized_objects
        self.string_encoding = string_encoding


    def __extend_token_object(self, token_object,
                              is_denormalize=True,
                              func_denormalizer=denormalize_text):
        # type: (TokenizedResult,bool,Callable[[str],str])->Tuple
        """This method creates dict object from token object.
        """
        assert isinstance(token_object, TokenizedResult)

        if is_denormalize:
            if token_object.is_feature == True:
                if token_object.is_surface == True:
                    token = (func_denormalizer(token_object.word_surface), token_object.tuple_pos)
                else:
                    token = (func_denormalizer(token_object.word_stem), token_object.tuple_pos)
            else:
                if token_object.is_surface == True:
                    token = func_denormalizer(token_object.word_surface)
                else:
                    token = func_denormalizer(token_object.word_stem)
        else:
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

    def convert_list_object(self,
                            is_denormalize=True,
                            func_denormalizer=denormalize_text):
        # type: (bool,Callable[[str],str])->List[Union[str, Tuple[str,...]]]
        """* What you can do
        - You extract string object from TokenizedResult object

        * Args
        - is_denormalize: boolen object. True; it makes denormalize string
        - func_denormalizer: callable object. de-normalization function.
        """
        sentence_in_list_obj = [
            self.__extend_token_object(token_object,is_denormalize,func_denormalizer)
            for token_object
            in self.tokenized_objects
        ]

        return sentence_in_list_obj

    def __convert_string_type(self, p_c_tuple):
        # type: (Tuple[text_type,...])->Tuple[text_type]
        """* What you can do
        - it normalizes string types into str
        """
        if not isinstance(p_c_tuple, tuple):
            raise Exception('Pos condition expects tuple of string. However = {}'.format(p_c_tuple))

        converted = [text_type] * len(p_c_tuple)
        for i, pos_element in enumerate(p_c_tuple):
            if six.PY2 and isinstance(pos_element, str):
                """str into unicode if python2.x"""
                converted[i] = pos_element.decode(self.string_encoding)
            elif six.PY2 and isinstance(pos_element, text_type):
                converted[i] = pos_element
            elif six.PY3:
                converted[i] = pos_element
            else:
                raise Exception()

        return tuple(converted)

    def __check_pos_condition(self, pos_condistion):
        # type: (List[Tuple[text_type, ...]])->List[Tuple[text_type, ...]]
        """* What you can do
        - Check your pos condition
        - It converts character type into unicode if python version is 2.x
        """
        assert isinstance(pos_condistion, list)

        return [self.__convert_string_type(p_c_tuple) for p_c_tuple in pos_condistion]

    def filter(self,
               pos_condition=None,
               stopwords=None,
               is_normalize=True,
               func_normalizer=normalize_text,
               check_field_name='stem'):
        # type: (List[Tuple[text_type,...]], List[text_type], bool, Callable[[text_type], text_type],text_type)->FilteredObject
        """* What you can do
        - It filters out token which does NOT meet the conditions (stopwords & part-of-speech tag)
        - Under python2.x, pos_condition & stopwords are converted into unicode type.

        * Parameters
        - pos_condition: list of part-of-speech(pos) condition. The pos condition is tuple is variable length.
        You can specify hierarchical structure of pos condition with variable tuple.
        The hierarchy of pos condition follows definition of dictionary.
            - For example, in mecab you can take words with 名詞 if ('名詞',)
            - For example, in mecab you can take words with 名詞-固有名詞 if ('名詞', '固有名詞')
        - stopwords: list of word which you would like to remove
        - is_normalize: Boolean flag for normalize stopwords.
        - func_normalizer: Function object for normalization. The function object must be the same one as when you use tokenize.
        - check_field_name: Put field name to check if stopword or NOT. Kytea does not have stem form of word, put 'surface' instead.

        * Example
        >>> pos_condition = [('名詞', '一般'), ('形容詞', '自立'), ('助詞', '格助詞', '一般')]
        >>> stopwords = ['これ', 'それ']
        """
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))

        if stopwords is None:
            s_words = []
        elif six.PY2 and all((isinstance(s, str) for s in stopwords)):
            """under python2.x, from str into unicode"""
            if is_normalize:
                s_words = [func_normalizer(s.decode(self.string_encoding)) for s in stopwords]
            else:
                s_words = [s.decode(self.string_encoding) for s in stopwords]
        else:
            if is_normalize:
                s_words = [func_normalizer(s) for s in stopwords]
            else:
                s_words = stopwords


        if pos_condition is None:
            p_condition = []
        else:
            p_condition = self.__check_pos_condition(pos_condition)

        filtered_object = filter_words(
            tokenized_obj=self,
            valid_pos=p_condition,
            stopwords=s_words,
            check_field_name=check_field_name
        )
        assert isinstance(filtered_object, FilteredObject)

        return filtered_object


class FilteredObject(TokenizedSenetence):
    def __init__(self, sentence, tokenized_objects, pos_condition, stopwords):
        # type: (str, List[TokenizedResult], List[str, ...], List[str])->None
        super(FilteredObject, self).__init__(
            sentence=sentence,
            tokenized_objects=tokenized_objects
        )
        self.pos_condition=pos_condition
        self.stopwords=stopwords




