# coding: utf-8
#!/usr/bin/python

from twisted.internet import protocol

import Message

class Proxy(protocol.Protocol):
    def __init__(self):
        self.registry = self.factory.registry
        self.event_server = self.factory.event_server
        self.bandwidth_per_second = 0
        self.client_addr = None
        self.entities_enabled = False
        sellf.has_client = False
        self.lastency_last = 0
        self.latency_triggers = []
        self.time_since_heard_from_client = 0
        self.username = ''
        self.password = ''
        self.has_login = False


    def connectionMade(self):
        self.ip, self.port = self.transport.getPeer()
        self.event_server.registerEvent(self, Message.Login)
        sellf.has_client = True

    def login(self, username, password):
        if self.registry.exist(username):
            self.talk('duplicate login')
            self.clientDead()
            return
        self.username = username
        self.password = password
        self.registry.registerUser(username, password, self.ip, self.port, self)
        self.onLogOnAttempt(self.ip, self.port, username, password)

    def dataReceived(self, data):
        self.event_server.dispatch(self, data)

    def connectionLost(self, reason):
        sellf.has_client = False
        self.onClientDeath()

    def giveClientTo(self, proxy):
        pass

    def onClientDeath(self):
        pass

    def clientDead(self):
        self.transport.loseConnection()

    def onEntitiesEnable(self):
        self.entities_enabled = True

    def onLogOnAttempt(self, ip, port, username, password):
        pass

    def onLatencyTrigger(self, latebct, goneAboveThis):
        pass

    def onWriteToDb(self):
        pass

    def talk(self, msg):
        self.transport.write(msg)

