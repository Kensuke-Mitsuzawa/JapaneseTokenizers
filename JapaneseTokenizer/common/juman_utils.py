from JapaneseTokenizer.datamodels import TokenizedResult, TokenizedSenetence
from typing import Tuple
import pyknp
from six import text_type

"""These functions are for utilization of Juman"""


def extract_morphological_information(mrph_object, is_feature, is_surface):
    # type: (pyknp.Morpheme, bool, bool) -> TokenizedResult
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


def feature_parser(uni_feature, word_surface):
    # type: (text_type, text_type) -> Tuple[Tuple[text_type, text_type, text_type], text_type]
    """
    Parse the POS feature output by Mecab
    :param uni_feature unicode:
    :return ( (pos1, pos2, pos3), word_stem ):
    """
    list_feature_items = uni_feature.split(',')
    # if word has no feature at all
    if len(list_feature_items) == 1: return ('*'), ('*')

    pos1 = list_feature_items[0]
    pos2 = list_feature_items[1]
    pos3 = list_feature_items[2]
    tuple_pos = (pos1, pos2, pos3)

    # if without constraint(output is normal mecab dictionary like)
    if len(list_feature_items) == 9:
        word_stem = list_feature_items[6]
    # if with constraint(output format depends on Usedict.txt)
    else:
        word_stem = word_surface

    return tuple_pos, word_stem
