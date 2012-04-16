# -*- coding: utf8 -*-
#!/usr/bin/python

import sys; sys.path.append("../common")
import ConfigParser
import struct
from functools import partial

from gevent.server import StreamServer
from common.GlobalTimer import global_timer
from common import Log, BaseServer
from gevent import socket

import Storage

# 数据库链接服务器，用来处理Entity的查询，保存请求

class DbMgrServer(BaseServer.BaseServer):

    CONFIG_FILE = '../etc/server.cfg'

    def __init__(self):
        self._handlers = {
            ### loginApp 协议
            # loginApp 向 dbMgr 注册
            'LoginAppRegiste' : partial(self.loginAppRegisteHandler, cmd='LoginAppRegisteResp'),
            # 玩家登录
            'PlayerLogon' : partial(self.playerLogonHandler, cmd='playerLogonResp'),
            # 玩家退出
            'PlayerLogoff' : partial(self.playerLogoffHandler, cmd='playerLogoffResp'),

            ### gridAppMgr 协议
            # gridAppMgr 向 dbMgr 注册
            'GridAppMgrRegiste' : partial(self.gridAppMgrHandler, cmd='GridAppMgrRegisteResp'),
        }
        self.log = Log.Log('../logs/dbmgr.log')
        self.init()
        self.loginapps = set([])
        self.gridmgr = None

    # 初始化部分数据
    def init(self):
        global CONFIG_FILE
        # 初始化配置信息
        cfg = ConfigParser.ConfigParser()
        cfg.read(CONFIG_FILE)

        ip = cfg.get('dbmgr', 'ip')
        port = cfg.getint('dbmgr', 'port')
        if not ip or not port:
            self.log.error('init', 'Configure: need address of dbMgr')
            raise Exception('Configure: need address of dbMgr')
        self.dbmgr_addr = (ip, port)

        storage_type = cfg.get('database', 'database')
        if storage_type.strip().lower() == 'nosql':
            self.storage_factory = Storage.NoSql
        elif storage_type.strip().lower() == 'mysql':
            self.storage_factory = Storage.MySql
        else:
            self.log.error('init', 'Configure: database type not supported')
            raise Exception('Configure: database type not supported')

        # 初始化数据库参数
        host = cfg.get('database', 'host')
        user = cfg.getint('database', 'user')
        passwd = cfg.getint('database', 'passwd')
        db = cfg.getint('database', 'db')
        if not host or not user or not user or not passwd:
            self.log.error('init', 'database config file error')
            raise Exception('database config file error')

        self.storage = self.storage_factory(host = host, user = user, passwd = passwd, port = port, db = db)

    # account logon， 验证帐号密码
    # 通过 storage 访问持久化数据
    def playerLogonHandler(self, client_sock, dict, cmd):
        #
        def onCompleteHandler(dataset, affected, result):
            dict = {}
            dict['cmd'] = cmd
            if affected == 1 and len(dataset) == 1:
                dict['result'] = 'ok'
                dict['dbid'] = int(dataset[0][0])
            else:
                dict['result'] = result
                dict['dbid'] = 0
            self.sendJson(client_sock, dict)

        if client_sock not in self.loginapps:
            self.log.error('protocol', 'anonymous want to logon')
            return
        account = dict['account']
        passwd  = dict['passwd']
        sql = 'select id from tbl_Account where account="%s" and passwd="%s"' \
             % (account, passwd)
        self.storage.executeRawCommand(sql, onCompleteHandler)

    # avatar logoff
    # 设置在线映射表
    def playerLogoffHandler(self, client_sock, dict, cmd):
        pass

    # loginApp向dbMgr 注册
    # todo : 验证 IP 地址
    def loginAppRegisteHandler(self, client_sock, dict, cmd):
        dict = {}
        dict['cmd'] = cmd
        if client_sock in self.loginapps:
            dict['result'] = 'duplicate'
            self.log.error('login', 'loginApp registe duplicate')
        else:
            self.log.info('login', 'loginApp registe succed')
            dict['result'] = 'ok'
            self.loginapps.add(client_sock)
        self.sendJson(client_sock, dict)

    # gridAppMgr 向dbMgr 注册
    def gridAppMgrHandler(self, client_sock, dict, cmd):
        dict = {}
        dict['cmd'] = cmd
        if self.gridmgr is not None:
            self.log.error('login', 'gridAppMgr registe duplicate')
            dict['result'] = 'duplicate'
        else:
            self.log.info('login', 'gridAppMgr registe succeed')
            self.gridmgr = client_sock
            dict['result'] = 'ok'
        self.sendJson(client_sock, dict)

    # 加载 Entity
    def loadEntity(self, entity_type, id, onCompleteHandler):
        self.storage.get(entity_type, id, onCompleteHandler)

    # 创建 Entity
    def createEntity(self, entity_type, id, onCompleteHandler):
        pass

    # 写回 Entity
    def writeEntity(self, entity_type, id, prop_list, onCompleteHandler):
        pass

    # 删除 Entity
    def deleteEntity(self, entity_type, id, onCompleteHandler):
        self.storage.delete(entity_type, id, onCompleteHandler)

    # 执行 原始的SQL 命令
    # 仅关系数据库支持。 xml，nosql 不支持
    def executeRawCommand(self, sql, onCompleteHandler):
        try:
            self.storage.executeRawCommand(sql, onCompleteHandler)
        except:
            onCallback([], 1, 'Failed')

    # 将申请的多余的ID 还回id pool
    def putIDs(self, ids, onCompleteHandler):
        pass

    # 申请一定数量的id
    def getIDs(self, nums, onCompleteHandler):
        pass


dbmgr_server = DbMgrServer()

def DbMgrHandler(client_sock, client_addr):
    while True:
        try:
            length = struct.unpack("=H", client_sock.recv(2))
            raw_data = client_sock.recv(length)
            dict = dbmgr_server.parseRawData(raw_data)
            dbmgr_server.process(client_sock, dict)
        except:
            dbmgr_server.quit(client_sock)
            break

if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    print "Start dbmgr server on %s:%s" % (host, port)
    try:
        tcp_server = StreamServer((host, port), DbMgrHandler)
        dbmgr_server.serve_forever()
    except:
        tcp_server.kill()
