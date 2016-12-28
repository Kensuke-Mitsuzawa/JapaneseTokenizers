from pyknp import Jumanpp
from pyknp import MList
from JapaneseTokenizer.object_models import WrapperBase
from JapaneseTokenizer.common import text_preprocess, juman_utils
from JapaneseTokenizer import init_logger
from JapaneseTokenizer.datamodels import FilteredObject, TokenizedSenetence
from typing import List, Dict, Tuple, Union, TypeVar
import logging
import sys
import socket
import six
import re
__author__ = 'kensuke-mi'

logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
python_version = sys.version_info
ContentsTypes = TypeVar('T')

try:
    import pyknp
except ImportError:
    logger.error(msg='pyknp is not ready to use. Check your installing log.')


class JumanppClient(object):
    """Class for receiving data as client"""
    def __init__(self, hostname:str, port:int, timeout:int=50, option=None):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((hostname, port))
        except ConnectionRefusedError:
            raise Exception("There is no jumanpp server hostname={}, port={}".format(hostname, port))
        except:
            raise
        if option is not None:
            self.sock.send(option)
        data = b""
        self.sock.settimeout(timeout)

    def __del__(self):
        if self.sock:
            self.sock.close()

    def query(self, sentence, pattern):
        # type: (, str, bytes) -> str
        assert (isinstance(sentence, six.text_type))
        self.sock.sendall(b"%s\n" % sentence.encode('utf-8').strip())
        data = self.sock.recv(1024)
        assert isinstance(data, bytes)
        recv = data
        while not re.search(pattern, recv):
            data = self.sock.recv(1024)
            recv = b"%s%s" % (recv, data)
        return recv.strip().decode('utf-8')


class JumanppWrapper(WrapperBase):
    """Class for Juman++"""
    def __init__(self, command='jumanpp', timeout=30, pattern=r'EOS', server:str=None, port:int=12000, **args):
        # type: (str, int, str, str) -> None
        if not server is None:
            pattern = pattern.encode('utf-8')


        self.eos_pattern = pattern
        if server is None:
            self.jumanpp_obj = Jumanpp(
                command=command,
                timeout=timeout,
                pattern=pattern,
                **args)
        else:
            self.jumanpp_obj = JumanppClient(hostname=server, port=port, timeout=timeout)

    def __del__(self):
        if isinstance(self.jumanpp_obj, JumanppClient):
            self.jumanpp_obj.sock.close()
        del self.jumanpp_obj

    def call_juman_interface(self, input_str):
        # type: (str) -> MList
        """* What you can do
        - You call Juman tokenizer interface.

        * Output
        - pyknp.MList
        """
        if isinstance(self.jumanpp_obj, Jumanpp):
            ml_token_object = self.jumanpp_obj.analysis(input_str=input_str)
        elif isinstance(self.jumanpp_obj, JumanppClient):
            server_response = self.jumanpp_obj.query(sentence=input_str, pattern=self.eos_pattern)
            ml_token_object = MList(server_response)
        else:
            raise Exception('Not defined')

        return ml_token_object

    def tokenize(self, sentence,
                 normalize=True,
                 is_feature=False,
                 is_surface=False,
                 return_list=False,
                 func_normalizer=text_preprocess.normalize_text):
        # type: (str, bool, bool, bool, bool, Callable[[str], str]) -> Union[TokenizedSenetence, List[str]]
        """* What you can do
        -
        """
        if normalize:
            normalized_sentence = func_normalizer(sentence)
        else:
            normalized_sentence = sentence

        ml_token_object = self.call_juman_interface(normalized_sentence)

        token_objects = [
            juman_utils.extract_morphological_information(
                mrph_object=morph_object,
                is_surface=is_surface,
                is_feature=is_feature
            )
            for morph_object in ml_token_object]

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

    def filter(self, parsed_sentence: TokenizedSenetence, pos_condition:List[Tuple[str,...]]=None, stopwords:List[str]=None) -> FilteredObject:
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))

        return  parsed_sentence.filter(pos_condition, stopwords)
