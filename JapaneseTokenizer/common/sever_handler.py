#! -*- coding: utf-8 -*-
import subprocess
from subprocess import Popen, PIPE, STDOUT
import multiprocessing
# socket object
import socket
# logger
from JapaneseTokenizer import init_logger
import logging
# typing
from typing import Union
# else
from six import text_type
import six
import pexpect
import shutil
import signal
import os
logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))


class ProcessDownException(Exception):
    pass


class UnixProcessHandler(object):
    def __init__(self,
                 command,
                 option=None,
                 pattern='EOS',
                 timeout_second=10):
        # type: (text_type,text_type,text_type,int)->None
        """* Get communication with unix process using pexpect module."""
        self.command = command
        self.timeout_second = timeout_second
        self.pattern = pattern
        self.option = option
        self.launch_process(command)

    def __del__(self):
        if hasattr(self, "process_analyzer"):
            self.process_analyzer.kill(sig=9)

    def launch_process(self, command):
        # type: (Union[bytes,text_type])->None
        """* What you can do
        - It starts process and keep it.
        """
        if not self.option is None:
            command_plus_option = self.command + " " + self.option
        else:
            command_plus_option = self.command

        if six.PY3:
            if shutil.which(command) is None:
                raise Exception("No command at {}".format(command))
            else:
                self.process_analyzer = pexpect.spawnu(command_plus_option)
                self.process_id = self.process_analyzer.pid
        else:
            doc_command_string = "echo '' | {}".format(command)
            command_check = os.system(doc_command_string)
            if not command_check == 0:
                raise Exception("No command at {}".format(command))
            else:
                self.process_analyzer = pexpect.spawnu(command_plus_option)
                self.process_id = self.process_analyzer.pid

    def restart_process(self):
        # type: ()->None
        if not self.option is None:
            command_plus_option = self.command + " " + self.option
        else:
            command_plus_option = self.command

        self.process_analyzer.kill(sig=9)
        self.process_analyzer = pexpect.spawnu(command_plus_option)
        self.process_id = self.process_analyzer.pid

    def stop_process(self):
        # type: ()->bool
        """* What you can do
        - You're able to stop the process which this instance has now.
        """
        if hasattr(self, "process_analyzer"):
            self.process_analyzer.kill(sig=9)
        else:
            pass

        return True

    def __query(self, input_string):
        # type: (text_type)->text_type
        """* What you can do
        - It takes the result of Juman++
        - This function monitors time which takes for getting the result.
        """
        signal.signal(signal.SIGALRM, self.__notify_handler)
        signal.alarm(self.timeout_second)
        self.process_analyzer.sendline(input_string)
        buffer = ""
        while True:
            line_string = self.process_analyzer.readline()  # type: text_type
            if line_string.strip() == input_string:
                """Skip if process returns the same input string"""
                continue
            elif line_string.strip() == self.pattern:
                buffer += line_string
                signal.alarm(0)
                return buffer
            else:
                buffer += line_string

    def __notify_handler(self, signum, frame):
        raise ProcessDownException("""It takes longer time than {time} seconds. You're able to try, 
        1. Change your setting of 'timeout_second' parameter
        2. Run restart_process() method when the exception happens.""".format(**{"time": self.timeout_second}))

    def query(self, input_string):
        # type: (text_type)->text_type
        return self.__query(input_string=input_string)


class JumanppHnadler(UnixProcessHandler):

    def __init__(self,
                 jumanpp_command,
                 option = None,
                 pattern = 'EOS',
                 timeout_second = 10):
        # type: (text_type,text_type,text_type,int)->None
        super(JumanppHnadler, self).__init__(command=jumanpp_command, option=option, pattern=pattern, timeout_second=timeout_second)

    def launch_jumanpp_process(self, command):
        # type: (text_type)->None
        return self.launch_process(command)
