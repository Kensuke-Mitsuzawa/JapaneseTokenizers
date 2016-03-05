#! -*- coding: utf-8 -*-
from MeCab import Node
import sys
__author__ = 'kensuke-mi'

python_version = sys.version_info


if python_version >= (3, 0, 0):
    class TokenizedSenetence(object):

        def __init__(self, sentence, tokenized_objects):
            assert isinstance(sentence, (str))
            assert isinstance(tokenized_objects, list)

            self.sentence = sentence
            self.tokenized_objects = tokenized_objects

        def __extend_token_object(self, token_object):
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
            sentence_in_list_obj = [
                self.__extend_token_object(token_object)
                for token_object
                in self.tokenized_objects
            ]

            return sentence_in_list_obj


    class TokenizedResult(object):
        def __init__(self, analyzed_line, tuple_pos, word_stem, word_surface, is_feature=True, is_surface=False):
            assert isinstance(analyzed_line, str)
            assert isinstance(tuple_pos, (str, tuple))
            assert isinstance(word_stem, (str))
            assert isinstance(word_surface, (str))

            self.analyzed_line = analyzed_line
            self.word_stem = word_stem
            self.word_surface = word_surface
            self.is_surface = is_surface
            self.is_feature = is_feature

            if isinstance(tuple_pos, tuple):
                self.tuple_pos = tuple_pos
            elif isinstance(tuple_pos, (str)):
                self.tuple_pos = ('*', )
            else:
                raise Exception('Error while parsing feature object. {}'.format(self.tuple_pos))


    class FilteredObject(TokenizedSenetence):
        def __init__(self, sentence, tokenized_objects, pos_condition, stopwords):
            super(FilteredObject, self).__init__(
                sentence=sentence,
                tokenized_objects=tokenized_objects
            )
            self.pos_condition=pos_condition
            self.stopwords=stopwords

else:
    class TokenizedSenetence(object):
        def __init__(self, sentence, tokenized_objects):
            assert isinstance(sentence, (str, unicode))
            assert isinstance(tokenized_objects, list)

            self.sentence = sentence
            self.tokenized_objects = tokenized_objects

        def __extend_token_object(self, token_object):
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
            sentence_in_list_obj = [
                self.__extend_token_object(token_object)
                for token_object
                in self.tokenized_objects
            ]

            return sentence_in_list_obj


    class TokenizedResult(object):
        def __init__(self, node_obj, tuple_pos, word_stem, word_surface, is_feature=True, is_surface=False):
            assert isinstance(node_obj, Node)
            assert isinstance(tuple_pos, (str, unicode, tuple))
            assert isinstance(word_stem, (str, unicode))
            assert isinstance(word_surface, (str, unicode))

            self.node_obj = node_obj
            self.word_stem = word_stem
            self.word_surface = word_surface
            self.is_surface = is_surface
            self.is_feature = is_feature

            if isinstance(tuple_pos, tuple):
                self.tuple_pos = tuple_pos
            elif isinstance(tuple_pos, (str, unicode)):
                self.tuple_pos = ('*', )
            else:
                raise Exception('Error while parsing feature object. {}'.format(self.tuple_pos))


    class FilteredObject(TokenizedSenetence):
        def __init__(self, sentence, tokenized_objects, pos_condition, stopwords):
            super(FilteredObject, self).__init__(
                sentence=sentence,
                tokenized_objects=tokenized_objects
            )
            self.pos_condition=pos_condition
            self.stopwords=stopwords




