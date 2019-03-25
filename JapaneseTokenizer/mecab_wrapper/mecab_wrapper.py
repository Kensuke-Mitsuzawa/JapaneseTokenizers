#! -*- coding: utf-8 -*-
# core module
from JapaneseTokenizer.object_models import WrapperBase
from JapaneseTokenizer.common.text_preprocess import normalize_text
from JapaneseTokenizer import init_logger
from JapaneseTokenizer.datamodels import TokenizedResult, TokenizedSenetence, FilteredObject
import MeCab
# else
import sys
import os
import logging
import subprocess
import six
from six import text_type
# typing
from typing import List, Tuple, Union, TypeVar, Callable
ContentsTypes = TypeVar('T')

__author__ = 'kensuke-mi'

logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
python_version = sys.version_info

try:
    import neologdn
    is_neologdn_valid = True
except:
    logger.warning("neologdn package is not installed yet. You could not call neologd dictionary.")
    is_neologdn_valid = False


class MecabWrapper(WrapperBase):
    def __init__(self,
                 dictType,
                 pathUserDictCsv=None,
                 path_mecab_config=None,
                 path_dictionary=None,
                 string_encoding='utf-8'):
        # type: (text_type, text_type, text_type, text_type, text_type)->None
        """

        :param dictType: a dictionary type called by mecab
        :param pathUserDictCsv: path to your original dictionary file
        :param path_mecab_config: path to 'mecab_config' command. It's automatically detected if not give
        :param path_dictionary: path to a dictionary which you want to use. If not given, it's automatically detected
        :param string_encoding: encoding option to parse command line result. This is mainly used for python2.x
        """
        self.string_encoding = string_encoding
        self._dictType = dictType
        self._pathUserDictCsv = pathUserDictCsv
        self._path_dictionary = path_dictionary
        if path_mecab_config is None:
            self._path_mecab_config = self.__get_path_to_mecab_config()
        else:
            self._path_mecab_config = path_mecab_config

        if self._path_dictionary is not None:
            assert os.path.exists(self._path_dictionary), 'Path dictionary is NOT exist.'
            self._mecab_dictionary_path = None
        else:
            self._mecab_dictionary_path = self.__check_mecab_dict_path()

        logger.info("mecab dictionary path is detected under {}".format(self._mecab_dictionary_path))
        self.mecabObj = self.__CallMecab()

        assert dictType in ["neologd", "all", "ipadic", "ipaddic", "user", "", "jumandic", "unidic", None], \
            'Dictionary Type Error. Your dict = {} is NOT available.'
        if dictType == 'all':
            logger.error('dictionary type "all" is deprecated from version1.6')
            raise Exception('dictionary type "all" is deprecated from version1.6')
        if dictType == 'user':
            logger.error('dictionary type "user" is deprecated from version1.6. You just give path to dictionary csv.')
            raise Exception('dictionary type "all" is deprecated from version1.6. You just give path to dictionary csv.')

        if pathUserDictCsv is not None and isinstance(pathUserDictCsv, text_type) and pathUserDictCsv != '':
            assert os.path.exists(pathUserDictCsv), \
                'Your user dictionary does NOT exist. Path={}'.format(pathUserDictCsv)

    def __get_path_to_mecab_config(self):
        """You get path into mecab-config
        """
        if six.PY2:
            path_mecab_config_dir = subprocess.check_output(['which', 'mecab-config'])
            path_mecab_config_dir = path_mecab_config_dir.strip().replace('/mecab-config', '')
        else:
            path_mecab_config_dir = subprocess.check_output(['which', 'mecab-config']).decode(self.string_encoding)
            path_mecab_config_dir = path_mecab_config_dir.strip().replace('/mecab-config', '')

        logger.info(msg='mecab-config is detected at {}'.format(path_mecab_config_dir))
        return path_mecab_config_dir

    def __check_mecab_dict_path(self):
        """check path to dict of Mecab in system environment
        """
        mecab_dic_cmd = "echo `{} --dicdir`".format(os.path.join(self._path_mecab_config, 'mecab-config'))

        try:
            if six.PY2:
                path_mecab_dict = subprocess.check_output( mecab_dic_cmd, shell=True  ).strip('\n')
            else:
                path_mecab_dict = subprocess.check_output(mecab_dic_cmd, shell=True).decode(self.string_encoding).strip('\n')

        except subprocess.CalledProcessError:
            logger.error("{}".format(mecab_dic_cmd))
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to execute mecab-config command")
        if path_mecab_dict == '':
            raise SystemError("""mecab dictionary path is not found with following command: {} 
            You are not able to use additional dictionary. 
            Still you are able to call mecab default dictionary""".format(mecab_dic_cmd))

        return path_mecab_dict

    def __check_mecab_libexe(self):
        mecab_libexe_cmd = "echo `{} --libexecdir`".format(os.path.join(self._path_mecab_config, 'mecab-config'))

        try:
            if six.PY2:
                path_mecab_libexe = subprocess.check_output( mecab_libexe_cmd, shell=True  ).strip('\n')
            else:
                path_mecab_libexe = subprocess.check_output(mecab_libexe_cmd, shell=True).decode(self.string_encoding).strip('\n')

        except subprocess.CalledProcessError:
            logger.error("{}".format(mecab_libexe_cmd))
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to execute mecab-config --libexecdir")
        if path_mecab_libexe == '':
            raise SystemError("""Mecab config is not callable with following command: {} 
            You are not able to compile your user dictionary. 
            Still, you are able to use default mecab dictionary.""".format(mecab_libexe_cmd))

        return path_mecab_libexe

    def __CallMecab(self):
        if self._path_dictionary is not None and self._mecab_dictionary_path is None:
            logger.debug('Use dictionary you specified.')
            cmMecabInitialize = '-d {}'.format(self._path_dictionary)
        elif self._dictType == 'neologd':
            # use neologd
            logger.debug('Use neologd additional dictionary')
            cmMecabInitialize = '-d {}'.format(os.path.join(self._mecab_dictionary_path, "mecab-ipadic-neologd"))
        elif self._dictType == 'ipadic' or self._dictType == 'ipaddic':
            # use ipadic
            logger.debug('Use ipadic dictionary')
            cmMecabInitialize = '-d {}'.format(os.path.join(self._mecab_dictionary_path, "ipadic"))
        elif six.PY2 is False and self._dictType == 'jumandic':
            # use jumandic. This is impossible to call in Python2.x
            logger.debug('Use jumandic dictionary')
            cmMecabInitialize = '-d {}'.format(os.path.join(self._mecab_dictionary_path, "jumandic"))
        elif six.PY2 and self._dictType == 'jumandic':
            raise Exception('In python2.x, impossible to call jumandic.')
        else:
            logger.debug('Use no default dictionary')
            cmMecabInitialize = ''

        # execute compile if user dictionary is given
        if self._pathUserDictCsv is not None:
            logger.debug('Use User dictionary')
            pathUserDict = self.__CompileUserdict()
            cmMecabInitialize += ' -u {}'.format(pathUserDict)

        if six.PY2:
            cmMecabCall = "-Ochasen {}".format(cmMecabInitialize)
        else:
            cmMecabCall = "{}".format(cmMecabInitialize)
        logger.debug(msg="mecab initialized with {}".format(cmMecabCall))

        try:
            mecabObj = MeCab.Tagger(cmMecabCall)
        except Exception as e:
            logger.error(e.args)
            logger.error("Possibly Path to userdict is invalid. Check the path")
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to initialize Mecab object")

        return mecabObj

    def __CompileUserdict(self):
        """* What you can do
        """
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

    def __postprocess_analyzed_result(self, string_mecab_parsed_result, is_feature, is_surface):
        # type: (text_type,bool,bool)->List[TokenizedResult]
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

    def __result_parser(self, analyzed_line, is_feature, is_surface):
        # type: (text_type,bool,bool)->TokenizedResult
        """Extract surface word and feature from analyzed line.
        Extracted elements are returned with TokenizedResult class
        """
        assert isinstance(analyzed_line, str)
        assert isinstance(is_feature, bool)
        assert isinstance(is_surface, bool)

        surface, features = analyzed_line.split('\t', 1)
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

    def tokenize(self, sentence,
                 normalized=True,
                 is_feature=False,
                 is_surface=False,
                 return_list=False,
                 func_normalizer=normalize_text):
        # type: (text_type, bool, bool, bool, bool, Callable[[str], str])->Union[List[str], TokenizedSenetence]
        """* What you can do
        - Call mecab tokenizer, and return tokenized objects

        """
        if six.PY2 and isinstance(sentence, str):
            sentence = sentence.decode(self.string_encoding)
        else:
            pass

        # decide normalization function depending on dictType
        if func_normalizer is None and self._dictType == 'neologd' and is_neologdn_valid:
            normalized_sentence = neologdn.normalize(sentence)
        elif func_normalizer is None and self._dictType == 'neologd' and is_neologdn_valid == False:
            raise Exception("You could not call neologd dictionary bacause you do NOT install the package neologdn.")
        elif func_normalizer == normalize_text:
            normalized_sentence = normalize_text(sentence, dictionary_mode=self._dictType)
        elif func_normalizer is None:
            normalized_sentence = sentence
        else:
            normalized_sentence = func_normalizer(sentence)

        # don't delete this variable. The variable "encoded_text" protects sentence from deleting
        if six.PY2:
            encoded_text = normalized_sentence.encode(self.string_encoding)
        else:
            encoded_text = normalized_sentence

        if six.PY2:
            tokenized_objects = []
            node = self.mecabObj.parseToNode(encoded_text)
            node = node.next
            while node.next is not None:
                word_surface = node.surface.decode(self.string_encoding)

                tuple_pos, word_stem = self.__feature_parser(node.feature.decode(self.string_encoding), word_surface)

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
                tokenized_objects=tokenized_objects)
        else:
            parsed_result = self.mecabObj.parse(encoded_text)
            tokenized_objects = self.__postprocess_analyzed_result(
                string_mecab_parsed_result=parsed_result,
                is_feature=is_feature,
                is_surface=is_surface
            )
            tokenized_sentence = TokenizedSenetence(
                sentence=sentence,
                tokenized_objects=tokenized_objects
            )  # type: TokenizedSenetence

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
