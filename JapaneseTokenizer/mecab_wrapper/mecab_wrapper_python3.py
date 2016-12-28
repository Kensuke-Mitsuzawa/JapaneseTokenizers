#! -*- coding: utf-8 -*-
import sys
import os
import subprocess
import MeCab
import logging
from JapaneseTokenizer import init_logger
from JapaneseTokenizer.common.text_preprocess import normalize_text
from JapaneseTokenizer.object_models import WrapperBase
from JapaneseTokenizer.datamodels import TokenizedSenetence, TokenizedResult, FilteredObject
from typing import List, Dict, Tuple, Union, TypeVar, Callable
ContentsTypes = TypeVar('T')
__author__ = 'kensuke-mi'

logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")
python_version = sys.version_info


class MecabWrapper(WrapperBase):
    def __init__(self, dictType:str, pathUserDictCsv:str=None, path_mecab_config:str='/usr/local/bin/', osType:str=''):
        assert dictType in ["neologd", "all", "ipaddic", "user", ""]
        if dictType == 'all' or dictType == 'user': assert os.path.exists(pathUserDictCsv)
        self._path_mecab_config = path_mecab_config
        if osType != '':
            logger.warning('osType argument is abolished. This argument might be unavailable in next version.')

        self._osType = osType
        self._dictType = dictType
        self._pathUserDictCsv = pathUserDictCsv
        self._mecab_dictionary_path = self.__check_mecab_dict_path()
        logger.info("mecab dictionary path is detected under {}".format(self._mecab_dictionary_path))

        self.mecabObj = self.__CallMecab()


    def __check_mecab_dict_path(self)->str:
        """check path to dict of Mecab in system environment
        """
        mecab_dic_cmd = "echo `{} --dicdir`".format(os.path.join(self._path_mecab_config, 'mecab-config'))

        try:
            path_mecab_dict = subprocess.check_output( mecab_dic_cmd, shell=True  ).decode('utf-8').strip('\n')

        except subprocess.CalledProcessError:
            logger.error("{}".format(mecab_dic_cmd))
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to execute mecab-config command")

        if path_mecab_dict == '':
            raise SystemError(
                'mecab dictionary path is not found with following command: {} You are not able to use additional dictionary. Still you are able to call mecab default dictionary'.format(mecab_dic_cmd)
            )

        return path_mecab_dict


    def __check_mecab_libexe(self)->str:

        mecab_libexe_cmd = "echo `{} --libexecdir`".format(os.path.join(self._path_mecab_config, 'mecab-config'))

        try:
            path_mecab_libexe = subprocess.check_output( mecab_libexe_cmd, shell=True  ).decode('utf-8').strip('\n')

        except subprocess.CalledProcessError:
            logger.error("{}".format(mecab_libexe_cmd))
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to execute mecab-config --libexecdir")

        if path_mecab_libexe == '':
            raise SystemError('Mecab config is not callable with following command: {} You are not able to compile your user dictionary. Still, you are able to use default mecab dictionary.'.format(mecab_libexe_cmd))

        return path_mecab_libexe


    def __CallMecab(self)->MeCab:
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

        cmMecabCall = "{}".format(cmMecabInitialize)
        logger.debug(msg="mecab initialized with {}".format(cmMecabCall))

        try:
            mecabObj = MeCab.Tagger(cmMecabCall)
        except Exception as e:
            logger.error(e.args)
            logger.error("Possibly Path to userdict is invalid. Check the path")
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to initialize Mecab object")

        return mecabObj


    def __CompileUserdict(self)->str:
        # 複合語辞書のコンパイルをする

        path_mecab_dict = self.__check_mecab_dict_path()
        path_mecab_libexe = self.__check_mecab_libexe()


        cmCompileDict = '{0}/mecab-dict-index -d {1}/ipadic -u {2} -f utf-8 -t utf-8 {3} > /dev/null'.format(path_mecab_libexe,
                                                                                                            path_mecab_dict,
                                                                                                            self._pathUserDictCsv.replace("csv", "dict"),
                                                                                                            self._pathUserDictCsv)

        logger.debug(msg="compiling mecab user dictionary with: {}".format(cmCompileDict))
        try:
            subprocess.call( cmCompileDict , shell=True )
        except OSError as e:
            logger.error('type:' + str(type(e)))
            logger.error('args:' + str(e.args))
            sys.exit('Failed to compile mecab userdict. System ends')

        return self._pathUserDictCsv.replace("csv", "dict")


    def __feature_parser(self, uni_feature, word_surface):
        """
        Parse the POS feature output by Mecab
        :param uni_feature unicode:
        :return ( (pos1, pos2, pos3), word_stem ):
        """
        list_feature_items = uni_feature.split(',')
        # if word has no feature at all
        if len(list_feature_items)==1: return '*', '*'

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


    def __postprocess_analyzed_result(self, string_mecab_parsed_result:str, is_feature:bool, is_surface:bool)->List[TokenizedResult]:
        """Extract surface word and feature from analyzed lines.
        Extracted results are returned with list, whose elements are TokenizedResult class
        [TokenizedResult]
        """
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


    def __result_parser(self, analyzed_line:str, is_feature:bool, is_surface:bool)->TokenizedResult:
        """Extract surface word and feature from analyzed line.
        Extracted elements are returned with TokenizedResult class
        """
        assert isinstance(analyzed_line, str)
        assert isinstance(is_feature, bool)
        assert isinstance(is_surface, bool)


        surface, features = analyzed_line.split('\t')
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

    def tokenize(self, sentence:str,
                 normalize:bool=True,
                 is_feature:bool=False,
                 is_surface:bool=False,
                 return_list:bool=False,
                 func_normalizer:Callable[[str], str]=None
                 )->Union[TokenizedSenetence, List[ContentsTypes]]:
        """* What you can do
        -
        """
        assert isinstance(sentence, str)
        ### decide normalization function depending on dictType
        if func_normalizer is None and self._dictType == 'neologd':
            normalized_sentence = normalize_text(sentence, dictionary_mode='neologd')
            normalized_sentence = normalized_sentence.replace('　', '')
        elif func_normalizer is None:
            normalized_sentence = normalize_text(sentence)
            normalized_sentence = normalized_sentence.replace('　', '')
        else:
            normalized_sentence = func_normalizer(sentence)

        # don't delete this variable. encoded_text protects sentence from deleting
        encoded_text = normalized_sentence

        parsed_result = self.mecabObj.parse(encoded_text)
        tokenized_objects = self.__postprocess_analyzed_result(
            string_mecab_parsed_result=parsed_result,
            is_feature=is_feature,
            is_surface=is_surface
        )
        tokenized_sentence = TokenizedSenetence(
            sentence=sentence,
            tokenized_objects=tokenized_objects
        ) # type: TokenizedSenetence

        if return_list:
            return tokenized_sentence.convert_list_object()
        else:
            return tokenized_sentence

    def filter(self, parsed_sentence:TokenizedSenetence, pos_condition:List[Tuple[str,...]]=None, stopwords:List[str]=None)->FilteredObject:
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))

        return parsed_sentence.filter(pos_condition, stopwords)