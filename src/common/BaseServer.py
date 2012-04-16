# -*- coding: utf8 -*-
#!/usr/bin/python

import sys; sys.path.append("../common")
import ConfigParser

try:
    import cPickle as pickle
except:
    import pickle

import struct

from gevent.server import StreamServer
#from common import global_timer
#from common import Log
from common.lib import json
from gevent import socket

import Storage

# 数据库链接服务器，用来处理Entity的查询，保存请求

class BaseServer(object):

    def __init__(self):
        raise Exception('Base Server cant not ')

    def sendJson(self, client_socket, dict):
        string = json.json_write(dict)
        raw_data = struct.pack("=H", len(string)) + string
        client_socket.send(raw_data)

    def process(self, client_sock, dict):
        cmd = dict['cmd']
        handler = self._handlers[cmd]
        handler(client_sock, dict)

    def parseRawData(self, raw_data):
        try:
            dict = json.json_read(raw_data)
            return dict
        except:
            self.log.error('parse raw data error. %s', repr(raw_data))
            return {}

    def quit(self, client_sock):
        self.log.info('server quit. ')
        import sys
        sys.exit(0)

