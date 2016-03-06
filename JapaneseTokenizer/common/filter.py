#! -*- coding: utf-8 -*-
from ..datamodels import TokenizedSenetence, TokenizedResult, FilteredObject
__author__ = 'kensuke-mi'


def __is_sotpwords(token, stopwords):
    """This function filters out stopwords. If token is in stopwords list, return True; else return False
    :param token:
    :param stopwords:
    :return:
    """
    if token in stopwords:
        return True
    else:
        return False


def __is_valid_pos(pos_tuple, valid_pos):
    """This function checks token's pos is with in POS set that user specified.
    If token meets all conditions, Return True; else return False
    :param pos_tuple:
    :param valid_pos:
    :return:
    """
    bool_list =[
        True
        for pos
        in valid_pos
        if set(pos).issubset(set(pos_tuple))
    ]
    if list(set(bool_list)) == [True]:
        return True
    else:
        return False


def filter_words(tokenized_obj, valid_pos, stopwords):
    """This function filter token that user don't want to take.
    Condition is stopword and pos.
    :param tokenized_obj:
    :param valid_pos:
    :param stopwords:
    :return:
    """
    assert isinstance(tokenized_obj, TokenizedSenetence)
    assert isinstance(valid_pos, list)
    assert isinstance(stopwords, list)

    filtered_tokens = []
    for token_obj in tokenized_obj.tokenized_objects:
        assert isinstance(token_obj, TokenizedResult)
        res_stopwords = __is_sotpwords(token_obj.word_surface, stopwords)
        res_pos_condition = __is_valid_pos(token_obj.tuple_pos, valid_pos)

        # case1: only pos filtering is ON
        if valid_pos != [] and stopwords == []:
            if res_pos_condition: filtered_tokens.append(token_obj)
        # case2: obly stopwords filtering is ON
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
