# coding: utf-8
#!/usr/bin/python


def onServerReady():
    pass

def onServerShuttingDown( shutdown_time ):
    pass

def onServerShutDown():
    pass

def onInit(is_reload):
    pass


import Proxy
import EventServer
import Message
from twisted.internet import reactor, protocol


class Registry(object):

    def __init__(self):
        self.accounts = {}

    def exist(self, user):
        return user in self.accounts

    def unRegisterUser(self, user):
        del self.accounts[user]

    def registerUser(self, user, passwd, ip, port, proxy):
        self.accounts[user] = (passwd, ip, port, proxy)


class SmurfsServer(protocol.ServerFactory):

    protocol = Proxy.Proxy

    def __init__(self):
        self.registry = Registry()
        self.event_server = EventServer.EventServer()

        self.event_server.registerProtocol(Message.POSITON, Message.Position)
        self.event_server.registerProtocol(Message.ENTER_WORLD, Message.EnterWorld)
        self.event_server.registerProtocol(Message.LEAVE_WORLD, Message.LeaveWorld)

    def onAccountLogin(self, account, object):
        pass


if __name__ == '__main__':
    import sys
    if not len(sys.argv) == 2:
        print "Usage: %s port " % __file__
        sys.exit(1)

    reactor.listenTCP(int(sys.argv[1]), SmurfsServer(), timeout = 10)
    reactor.run()