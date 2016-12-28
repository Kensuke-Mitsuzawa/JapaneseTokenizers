#! -*- coding: utf-8 -*-
import sys
import os
import logging
import subprocess
import MeCab
from typing import List, Union, Any, Tuple, Callable
from JapaneseTokenizer.object_models import WrapperBase
from JapaneseTokenizer.common.text_preprocess import normalize_text
from JapaneseTokenizer import init_logger
from ..datamodels import TokenizedResult, TokenizedSenetence, FilteredObject
from future.utils import string_types
__author__ = 'kensuke-mi'

logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
python_version = sys.version_info


class MecabWrapper(WrapperBase):
    def __init__(self, dictType, pathUserDictCsv='', path_mecab_config='/usr/local/bin/', osType=''):
        # type: (str, str, str, str)->None
        assert dictType in ["neologd", "all", "ipaddic", "user", ""]
        if dictType == 'all' or dictType == 'user': assert os.path.exists(pathUserDictCsv)
        self._path_mecab_config = path_mecab_config
        if osType != '':
            logger.warn('osType argument is abolished. This argument might be unavailable in next version.')

        self._dictType = dictType
        self._pathUserDictCsv = pathUserDictCsv
        self._mecab_dictionary_path = self.__check_mecab_dict_path()

        logger.info("mecab dictionary path is detected under {}".format(self._mecab_dictionary_path))

        self.mecabObj = self.__CallMecab()


    def __check_mecab_dict_path(self):
        """check path to dict of Mecab in system environment
        """

        mecab_dic_cmd = "echo `{} --dicdir`".format(os.path.join(self._path_mecab_config, 'mecab-config'))

        try:
            path_mecab_dict = subprocess.check_output( mecab_dic_cmd, shell=True  ).strip('\n')
        except subprocess.CalledProcessError:
            logger.error("{}".format(mecab_dic_cmd))
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to execute mecab-config command")
        if path_mecab_dict == '':
            raise SystemError(
                'mecab dictionary path is not found with following command: {} You are not able to use additional dictionary. Still you are able to call mecab default dictionary'.format(mecab_dic_cmd)
            )

        return path_mecab_dict


    def __check_mecab_libexe(self):

        mecab_libexe_cmd = "echo `{} --libexecdir`".format(os.path.join(self._path_mecab_config, 'mecab-config'))

        try:
            path_mecab_libexe = subprocess.check_output( mecab_libexe_cmd, shell=True  ).strip('\n')
        except subprocess.CalledProcessError:
            logger.error("{}".format(mecab_libexe_cmd))
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to execute mecab-config --libexecdir")
        if path_mecab_libexe == '':
            raise SystemError('Mecab config is not callable with following command: {} You are not able to compile your user dictionary. Still, you are able to use default mecab dictionary.'.format(mecab_libexe_cmd))

        return path_mecab_libexe


    def __CallMecab(self):
        """
        """
        if self._dictType == 'neologd':
            logger.debug('Use neologd additional dictionary')
            cmMecabInitialize = '-d {}'.format(os.path.join(self._mecab_dictionary_path, "mecab-ipadic-neologd"))

        elif self._dictType == 'all':
            logger.debug('Use neologd additional dictionary')
            pathUserDict = self.__CompileUserdict()
            cmMecabInitialize = '-u {} -d {}'.format(pathUserDict,
                                                     os.path.join(self._mecab_dictionary_path, "mecab-ipadic-neologd"))
        elif self._dictType == 'ipadic':
            logger.debug('Use ipadic additional dictionary')
            cmMecabInitialize = '-d {}'.format(os.path.join(self._mecab_dictionary_path, "ipadic"))

        elif self._dictType == 'user':
            logger.debug('Use User dictionary')
            pathUserDict = self.__CompileUserdict()
            cmMecabInitialize = '-u {}'.format(pathUserDict)

        else:
            logger.debug('Use no default dictionary')
            cmMecabInitialize = ''

        cmMecabCall = "-Ochasen {}".format(cmMecabInitialize)
        logger.debug(msg="mecab initialized with {}".format(cmMecabCall))

        try:
            mecabObj = MeCab.Tagger(cmMecabCall)
        except Exception as e:
            logger.error(e.args)
            logger.error(e.message)
            logger.error(e.args)
            logger.error("Possibly Path to userdict is invalid check the path")
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to initialize Mecab object")

        return mecabObj


    def __CompileUserdict(self):
        # 複合語辞書のコンパイルをする

        path_mecab_dict = self.__check_mecab_dict_path()
        path_mecab_libexe = self.__check_mecab_libexe()

        cmCompileDict = u'{0}/mecab-dict-index -d {1}/ipadic -u {2} -f utf-8 -t utf-8 {3} > /dev/null'.format(path_mecab_libexe,
                                                                                                            path_mecab_dict,
                                                                                                            self._pathUserDictCsv.replace("csv", "dict"),
                                                                                                            self._pathUserDictCsv)
        logger.debug(msg="compiling mecab user dictionary with: {}".format(cmCompileDict))
        try:
            subprocess.call( cmCompileDict , shell=True )
        except OSError as e:
            logger.error('type:' + str(type(e)))
            logger.error('args:' + str(e.args))
            logger.error('message:' + e.message)
            sys.exit('Failed to compile mecab userdict. System ends')

        return self._pathUserDictCsv.replace("csv", "dict")


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

    def tokenize(self, sentence,
                 normalized=True,
                 is_feature=False,
                 is_surface=False,
                 return_list=False,
                 func_normalizer=None):
        # type: (, str, bool, bool, bool, bool, Callable[[str], str])->Union[List[str], TokenizedSenetence]
        """* What you can do
        - Call mecab tokenizer, and return tokenized objects

        """
        ### decide normalization function depending on dictType
        if func_normalizer is None and self._dictType == 'neologd':
            normalized_sentence = normalize_text(sentence, dictionary_mode='neologd')
            normalized_sentence = normalized_sentence.replace(u'　', u'')
        elif func_normalizer is None:
            normalized_sentence = normalize_text(sentence)
            normalized_sentence = normalized_sentence.replace(u'　', u'')
        else:
            normalized_sentence = func_normalizer(sentence)

        assert isinstance(sentence, string_types)
        tokenized_objects = []

        # don't delete this variable. encoded_text protects sentence from deleting
        encoded_text = normalized_sentence.encode('utf-8')

        node = self.mecabObj.parseToNode(encoded_text)
        node = node.next
        while node.next is not None:

            word_surface = node.surface.decode('utf-8')

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

    def filter(self, parsed_sentence, pos_condition=None, stopwords=None):
        # type: (TokenizedSenetence, List[Tuple[str,...]], List[str]) -> FilteredObject
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))
        return parsed_sentence.filter(pos_condition, stopwords)