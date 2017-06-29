# -*- coding: utf-8 -*-
# package module
from JapaneseTokenizer.object_models import WrapperBase
from JapaneseTokenizer.common import text_preprocess
from JapaneseTokenizer.datamodels import FilteredObject, TokenizedResult, TokenizedSenetence
from JapaneseTokenizer import init_logger
from JapaneseTokenizer.common.sever_handler import JumanppHnadler
# else
from typing import List, Union, Any, Callable, Tuple
from six import text_type
from pyknp import MList
import logging
import sys
import os

logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))
__author__ = 'kensuke-mi'

python_version = sys.version_info

try:
    import pyknp
except ImportError:
    logger.warning(msg='pyknp is not ready to use. Install first if you would like to use pyknp wrapper.')


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


        if is_use_pyknp:
            self.juman = pyknp.Juman(command=command, server=server, port=port,
                                     timeout=self.timeout, rcfile=rcfile, option=option,
                                     pattern=pattern, **args)
        else:
            self.juman = JumanppHnadler(jumanpp_command=command,
                                        option=self.option,
                                        pattern=self.pattern,
                                        timeout_second=self.timeout)

    def __del__(self):
        if hasattr(self, "juman"):
            if isinstance(self.juman, JumanppHnadler):
                self.juman.stop_process()

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
        # type: (str)->MList
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
        # type: (unicode, bool, bool, bool, bool, Callable[[str], str])->Union[List[str], TokenizedSenetence]
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
        # type: (TokenizedSenetence, List[Tuple[unicode,...]], List[unicode])->FilteredObject
        assert isinstance(parsed_sentence, TokenizedSenetence)
        assert isinstance(pos_condition, (type(None), list))
        assert isinstance(stopwords, (type(None), list))

        return parsed_sentence.filter(pos_condition, stopwords)
