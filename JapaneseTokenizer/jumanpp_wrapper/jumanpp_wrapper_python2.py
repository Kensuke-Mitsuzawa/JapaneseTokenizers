from pyknp import Jumanpp
from pyknp import MList
from JapaneseTokenizer.object_models import WrapperBase
from JapaneseTokenizer.common import text_preprocess, juman_utils
from JapaneseTokenizer import init_logger
from JapaneseTokenizer.datamodels import FilteredObject, TokenizedSenetence
from typing import List, Dict, Tuple, Union, TypeVar
from future.utils import string_types, text_type
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
    def __init__(self, hostname, port, timeout=50, option=None):
        # type: (str, int, int, Dict[string_types,Any])->None
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((hostname, port))
        except:
            raise Exception("There is no jumanpp server hostname={}, port={}".format(hostname, port))
        if option is not None:
            self.sock.send(option)
        data = ''
        self.sock.settimeout(timeout)

    def __del__(self):
        if self.sock: self.sock.close()

    def query(self, sentence, pattern):
        # type: (unicode, bytes) -> unicode
        assert (isinstance(sentence, six.text_type))
        data = ''
        self.sock.sendall("%s\n" % sentence.encode('utf-8').strip())
        data = self.sock.recv(1024)
        assert isinstance(data, bytes)
        recv = data
        while not re.search(pattern, recv):
            data = self.sock.recv(1024)
            recv = "%s%s" % (recv, data)
        return recv.strip().decode('utf-8')


class JumanppWrapper(WrapperBase):
    """Class for Juman++"""
    def __init__(self, command='jumanpp', timeout=30, pattern='EOS', server=None, port=12000, **args):
        # type: (str, int, str, str, int, Dict[str,Any]) -> None
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
        del self.jumanpp_obj

    def call_juman_interface(self, input_str):
        # type: (unicode) -> MList
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
        # type: (unicode, bool, bool, bool, bool, Callable[[unicode], unicode]) -> Union[TokenizedSenetence, List[unicode]]
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

    def filter(self, parsed_sentence, pos_condition=None, stopwords=None):
        # type: (TokenizedSenetence, List[Tuple[unicode,...]], List[unicode]) -> FilteredObject
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))

        return  parsed_sentence.filter(pos_condition, stopwords)
