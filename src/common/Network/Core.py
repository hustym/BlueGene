# coding: utf-8
#!/usr/bin/python

# reactor.callLater是常用于超时处理和定时事件。可以设置函数按照指定的时间间隔来执行关闭非活动连接或者保存内存数据到硬盘

from twisted.internet import reactor, protocol


class QuickDisconnectedProtocol(protocol.Protocol):

    def connectionMade(self):
        print "Connected to %s." % self.transport.getPeer().host
        self.transport.loseConnection()


class BasicClientFactory(protocol.ClientFactory):

    protocol = QuickDisconnectedProtocol

    def clientConnectionLost(self, connector,reason):
        print 'Lost connection: %s'%reason.getErrorMessage()
        reactor.stop()

    def clientConnectionFailed(self, connector,reason):
        print 'Connection failed: %s' % reason.getErrorMessage()
        reactor.stop()


reactor.connectTCP('www.google.com', 80, BasicClientFactory())
reactor.run()

class Core(object):
    pass