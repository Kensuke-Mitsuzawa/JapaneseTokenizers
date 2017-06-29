#! -*- coding: utf-8 -*-
# package modules
from JapaneseTokenizer.object_models import WrapperBase
from JapaneseTokenizer.common import text_preprocess, juman_utils
from JapaneseTokenizer import init_logger
from JapaneseTokenizer.datamodels import FilteredObject, TokenizedSenetence
from JapaneseTokenizer.common.sever_handler import JumanppHnadler  # todo
# pyknp modules
from pyknp.juman.mlist import MList
# else
from typing import List, Union, TypeVar, Tuple, Callable
from six import text_type
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
    logger.warning(msg='pyknp is not ready to use. Install first if you would like to use pyknp wrapper.')


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
        """"""
        # type: (str,str)->str
        assert(isinstance(sentence, six.text_type))
        sentence_bytes = sentence.encode('utf-8').strip()
        pattern_bytes = pattern.encode('utf-8')

        self.sock.sendall(sentence_bytes + b"\n")
        data = self.sock.recv(1024)
        assert isinstance(data, bytes)
        recv = data
        while not re.search(pattern_bytes, recv):
            data = self.sock.recv(1024)
            recv = recv + data
        return recv.strip().decode('utf-8')


class JumanWrapper(WrapperBase):
    def __init__(self,
                 command='juman',
                 server=None,
                 port=32000,
                 timeout=30,
                 rcfile=None,
                 option='-e2 -B',
                 pattern='EOS',
                 is_use_pyknp=False,
                 **args):
        """* Class to call Juman tokenizer
        """
        # type: (text_type,Union[str,None],int,int,text_type,Union[bytes,str],Union[bytes,str],bool)->None

        self.timeout = timeout
        self.pattern = pattern
        self.option = option
        self.command = command
        if not rcfile is None and not os.path.exists(rcfile):
            raise FileExistsError('rcfile does not exist at {}'.format(rcfile))
        if not server is None:
            ### It converts from str into bytes only for sever mode ###
            self.option = self.option.encode('utf-8')
            self.pattern = self.pattern.encode('utf-8')
        else:
            pass

        # check os #
        if os.name == 'nt':
            if not is_use_pyknp:
                logger.warning(msg='It forces is_use_pyknp = True on Windows.')
            else:
                pass
            self.is_use_pyknp = True
        else:
            pass


        if is_use_pyknp or not server is None:
            self.juman = pyknp.Juman(command=command, server=server, port=port,
                                     timeout=self.timeout, rcfile=rcfile, option=option,
                                     pattern=pattern, **args)
            ### It overwrites juman_lines() method ###
            self.juman.juman_lines = self.__monkey_patch_juman_lines
        else:
            self.juman = JumanppHnadler(jumanpp_command=command,
                                        option=self.option,
                                        pattern=self.pattern,
                                        timeout_second=self.timeout)

    def __del__(self):
        if hasattr(self, "juman"):
            if isinstance(self.juman, JumanppHnadler):
                self.juman.stop_process()

    def __monkey_patch_juman_lines(self, input_str:str):
        """* What you can do
        - It overwrites juman_line() method because this method causes TypeError in python3
        """
        assert isinstance(self.juman, pyknp.Juman)
        if not self.juman.socket and not self.juman.subprocess:
            if self.juman.server is not None:
                self.juman.socket = MonkeyPatchSocket(self.juman.server, self.juman.port, b"RUN -e2\n")
            else:
                command = "%s %s" % (self.juman.command, self.juman.option)
                if self.juman.rcfile:
                    command += " -r %s" % self.juman.rcfile
                self.juman.subprocess = pyknp.Subprocess(command)
        if self.juman.socket:
            return self.juman.socket.query(input_str, pattern=self.juman.pattern)
        return self.juman.subprocess.query(input_str, pattern=self.juman.pattern)

    def call_juman_interface(self, input_str):
        """* What you can do
        - You call Juman tokenizer interface.

        * Output
        - pyknp.MList
        """
        # type: (str)->MList
        if isinstance(self.juman, pyknp.Juman):
            return self.juman.analysis(input_str)
        elif isinstance(self.juman, JumanppHnadler):
            try:
                result_analysis = self.juman.query(input_str)
            except UnicodeDecodeError:
                logger.warning(msg="Process is down by some reason. It restarts process automatically.")
                self.juman.restart_process()
                result_analysis = self.juman.query(input_string=input_str)
            return MList(spec=result_analysis)
        else:
            raise Exception('Not defined.')

    def tokenize(self, sentence,
                 normalize=True,
                 is_feature=False,
                 is_surface=False,
                 return_list=False,
                 func_normalizer=text_preprocess.normalize_text):
        # type: (str, bool, bool, bool, bool, Callable[[str], str]) -> Union[TokenizedSenetence, List[str]]
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
            normalized_sentence = func_normalizer(sentence)
        else:
            normalized_sentence = sentence

        result = self.call_juman_interface(normalized_sentence)
        token_objects = [
            juman_utils.extract_morphological_information(
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

    def filter(self, parsed_sentence:TokenizedSenetence, pos_condition:List[Tuple[str, ...]]=None, stopwords:List[str]=None)->FilteredObject:
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))

        return parsed_sentence.filter(pos_condition, stopwords)
