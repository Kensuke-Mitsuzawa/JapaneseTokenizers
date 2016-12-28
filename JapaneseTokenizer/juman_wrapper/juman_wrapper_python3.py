from JapaneseTokenizer.object_models import WrapperBase
from JapaneseTokenizer.common import text_preprocess, juman_utils
from JapaneseTokenizer import init_logger
from JapaneseTokenizer.datamodels import FilteredObject, TokenizedSenetence
from typing import List, Union, TypeVar, Tuple
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


class JumanWrapper(WrapperBase):
    def __init__(self, command:str='juman', server:Union[str,None]=None,
                 port:int=32000,
                 timeout:int=30,
                 rcfile:str=None,
                 option:Union[bytes, str]='-e2 -B',
                 pattern:Union[bytes, str]='EOS',
                 **args):
        """* Class to call Juman tokenizer
        """
        if not rcfile is None and not os.path.exists(rcfile): raise FileExistsError('rcfile does not exist at {}'.format(rcfile))
        if not server is None:
            ### It converts from str into bytes only for sever mode ###
            option = option.encode('utf-8')
            pattern = pattern.encode('utf-8')

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
                self.juman.subprocess = pyknp.Subprocess(command)
        if self.juman.socket:
            return self.juman.socket.query(input_str, pattern=self.juman.pattern)
        return self.juman.subprocess.query(input_str, pattern=self.juman.pattern)

    def call_juman_interface(self, input_str):
        # type: (str) -> MList
        """* What you can do
        - You call Juman tokenizer interface.

        * Output
        - pyknp.MList
        """
        return self.juman.analysis(input_str)


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
