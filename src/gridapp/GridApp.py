# coding: utf-8
#!/usr/bin/python

import SpaceMgr
import Proxy

from common.Log import log

class GridApp(object):

    CONFIG_FILE = '../etc/grids.cfg'

    def __init__(self, id):
        self.id = id   # 启动时，根据id，获取自己所管辖的 space
        self.proxys = {}
        self.spaces = []
        self.log = Log.Log('../logs/dbmgr.log')
        self.init()

    def init(self):
        cfg = ConfigParser.ConfigParser()
        cfg.read(GridApp.CONFIG_FILE)

        ip = cfg.get('gridsmgr', 'ip')
        port = cfg.getint('gridsmgr', 'port')
        if not ip or not port:
            raise Exception('Configure: need address of gridsMgr')
        self.gridmgr_addr = (ip, port)

        self.registeToGridMgr()

        spaces = cfg.get('gridapp%02d' % self.id, 'spaces')
        self.spaces = {}
        for space in spaces.split(';'):
            self.spaces[space] = SpaceMgr.Space(space)
        port = cfg.getint('dbmgr', 'port')
        if not ip or not port:
            raise Exception('Configure: need address of dbMgr')
        self.dbmgr_addr = (ip, port)

    def onEntityEnter(self, entity):
        if isinstance(entity, Proxy.Proxy):
            self.proxys[entity.id] = entity
        else:
            self.entities[entity.id] = entity



