# -*- coding: utf-8 -*-
# package module
from JapaneseTokenizer.object_models import WrapperBase
from JapaneseTokenizer.common import text_preprocess
from JapaneseTokenizer.datamodels import FilteredObject, TokenizedResult, TokenizedSenetence
from JapaneseTokenizer import init_logger
from JapaneseTokenizer.common.sever_handler import JumanppHnadler
# else
from typing import List, Union, Callable, Tuple
from six import text_type
from pyknp import MList
import logging
import sys
import os
import six

logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
__author__ = 'kensuke-mi'

python_version = sys.version_info

try:
    import pyknp
except ImportError:
    logger.warning(msg='pyknp is not ready to use. Install first if you would like to use pyknp wrapper.')

if six.PY3:
    import socket
    import re

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
                # while isinstance(data, bytes) and b"OK" not in data:
                data = self.sock.recv(1024)

        def __del__(self):
            if self.sock:
                self.sock.close()

        def query(self, sentence, pattern):
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
        # type: (text_type, text_type, int, int, text_type, Union[bytes, text_type], Union[bytes, text_type], bool, **str)->None
        """* Class to call Juman tokenizer
        """

        self.timeout = timeout
        self.pattern = pattern
        self.option = option
        self.command = command
        if not rcfile is None and not os.path.exists(rcfile):
            raise FileExistsError('rcfile does not exist at {}'.format(rcfile))
        if not server is None:
            # It converts from str into bytes only for sever mode #
            self.option = self.option.encode('utf-8')  # type: Union[str,bytes]
            self.pattern = self.pattern.encode('utf-8')  # type: Union[str,bytes]
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

        if server is not None:
            # use server mode #
            self.juman = pyknp.Juman(command=command, server=server, port=port,
                                     timeout=self.timeout, rcfile=rcfile, option=option,
                                     pattern=pattern, jumanpp=False, **args)
            if six.PY3:
                # It overwrites juman_lines() method #
                self.juman.juman_lines = self.__monkey_patch_juman_lines
        elif is_use_pyknp and server is None:
            # use unix process with pyknp
            self.juman = pyknp.Juman(command=command, server=server, port=port,
                                     timeout=self.timeout, rcfile=rcfile, option=option,
                                     pattern=pattern, jumanpp=False, **args)
        else:
            # use unix process with pexpect(RECOMMENDED) #
            self.juman = JumanppHnadler(jumanpp_command=command,
                                        option=self.option,
                                        pattern=self.pattern,
                                        timeout_second=self.timeout)

    def __del__(self):
        if hasattr(self, "juman"):
            if isinstance(self.juman, JumanppHnadler):
                self.juman.stop_process()

    def __monkey_patch_juman_lines(self, input_str):
        # type: (text_type)->text_type
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

    def __extract_morphological_information(self, mrph_object, is_feature, is_surface):
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

    def call_juman_interface(self, input_str):
        # type: (text_type)->MList
        if isinstance(self.juman, pyknp.Juman):
            result = self.juman.analysis(input_str)
            return result
        elif isinstance(self.juman, JumanppHnadler):
            try:
                result_analysis = self.juman.query(input_str)
            except UnicodeDecodeError:
                logger.warning(msg="Process is down by some reason. It restarts process automatically.")
                self.juman.restart_process()
                result_analysis = self.juman.query(input_string=input_str)
            return MList(result_analysis)
        else:
            raise Exception('Not defined.')

    def tokenize(self,
                 sentence,
                 normalize=True,
                 is_feature=False,
                 is_surface=False,
                 return_list=False,
                 func_normalizer=text_preprocess.normalize_text):
        # type: (text_preprocess, bool, bool, bool, bool, Callable[[str], text_type])->Union[List[text_type], TokenizedSenetence]
        """This method returns tokenized result.
        If return_list==True(default), this method returns list whose element is tuple consisted with word_stem and POS.
        If return_list==False, this method returns TokenizedSenetence object.
        """
        assert isinstance(normalize, bool)
        assert isinstance(sentence, text_type)
        normalized_sentence = func_normalizer(sentence)
        result = self.call_juman_interface(normalized_sentence)

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
                tokenized_objects=token_objects
            )
            return tokenized_objects.convert_list_object()
        else:
            tokenized_objects = TokenizedSenetence(
                sentence=sentence,
                tokenized_objects=token_objects)

            return tokenized_objects

    def filter(self, parsed_sentence, pos_condition=None, stopwords=None):
        # type: (TokenizedSenetence, List[Tuple[text_type,...]], List[text_type])->FilteredObject
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))

        return parsed_sentence.filter(pos_condition, stopwords)
