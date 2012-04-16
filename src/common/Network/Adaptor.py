# coding: utf-8
#!/usr/bin/python

POSITON     = 0x0001
ENTER_WORLD = 0x0002
LEAVE_WORLD = 0x0003


import Message

class EventServer(object):

    def __init__(self):
        self.object_map = {}
        self.object_map[POSITON] = Message.Position
        self.object_map[ENTER_WORLD] = Message.EnterWorld
        self.object_map[LEAVE_WORLD] = Message.LeaveWorld

        self.id_map = {}
        self.id_map[Message.Position] = POSITON
        self.id_map[Message.EnterWorld] = ENTER_WORLD
        self.id_map[Message.LeaveWorld] = LEAVE_WORLD


        self.observer = {}

    def registerProtocol(self, message_id, protocol):
        self.object_map[message_id] = protocol
        self.id_map[protocol] = message_id

    def registerEvent(self, proxy, message):
        if proxy in self.observer:
            self.observer[proxy].add(message)
        else:
            self.observer[proxy] = set([message,])

    def unregisterEvent(self, proxy, message):
        self.observer.get(proxy, set([]).pop(message))

    def parseFromString(self, string):
        head = Message.Head()
        head.ParseFromString(string)
        object = head[head.id]()
        object.ParseFromString(head.string)
        return object

    def serializeToString(self, object):
        head = Message.Head()
        head.id = self.id_map[object]
        head.string = object.SerializeToString()
        return head.SerializeToString()

g_adaptor = Adaptor()