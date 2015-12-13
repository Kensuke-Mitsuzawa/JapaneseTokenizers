#! -*- coding: utf-8 -*-
import sys
import os
import logging
import subprocess
import MeCab
from JapaneseTokenizer.mecab_wrapper.text_preprocess import normalize_text
from ..common.filter import filter_words
from ..datamodels import TokenizedResult, TokenizedSenetence, FilteredObject
__author__ = 'kensuke-mi'

try:
    unicode # python2
    def u(str): return str.decode("utf-8")
    def b(str): return str
    pass
except: # python3
    def u(str): return str
    def b(str): return str.encode("utf-8")
    pass


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")
python_version = sys.version_info


class MecabWrapper:

    def __init__(self, dictType, osType, pathUserDictCsv=''):
        assert dictType in ["neologd", "all", "ipaddic", "user", ""]
        if dictType == 'all' or dictType == 'user': assert os.path.exists(pathUserDictCsv)

        self._osType = osType
        self._dictType = dictType
        self._pathUserDictCsv = pathUserDictCsv
        self._mecab_dictionary_path = self.__check_mecab_dict_path()
        logging.info("mecab dictionary path is detected under {}".format(self._mecab_dictionary_path))

        self.mecabObj = self.__CallMecab()


    def __check_mecab_dict_path(self):
        """check path to dict of Mecab in system environment
        """

        if self._osType=="centos":
            mecab_dic_cmd = "echo `/usr/local/bin/mecab-config --dicdir`"
        else:
            mecab_dic_cmd = 'echo `mecab-config --dicdir`'

        try:
            if python_version >= (3, 0, 0):
                path_mecab_dict = subprocess.check_output( mecab_dic_cmd, shell=True  ).decode('utf-8').strip(u('\n'))
            else:
                path_mecab_dict = subprocess.check_output( mecab_dic_cmd, shell=True  ).strip(u('\n'))
        except subprocess.CalledProcessError:
            logging.error("{}".format(mecab_dic_cmd))
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to execute mecab-config command")

        return path_mecab_dict


    def __check_mecab_libexe(self):

        if self._osType=="centos":
            mecab_libexe_cmd = "echo `/usr/local/bin/mecab-config --libexecdir`"
        else:
            mecab_libexe_cmd = 'echo `mecab-config --libexecdir`'

        try:
            if python_version >= (3, 0, 0):
                path_mecab_libexe = subprocess.check_output( mecab_libexe_cmd, shell=True  ).decode('utf-8').strip(u('\n'))
            else:
                path_mecab_libexe = subprocess.check_output( mecab_libexe_cmd, shell=True  ).strip(u('\n'))
        except subprocess.CalledProcessError:
            logging.error("{}".format(mecab_libexe_cmd))
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to execute mecab-config --libexecdir")

        return path_mecab_libexe


    def __CallMecab(self):
        """
        """
        if self._dictType == 'neologd':
            logging.debug('Use neologd additional dictionary')
            cmMecabInitialize = '-d {}'.format(os.path.join(self._mecab_dictionary_path, "mecab-ipadic-neologd"))

        elif self._dictType == 'all':
            logging.debug('Use neologd additional dictionary')
            pathUserDict = self.__CompileUserdict()
            cmMecabInitialize = '-u {} -d {}'.format(pathUserDict,
                                                     os.path.join(self._mecab_dictionary_path, "mecab-ipadic-neologd"))
        elif self._dictType == 'ipadic':
            logging.debug('Use ipadic additional dictionary')
            cmMecabInitialize = '-d {}'.format(os.path.join(self._mecab_dictionary_path, "ipadic"))

        elif self._dictType == 'user':
            if python_version >= (3, 0, 0):
                sys.exit('User dictionary is not supported in Python3')

            logging.debug('Use User dictionary')
            pathUserDict = self.__CompileUserdict()
            cmMecabInitialize = '-u {}'.format(pathUserDict)

        else:
            logging.debug('Use no default dictionary')
            cmMecabInitialize = ''

        cmMecabCall = "-Ochasen {}".format(cmMecabInitialize)
        logging.debug(msg="mecab initialized with {}".format(cmMecabCall))

        try:
            mecabObj = MeCab.Tagger(cmMecabCall)
        except Exception as e:
            logging.error(e.args)
            logging.error(e.message)
            logging.error(e.args)
            logging.error("Possibly Path to userdict is invalid check the path")
            raise subprocess.CalledProcessError(returncode=-1, cmd="Failed to initialize Mecab object")

        return mecabObj


    def __CompileUserdict(self):
        # 複合語辞書のコンパイルをする

        path_mecab_dict = self.__check_mecab_dict_path()
        path_mecab_libexe = self.__check_mecab_libexe()

        if python_version >= (3, 0, 0):
            cmCompileDict = '{0}/mecab-dict-index -d {1}/ipadic -u {2} -f utf-8 -t utf-8 {3} > /dev/null'.format(path_mecab_libexe,
                                                                                                                path_mecab_dict,
                                                                                                                self._pathUserDictCsv.replace("csv", "dict"),
                                                                                                                self._pathUserDictCsv)
        else:
            cmCompileDict = u'{0}/mecab-dict-index -d {1}/ipadic -u {2} -f utf-8 -t utf-8 {3} > /dev/null'.format(path_mecab_libexe,
                                                                                                                path_mecab_dict,
                                                                                                                self._pathUserDictCsv.replace("csv", "dict"),
                                                                                                                self._pathUserDictCsv)
        logging.debug(msg="compiling mecab user dictionary with: {}".format(cmCompileDict))
        try:
            subprocess.call( cmCompileDict , shell=True )
        except OSError as e:
            logging.error('type:' + str(type(e)))
            logging.error('args:' + str(e.args))
            logging.error('message:' + e.message)
            sys.exit('Failed to compile mecab userdict. System ends')

        return self._pathUserDictCsv.replace("csv", "dict")


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
        return [
            u(s_word)
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

    def filter(self, parsed_sentence, pos_condistion, stopwords=None):
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condistion, list)
        assert isinstance(stopwords, (type(None), list))

        if isinstance(stopwords, type(None)):
            s_words = []
        else:
            s_words = self.__check_stopwords_str_typle(stopwords)

        if isinstance(pos_condistion, type(None)):
            p_condition = []
        else:
            p_condition = self.__check_pos_condition_str(pos_condistion)

        filtered_object = filter_words(
            tokenized_obj=parsed_sentence,
            valid_pos=p_condition,
            stopwords=s_words
        )
        assert isinstance(filtered_object, FilteredObject)

        return filtered_object

