#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sys
import simplejson
from gevent import monkey; monkey.patch_all();
from gevent.server import StreamServer
from common import Protocol, gen_pro_data, parse_pro_data

class ChatService:
    def __init__(self):
        self._clients = {}
        self._handlers = {
            Protocol.Connect : self.connect,
            Protocol.SendMsg : self.sendmsg,
            Protocol.Quit : self.quit,
        }

    def connect(self, sock, data):
        userinfo = self._clients.get(sock, None)
        if userinfo: return
        self._clients[sock] = data['name']
        print "New User : %s" % (data['name'],)

    def sendmsg(self, sock, data):
        msg = gen_pro_data(data)
        for s, u in self._clients.items():
            if sock != s:
                s.send(msg)

    def quit(self, sock, data=None):
        if sock in self._clients:
            print "User [%s] quit." % (self._clients[sock],)
            del self._clients[sock]
            sock.close()

    def process(self, sock, promsg):
        cmd = promsg['cmd']
        func = self._handlers[cmd]
        func(sock, promsg)

# server chat service
chatservice = ChatService()

def serve(sock, addr):
    while True:
        try:
            length = ord(sock.recv(1))
            content = sock.recv(length)
            # protocol :  length + json({'cmd' : 'sendmsg', 'msg' : 'hallo'})
            promsg = parse_pro_data(content)
            chatservice.process(sock, promsg)
        except:
            chatservice.quit(sock)
            break

if __name__ == "__main__":
    host = sys.argv[1]
    port = int(sys.argv[2])
    print "Start chat server on %s:%s" % (host, port)
    try:
        chatserver = StreamServer((host, port), serve)
        chatserver.serve_forever()
    except:
        chatserver.kill()


def test():
    import gevent
    from gevent.pool import Pool

    def robot(idx, host, port):
        # client chat service
        chatservice = ChatService(host, port)
        chatservice.connect("user%s" % (idx,))
        while True:
            chatservice.sendmsg("hallo from %s" % (idx,))
            gevent.sleep(3)
    host = sys.argv[1]
    port = int(sys.argv[2])
    count = 5000
    pool = Pool(5000)
    for i in range(count):
        pool.spawn(robot, i, host, port)
    pool.join()
