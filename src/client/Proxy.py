# -*- coding:utf8 -*-

from gevent import monkey; monkey.patch_all();
import socket
class Proxy(object):

    def connect(self, host, port):
        sock = socket.socket()
        socket.connect()