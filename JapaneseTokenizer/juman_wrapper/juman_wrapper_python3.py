from JapaneseTokenizer.common import text_preprocess, filter
from JapaneseTokenizer import init_logger
from JapaneseTokenizer.datamodels import FilteredObject, TokenizedResult, TokenizedSenetence
from typing import List, Dict, Tuple, Union, TypeVar
import logging
import sys
import socket
import six
import os
import re
__author__ = 'kensuke-mi'

logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
python_version = sys.version_info
ContentsTypes = TypeVar('T')

try:
    import pyknp
except ImportError:
    logger.error(msg='pyknp is not ready to use. Check your installing log.')


class MonkeyPatchSocket(object):
    """* Class for overwriting pyknp.Socket because it is only for python2.x"""
    def __init__(self, hostname, port, option=None):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((hostname, port))
        except:
            raise
        if option is not None:
            self.sock.send(option)
        data = b""
        while b"OK" not in data:
            #while isinstance(data, bytes) and b"OK" not in data:
            data = self.sock.recv(1024)

    def __del__(self):
        if self.sock:
            self.sock.close()

    def query(self, sentence, pattern):
        assert(isinstance(sentence, six.text_type))
        self.sock.sendall(b"%s\n" % sentence.encode('utf-8').strip())
        data = self.sock.recv(1024)
        assert isinstance(data, bytes)
        recv = data
        while not re.search(pattern, recv):
            data = self.sock.recv(1024)
            recv = b"%s%s" % (recv, data)
        return recv.strip().decode('utf-8')


class JumanWrapper:
    def __init__(self, command:str='juman', server:Union[str,None]=None,
                 port:int=32000,
                 timeout:int=30,
                 rcfile:str=None,
                 option:bytes=b'-e2 -B',
                 pattern:bytes=b'EOS',
                 **args):
        """* Class to call Juman tokenizer
        """
        if not rcfile is None and not os.path.exists(rcfile): raise FileExistsError('rcfile does not exist at {}'.format(rcfile))

        self.juman = pyknp.Juman(command=command, server=server, port=port,
                                 timeout=timeout, rcfile=rcfile, option=option,
                                 pattern=pattern, **args)
        ### It overwrites juman_lines() method ###
        self.juman.juman_lines = self.__monkey_patch_juman_lines
        self.timeout = timeout

    def __monkey_patch_juman_lines(self, input_str:str):
        """* What you can do
        - It overwrites juman_line() method because this method causes TypeError in python3
        """
        if not self.juman.socket and not self.juman.subprocess:
            if self.juman.server is not None:
                self.juman.socket = MonkeyPatchSocket(self.juman.server, self.juman.port, b"RUN -e2\n")
            else:
                command = "%s %s" % (self.juman.command, self.juman.option)
                if self.juman.rcfile:
                    command += " -r %s" % self.juman.rcfile
                self.subprocess = pyknp.Subprocess(command)
        if self.juman.socket:
            return self.juman.socket.query(input_str, pattern=self.juman.pattern)
        return self.juman.subprocess.query(input_str, pattern=self.juman.pattern)


    def __extract_morphological_information(self, mrph_object:pyknp.Morpheme, is_feature:bool, is_surface:bool)->TokenizedResult:
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

    def __feature_parser(self, uni_feature:str, word_surface:str)->Tuple[Tuple[str,str,str,],str]:
        """
        Parse the POS feature output by Mecab
        :param uni_feature unicode:
        :return ( (pos1, pos2, pos3), word_stem ):
        """
        list_feature_items = uni_feature.split(',')
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

    def tokenize(self, sentence:str, normalize:bool=True,
                 is_feature:bool=False,
                 is_surface:bool=False,
                 return_list:bool=True)->Union[List[ContentsTypes], TokenizedSenetence]:
        """
        :param sentence:
        :param ins_mecab:
        :param list_stopword:
        :param list_pos_candidate:
        :return:  list [tuple (unicode, unicode)]
        """
        assert isinstance(normalize, bool)
        assert isinstance(sentence, str)
        if normalize:
            normalized_sentence = text_preprocess.normalize_text(sentence, dictionary_mode='ipadic')
        else:
            normalized_sentence = sentence

        result = self.juman.analysis(normalized_sentence)
        token_objects = [
            self.__extract_morphological_information(
                mrph_object=morph_object,
                is_surface=is_surface,
                is_feature=is_feature
            )
            for morph_object in result]

        if return_list:
            tokenized_objects = TokenizedSenetence(
                sentence=sentence,
                tokenized_objects=token_objects)
            return tokenized_objects.convert_list_object()
        else:
            tokenized_objects = TokenizedSenetence(
                sentence=sentence,
                tokenized_objects=token_objects)

            return tokenized_objects

    def convert_str(self, p_c_tuple):
        converted = []
        for item in p_c_tuple:
            if isinstance(item, str): converted.append(item)
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

    def filter(self, parsed_sentence:TokenizedSenetence, pos_condition=None, stopwords=None)->FilteredObject:
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))

        if isinstance(stopwords, type(None)):
            s_words = []
        else:
            s_words = stopwords

        if isinstance(pos_condition, type(None)):
            p_condition = []
        else:
            p_condition = self.__check_pos_condition_str(pos_condition)

        filtered_object = filter.filter_words(
            tokenized_obj=parsed_sentence,
            valid_pos=p_condition,
            stopwords=s_words
        )
        assert isinstance(filtered_object, FilteredObject)

        return filtered_object
