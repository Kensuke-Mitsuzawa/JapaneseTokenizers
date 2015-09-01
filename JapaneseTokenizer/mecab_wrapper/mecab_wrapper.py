#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

import sys
import os
import MeCab
import logging
import subprocess
from text_preprocess import normalize_text
logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

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
            path_mecab_dict = subprocess.check_output( mecab_dic_cmd, shell=True  ).strip(u'\n')
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
            path_mecab_libexe = subprocess.check_output( mecab_libexe_cmd, shell=True  ).strip(u'\n')
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
        list_feature_items = uni_feature.split(u',')
        # if word has no feature at all
        if len(list_feature_items)==1: return u'*', u'*'

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


    def tokenize(self, sentence, is_feature=False, is_surface=False):
        """
        :param sentence:
        :param ins_mecab:
        :param list_stopword:
        :param list_pos_candidate:
        :return:  list [tuple (unicode, unicode)]
        """
        assert isinstance(sentence, unicode)

        list_sentence_processed = []  # list to save word stem of posted contents
        normalized_sentence = normalize_text(sentence)

        # don't delete this variable. encoded_text protects sentence from deleting
        encoded_text = normalized_sentence.encode('utf-8')

        node = self.mecabObj.parseToNode(encoded_text)
        node = node.next
        while node.next is not None:
            word_surface = node.surface.decode('utf-8')
            tuple_pos, word_stem = self.__feature_parser(node.feature.decode('utf-8'), word_surface)
            if is_feature == True:
                if is_surface == True:
                    list_sentence_processed.append( (word_surface, tuple_pos) )
                else:
                    list_sentence_processed.append( (word_stem, tuple_pos) )
            else:
                if is_surface == True:
                    list_sentence_processed.append( word_surface )
                else:
                    list_sentence_processed.append( word_stem )

            node = node.next

        return list_sentence_processed