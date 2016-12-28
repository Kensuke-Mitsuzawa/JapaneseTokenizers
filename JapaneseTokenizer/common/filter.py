#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'
from JapaneseTokenizer.datamodels import TokenizedSenetence, TokenizedResult, FilteredObject

'''
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
    # type: (TokenizedSenetence, List[Tuple[str,...]], List[str]) -> FilteredObject
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

    return filtered_object'''
