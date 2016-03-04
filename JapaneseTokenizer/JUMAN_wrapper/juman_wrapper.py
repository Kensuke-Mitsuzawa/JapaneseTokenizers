#! -*- coding: utf-8 -*-
import pyknp
import typing
import logging
import sys
__author__ = 'kensuke-mi'

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")
python_version = sys.version_info


class JumanWrapper:
    def __init__(self):
        self.juman = pyknp.Juman()



    def __feature_parser(self, uni_feature, word_surface):
        """
        Parse the POS feature output by Mecab
        :param uni_feature unicode:
        :return ( (pos1, pos2, pos3), word_stem ):
        """
        list_feature_items = uni_feature.split(u(','))
        # if word has no feature at all
        if len(list_feature_items)==1: return u('*'), u('*')

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


    def tokenize(self, sentence, is_feature=False, is_surface=False, return_list=True):
        """
        :param sentence:
        :param ins_mecab:
        :param list_stopword:
        :param list_pos_candidate:
        :return:  list [tuple (unicode, unicode)]
        """
        if python_version >= (3, 0, 0):
            assert isinstance(sentence, str)
        else:
            assert isinstance(sentence, unicode)

        tokenized_objects = []
        list_sentence_processed = []  # list to save word stem of posted contents
        normalized_sentence = normalize_text(sentence)

        # don't delete this variable. encoded_text protects sentence from deleting
        if python_version >= (3, 0, 0):
            encoded_text = normalized_sentence
        else:
            encoded_text = normalized_sentence.encode('utf-8')

        node = self.mecabObj.parseToNode(encoded_text)
        node = node.next
        while node.next is not None:


            if python_version >= (3, 0, 0):
                word_surface = node.surface
            else:
                word_surface = node.surface.decode('utf-8')

            if python_version >= (3,0,0):
                tuple_pos, word_stem = self.__feature_parser(node.feature, word_surface)
            else:
                tuple_pos, word_stem = self.__feature_parser(node.feature.decode('utf-8'), word_surface)

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
            tokenized_objects=tokenized_objects
        )

        if return_list:
            return tokenized_sentence.convert_list_object()
        else:
            return tokenized_sentence

    def __check_stopwords_str_typle(self, stopwords):
        assert isinstance(stopwords, list)
        convert_to_unicode = lambda input: u(input) if isinstance(s_word, str) else input

        return [
            convert_to_unicode(s_word)
            for s_word
            in stopwords
        ]

    def convert_str(self, p_c_tuple):
        converted = []
        for item in p_c_tuple:
            if isinstance(item, str): converted.append(u(item))
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
            s_words = self.__check_stopwords_str_typle(stopwords)

        if isinstance(pos_condition, type(None)):
            p_condition = []
        else:
            p_condition = self.__check_pos_condition_str(pos_condition)

        filtered_object = filter_words(
            tokenized_obj=parsed_sentence,
            valid_pos=p_condition,
            stopwords=s_words
        )
        assert isinstance(filtered_object, FilteredObject)

        return filtered_object





res = juman.analysis('今日は晴れです')

for mrph in res.mrph_list():
    print mrph.midasi