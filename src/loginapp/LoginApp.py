# -*- coding: utf8 -*-


import sys; sys.path.append("../common")
import ConfigParser
import struct
from functools import partial

from gevent.server import StreamServer
from common.GlobalTimer import global_timer
from common.Log import log, BaseServer
from gevent import socket


# 登录服务器，用来处理玩家的登录请求，并转发到 dbmgr 进行验证
# 验证通过的链接，转给 GridAppMgr

class LoginServer(BaseServer.BaseServer):

    CONFIG_FILE = '../etc/server.cfg'

    def __init__(self):
        self._clients = {}
        self._handlers = {
            ### 客户端协议
            # 玩家 Account 登录请求
            'ClientLogin' : partial(self.loginHandler, cmd='ClientLoginResp'),

            ### dbMgr 协议
            # 向 dbMgr 注册相应
            'LoginAppRegisteResp' : self.LoginAppRegisteRespHandler,
            # 向 dbMgr 请求玩家登录
            'playerLogonResp' : self.playerLogonRespHandler,
            # 向 dbMgr 请求玩家退出
            'playerLogoffResp' : self.playerLogoffRespHandler,
            }
        self.permit_login = False
        global_timer.addTimer(1, self.init)

    def init(self):
        cfg = ConfigParser.ConfigParser()
        cfg.read(CONFIG_FILE)

        ip = cfg.get('dbmgr', 'ip')
        port = cfg.getint('dbmgr', 'port')
        if not ip or not port:
            raise Exception('Configure: need address of dbMgr')
        self.dbmgr_addr = (ip, port)

        ip = cfg.get('gridsmgr', 'ip')
        port = cfg.getint('gridsmgr', 'port')
        if not ip or not port:
            raise Exception('Configure: need address of gridsMgr')
        self.gridmgr_addr = (ip, port)

        self.registeToDbMgr()
        self.registeToGridMgr()
        self.permit_login = True

    def isPermitLogin(self):
        return self.permit_login

    def registeToDbMgr(self):
        self.dbmgr_sock = socket.socket(type=socket.SOCK_STREAM)
        self.dbmgr_sock.connect(self.dbmgr_addr)
        dict = {}
        dict['cmd']
        self.dbmgr_sock.send()

    def registeToGridMgr(self):
        self.gridmgr_sock = socket.socket(type=socket.SOCK_STREAM)
        self.gridmgr_sock.connect(self.gridmgr_addr)
        self.gridmgr_sock.send()

    def LoginAppRegisteRespHandler(self, sock, data):
        pass

    def playerLogonRespHandler(self, client_sock, dict, cmd):
        userinfo = self._clients.get(sock, None)
        if userinfo: return
        self._clients[sock] = data['name']
        print "New User : %s" % (data['name'],)

    def playerLogonRespHandler(self, client_sock, dict, cmd):
        userinfo = self._clients.get(sock, None)
        if userinfo: return
        self._clients[sock] = data['name']
        print "New User : %s" % (data['name'],)


login_server = LoginServer()

def loginHandler(client_sock, client_addr):
    while True:
        try:
            length = struct.unpack("=H", client_sock.recv(2))
            raw_data = client_sock.recv(length)
            dict = login_server.parseRawData(raw_data)
            login_server.process(client_sock, dict)
        except:
            login_server.quit(client_sock)
            break

if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    print "Start login server on %s:%s" % (host, port)
    try:
        tcp_server = StreamServer((host, port), loginHandler)
        tcp_server.serve_forever()
    except:
        login_server.kill()
