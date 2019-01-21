#! -*- coding: utf-8 -*-
from pyknp import Juman
from pyknp import MList
# modules
from JapaneseTokenizer.object_models import WrapperBase
from JapaneseTokenizer.common import text_preprocess, juman_utils
from JapaneseTokenizer.common.sever_handler import JumanppHnadler, ProcessDownException
from JapaneseTokenizer import init_logger
from JapaneseTokenizer.datamodels import FilteredObject, TokenizedSenetence
from typing import List, Dict, Tuple, Union, TypeVar, Any, Callable
# timeout
from JapaneseTokenizer.common.timeout_handler import on_timeout
from six import text_type
import logging
import sys
import socket
import six
import re
import os
__author__ = 'kensuke-mi'

logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
python_version = sys.version_info
ContentsTypes = TypeVar('T')

try:
    import pyknp
except ImportError:
    logger.warning(msg='pyknp is not ready to use. Install first if you would like to use pyknp wrapper.')


if six.PY2:
    ConnectionRefusedError = Exception 
    class JumanppClient(object):
        """Class for receiving data as client"""
        def __init__(self, hostname, port, timeout=50, option=None):
            # type: (text_type, int, int, Dict[text_type,Any])->None
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if isinstance(port, text_type):
                    port = int(port)
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
            # type: (text_type, bytes) -> text_type
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

else:
    class JumanppClient(object):
        """Class for receiving data as client"""
        def __init__(self, hostname, port, timeout=50, option=None):
            # type: (text_type, int, int, Dict[text_type,Any])->None
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if isinstance(port, str):
                    port = int(port)
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
            # type: (str, Union[str,bytes]) -> str
            assert (isinstance(sentence, six.text_type))
            if isinstance(pattern, str):
                pattern = pattern.encode('utf-8')
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

    def __init__(self,
                 command='jumanpp',
                 timeout=30,
                 pattern=r'EOS',
                 server=None,
                 port=12000,
                 is_use_pyknp = False,
                 ** args):
        # type: (text_type,int,text_type,text_type,bool)
        """* What you can do
        - You can select backend process of jumanpp.
            - jumanpp-pexpect: It calls jumanpp on your local machine. It keeps jumanpp process running.
            - jumanpp-pyknp: It calls jumanpp on your local machine. It launches jumanpp process everytime you call. Thus, this is slower than jumanpp-pexpect
            - jumanpp-server: It calls jumannpp on somewhere else. Keep mind, you have jumanpp sever process somewhere.

        * Parameters
        - timeout: Time to wait from jumanpp process.
        - is_use_pyknp: bool flag to decide if you use pyknp as backend process.  If True; you use pyknp. False; you use pexpect.
        pexpect is much faster than you use pyknp. You can not use pexpect if you're using it on Windowns
        - server: hostname where jumanpp is running
        - port: port number where jumanpp is running
        """
        self.eos_pattern = pattern
        self.is_use_pyknp = is_use_pyknp


        if six.PY2:
            self.dummy_text = 'これはダミーテキストです'.decode('utf-8')
        elif six.PY3:
            self.dummy_text = 'これはダミーテキストです'

        if not server is None:
            pattern = pattern.encode('utf-8')
        else:
            pass

        if os.name == 'nt':
            """It forces to use pyknp if it runs on Windows."""
            if not self.is_use_pyknp:
                logger.warning(msg="You're not able to use pexpect in Windows. It forced to set is_use_pyknp = True")
            else:
                pass
            self.is_use_pyknp = True
        else:
            pass

        if server is None and self.is_use_pyknp:
            # jumanpp-pexpect #
            logger.debug('jumanpp wrapper is initialized with pyknp package')
            self.jumanpp_obj = Juman(
                command=command,
                timeout=timeout,
                pattern=pattern,
                jumanpp=True,
                **args)
        elif server is None:
            # jumanpp-pexpect #
            logger.debug('jumanpp wrapper is initialized with pexpect unix handler')
            self.jumanpp_obj = JumanppHnadler(jumanpp_command=command, timeout_second=timeout, pattern=pattern)  # type: JumanppHnadler
            # put dummy sentence to avoid exception just after command initialization #
            res = self.jumanpp_obj.query(self.dummy_text)
        else:
            # jumanpp-server #
            self.jumanpp_obj = JumanppClient(hostname=server, port=port, timeout=timeout)

    def __del__(self):
        if hasattr(self, "jumanpp_obj"):
            if isinstance(self.jumanpp_obj, JumanppClient):
                self.jumanpp_obj.sock.close()
            elif isinstance(self.jumanpp_obj, JumanppHnadler):
                self.jumanpp_obj.stop_process()
            else:
                del self.jumanpp_obj
        else:
            pass

    def call_juman_interface(self, input_str):
        # type: (text_type) -> MList
        """* What you can do
        - You call Juman tokenizer interface.

        * Output
        - pyknp.MList
        """
        if isinstance(self.jumanpp_obj, Juman):
            ml_token_object = self.jumanpp_obj.analysis(input_str=input_str)
        elif isinstance(self.jumanpp_obj, JumanppHnadler):
            try:
                result_token = self.jumanpp_obj.query(input_string=input_str)
            except ProcessDownException:
                """Unix process is down by any reason."""
                logger.warning("Re-starting unix process because it takes longer time than {} seconds...".format(self.jumanpp_obj.timeout_second))
                self.jumanpp_obj.restart_process()
                self.jumanpp_obj.query(self.dummy_text)
                result_token = self.jumanpp_obj.query(input_string=input_str)
                ml_token_object = MList(result_token)
            except UnicodeDecodeError:
                logger.warning(msg="Process is down by some reason. It restarts process automatically.")
                self.jumanpp_obj.restart_process()
                self.jumanpp_obj.query(self.dummy_text)
                result_token = self.jumanpp_obj.query(input_string=input_str)
                ml_token_object = MList(result_token)
            else:
                ml_token_object = MList(result_token)
        elif isinstance(self.jumanpp_obj, JumanppClient):
            server_response = self.jumanpp_obj.query(sentence=input_str, pattern=self.eos_pattern)
            ml_token_object = MList(server_response)
        else:
            raise Exception('Not defined')

        return ml_token_object

    @on_timeout(limit=60)
    def tokenize(self, sentence,
                 normalize=True,
                 is_feature=False,
                 is_surface=False,
                 return_list=False,
                 func_normalizer=text_preprocess.normalize_text):
        # type: (text_type, bool, bool, bool, bool, Callable[[text_type], text_type]) -> Union[TokenizedSenetence, List[text_type]]
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
        # type: (TokenizedSenetence, List[Tuple[text_type,...]], List[text_type]) -> FilteredObject
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))

        return  parsed_sentence.filter(pos_condition, stopwords)
