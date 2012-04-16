# coding: utf-8
#!/usr/bin/python

POSITON     = 0x0001
ENTER_WORLD = 0x0002
LEAVE_WORLD = 0x0003

import Message


ID_2_PROTOCOL = {
        POSITON : Message.Position,
        ENTER_WORLD : Message.EnterWorld,
        LEAVE_WORLD : Message.LeaveWorld,
        }

FUNC_2_CLASS = {
        "position" : (POSITON, ('id', 'x', 'y')),
        "enterWorld" : (ENTER_WORLD, ('id', 'x', 'y')),
        "leaveWorld" : (LEAVE_WORLD, ('id',)),
        }


class RPC(object):

    def __init__(self, transfer, proxy):
        self.transfer = transfer
        self.proxy = proxy

    def __getattr__(self, attr):
        if attr in ['enterWorld', 'leaveWorld', 'position' ]:
            return lambda *args : self.callRemote(attr, args)
        return getattr(self, attr)

    def callRemote(self, func, *args):
        head = Message.Head()
        command = None
        if func in FUNC_2_CLASS:
            head.id = FUNC_2_CLASS[func][0]
            command = ID_2_PROTOCOL[head.id]()
            index = 0
            for index in xrange(len(FUNC_2_CLASS[func][1])):
                setattr(command, FUNC_2_CLASS[func][1][index], args[0][index])
            head.string = command.SerializeToString()
            string = head.SerializePartialToString()
            self.transfer.write(string)

    def fromRemote(self, string):
        head = Message.Head()
        head.ParseFromString(string)
        if head.id in self.map:
            command = self.map[head.id]()
            command.ParseFromString(head.string)
            self.proxy.onEvent(command)

