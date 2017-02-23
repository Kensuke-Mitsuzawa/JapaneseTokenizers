#! -*- coding: utf-8 -*-
import six
import subprocess
from subprocess import Popen, PIPE
# socket object
import socket
# logger
from JapaneseTokenizer import init_logger
import logging
logger = init_logger.init_logger(logging.getLogger(init_logger.LOGGER_NAME))


class BaseServerHandler(object):
    def start_server(self):
        raise NotImplementedError()

    def shutdown_server(self):
        raise NotImplementedError()

    def call_server(self):
        raise NotImplementedError()


if six.PY2:
    from daemons import daemonizer

    class JumanppServerHandler(BaseServerHandler):
        def __init__(self, host, port, command):
            """* What you can do
            - You start juman++ server mode
            """
            # type: (str,int,str)->None
            self.command = command
            self.host = host
            if isinstance(port, str):
                port = int(port)
            self.port = port

        def launch_jumanpp_process(self):
            """* What you can do
            - It starts jumanpp process and keep it.
            """
            logger.debug(msg='Juman++ process is waiting with command = {}'.format(self.command))
            self.jumanpp_process = Popen(self.command, stdin=PIPE, stdout=PIPE)

        def restart_jumanpp_process(self):
            """* What you can do"""
            pass

        def __del__(self):
            if hasattr(self, 'jumanpp_process'):
                self.jumanpp_process.stdin.close()
                self.jumanpp_process.wait()

        @daemonizer.run(pidfile="/tmp/sleepy.pid")
        def start_server(self, max_queue=50):
            """"""
            # type: (int)->None
            ### it starts jumann++ process ###
            self.launch_jumanpp_process()

            ### it starts server ###
            serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            serversock.bind((self.host, self.port))  # IPとPORTを指定してバインドします
            serversock.listen(max_queue)
            logger.debug('Waiting for connections at host={} port={}...'.format(self.host, self.port))
            self.clientsock, self.client_address = serversock.accept()  # 接続されればデータを格納
            while True:
                input_string = self.clientsock.recv(1024)
                logger.debug('Received -> %s' % (input_string))
                if (buffer != "/^##JUMAN++\t.*/"): # 動的オプション
                    res = repr(self.process.stdout.readline(input_string))
                    self.clientsock.sendall() # 動的オプションの戻り値(必ず1行)
                elif (buffer != "/^#.*/"): # コメント行
                    res = self.process.stdout.readline(input_string)
                    self.clientsock.sendall()
                else:
                    responce = ""
                    responce += input_string
                    while True:
                        self.process.stdout.readline(input_string)
                        f = self.clientsock.recv(1024)
                        responce += f.to_s
                        if f.to_s == "EOS\n":
                            break
                        self.clientsock.sendall(input_string)  # メッセージを返します

        def shutdown_server(self):
            pass

        def call_server(self):
            """* What you can do
            """
            # type: ()->None
            if not hasattr(self, 'clientsock') or not hasattr(self, 'client_address') or not hasattr(self, 'process'):
                raise Exception('You must call start_server() first.')
            while True:
                input_string = self.clientsock.recv(1024)
                logger.debug('Received -> %s' % (input_string))
                if (buffer != "/^##JUMAN++\t.*/"): # 動的オプション
                    res = repr(self.process.stdout.readline(input_string))
                    self.clientsock.sendall() # 動的オプションの戻り値(必ず1行)
                elif (buffer != "/^#.*/"): # コメント行
                    res = self.process.stdout.readline(input_string)
                    self.clientsock.sendall()
                else:
                    responce = ""
                    responce += input_string
                    while True:
                        self.process.stdout.readline(input_string)
                        f = self.clientsock.recv(1024)
                        responce += f.to_s
                        if f.to_s == "EOS\n":
                            break
                        self.clientsock.sendall(input_string)  # メッセージを返します


    class JumanServerHandler(BaseServerHandler):
        pass

else:
    # asyncio.gatherを使う
    class JumanppServerHandler(BaseServerHandler):
        def __init__(self, host, port, command):
            """* What you can do
            - You start juman++ server mode
            """
            # type: (str,int,str)->None
            pass

        def launch_jumanpp_process(self):
            """* What you can do
            - It starts jumanpp process and keep it.
            """

        def __del__(self):
            pass

        def start_server(self):
            pass

        def shutdown_server(self):
            pass


    class JumanServerHandler(BaseServerHandler):
        pass