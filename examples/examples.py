#! -*- coding: utf-8 -*-
import sys
import os
from JapaneseTokenizer import JumanWrapper
from JapaneseTokenizer import JumanppWrapper
from JapaneseTokenizer import MecabWrapper
from JapaneseTokenizer import KyteaWrapper
from JapaneseTokenizer.datamodels import TokenizedResult
from JapaneseTokenizer import init_logger
import logging
import socket
import six
logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
__author__ = 'kensuke-mi'
logger.setLevel(logging.DEBUG)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# for python2.x

def basic_example():
    # ========================================================
    # TOKENIZE
    # ========================================================
    if six.PY2:
        # input is `unicode` type(in python2x)
        sentence = u'テヘランは、西アジア、イランの首都でありかつテヘラン州の州都。人口12,223,598人。都市圏人口は13,413,348人に達する。'
    elif six.PY3:
        sentence = 'テヘランは、西アジア、イランの首都でありかつテヘラン州の州都。人口12,223,598人。都市圏人口は13,413,348人に達する。'
    else:
        raise Exception()

    # make MecabWrapper object
    # you can choose from "neologd", "all", "ipadic", "user", "", None
    # "ipadic" and "" is equivalent
    mecab_wrapper = MecabWrapper(dictType="neologd")
    juman_wrapper = JumanWrapper()
    jumanpp_wrapper = JumanppWrapper()
    #kytea_wrapper = KyteaWrapper()

    # tokenize sentence into list of token.
    # with is_feature=True, you get part-of-speech tag also. in this case, you get tuple ( token, (part-of-speech-tags) )
    # with is_surface=True, you get surface form of token (in other words, not normalized token)
    seq_tokens_mecab = mecab_wrapper.tokenize(sentence=sentence, is_feature=False, is_surface=False).convert_list_object()
    seq_tokens_juman = juman_wrapper.tokenize(sentence=sentence, is_feature=False, is_surface=False).convert_list_object()
    seq_tokens_jumanpp = jumanpp_wrapper.tokenize(sentence=sentence, is_feature=False, is_surface=False).convert_list_object()
    #seq_tokens_kytea = kytea_wrapper.tokenize(sentence=sentence, is_feature=True, is_surface=False).convert_list_object()

    logger.debug(seq_tokens_mecab)
    logger.debug(seq_tokens_juman)
    logger.debug(seq_tokens_jumanpp)
    #logger.debug(seq_tokens_kytea)

def filtering_example():
    if six.PY2:
        # input is `unicode` type(in python2x)
        sentence = u'テヘランは、西アジア、イランの首都でありかつテヘラン州の州都。人口12,223,598人。都市圏人口は13,413,348人に達する。'
        stopwords = [u'テヘラン']
        pos_condition_ipadic = [(u'名詞', u'固有名詞'), (u'名詞', u'一般')]
        pos_condition_juman = [(u'名詞', u'固有名詞'), (u'名詞', u'普通名詞')]
        pos_condition_kytea = [(u'名詞',)]
    elif six.PY3:
        sentence = 'テヘランは、西アジア、イランの首都でありかつテヘラン州の州都。人口12,223,598人。都市圏人口は13,413,348人に達する。'
        stopwords = ['テヘラン']
        pos_condition_ipadic = [('名詞', '固有名詞'), ('名詞', '一般')]
        pos_condition_juman = [('名詞', '固有名詞'), ('名詞', '普通名詞')]
        pos_condition_kytea = [('名詞',)]
    else:
        raise Exception()

    # ========================================================
    # FILTERING
    # ========================================================
    # you can filter tokens by stopwords or POS conditions
    # stopword is list objetc

    mecab_wrapper = MecabWrapper(dictType="neologd")
    juman_wrapper = JumanWrapper()
    jumanpp_wrapper = JumanppWrapper()
    #kytea_wrapper = KyteaWrapper()
    seq_tokens_mecab = mecab_wrapper.tokenize(sentence=sentence, is_feature=False, is_surface=False).filter(pos_condition=pos_condition_ipadic,stopwords=stopwords).convert_list_object()
    seq_tokens_juman = juman_wrapper.tokenize(sentence=sentence, is_feature=False, is_surface=False).filter(pos_condition=pos_condition_juman, stopwords=stopwords).convert_list_object()
    seq_tokens_jumanpp = jumanpp_wrapper.tokenize(sentence=sentence, is_feature=False, is_surface=False).filter(pos_condition=pos_condition_juman, stopwords=stopwords).convert_list_object()
    #seq_tokens_kytea = kytea_wrapper.tokenize(sentence=sentence, is_feature=True, is_surface=False).filter(pos_condition=pos_condition_kytea, stopwords=stopwords).convert_list_object()

    logger.debug(seq_tokens_mecab)
    logger.debug(seq_tokens_juman)
    logger.debug(seq_tokens_jumanpp)
    #logger.debug(seq_tokens_kytea)


def advanced_example_mecab():
    if six.PY2:
        sentence = u'テヘランは、西アジア、イランの首都でありかつテヘラン州の州都。人口12,223,598人。都市圏人口は13,413,348人に達する。'
    elif six.PY3:
        sentence = 'テヘランは、西アジア、イランの首都でありかつテヘラン州の州都。人口12,223,598人。都市圏人口は13,413,348人に達する。'
    else:
        raise Exception()

    # ========================================================
    # USE YOUE OWN DICTIONARY
    # with your own dictionary, you can force Mecab to make some word into one token
    # ========================================================
    # make your own "user dictionary" with CSV file
    # To know more about this file, see this page(sorry, Japanese only) https://mecab.googlecode.com/svn/trunk/mecab/doc/dic.html
    example_user_dict = "userdict.csv"

    # set dictType='user' or dictType='all' and set pathUserDictCsv
    tokenized_obj = MecabWrapper(dictType='user', pathUserDictCsv=example_user_dict).tokenize(sentence)

    for token_obj in tokenized_obj.tokenized_objects:
        assert isinstance(token_obj, TokenizedResult)
        if six.PY2 and token_obj.word_stem == u'ペルシア語':
            logger.debug(token_obj.word_stem)
        elif six.PY3 and token_obj.word_stem == 'ペルシア語':
            logger.debug(token_obj.word_stem)

        ## TokenizedResult class has attributes of tokenized result ##
        token_obj.analyzed_line
        token_obj.word_surface
        token_obj.word_stem
        token_obj.tuple_pos


def advanced_example_juman():
    if six.PY2:
        sentence = u'テヘランは、西アジア、イランの首都でありかつテヘラン州の州都。人口12,223,598人。都市圏人口は13,413,348人に達する。'
        pos_condition = [(u'名詞',)]
    elif six.PY3:
        sentence = 'テヘランは、西アジア、イランの首都でありかつテヘラン州の州都。人口12,223,598人。都市圏人口は13,413,348人に達する。'
        pos_condition = [('名詞',)]
    else:
        raise Exception()

    ### You can call juman with server mode. You must start JUMAN as server mode beforehand ###
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST='localhost'
    PORT = 32000
    try:
        s.connect((HOST, PORT))
        s.close()
        juman_wrapper = JumanWrapper(server=HOST, port=PORT)
        tokens_list = juman_wrapper.tokenize(sentence, return_list=False).filter(pos_condition=pos_condition).convert_list_object()
        assert isinstance(tokens_list, list)
    except:
        logger.info(msg='Juman server is not running. Skip it.')


if __name__ == "__main__":
    basic_example()
    filtering_example()
    advanced_example_mecab()
    advanced_example_juman()