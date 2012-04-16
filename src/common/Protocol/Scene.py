# coding: utf-8
#!/usr/bin/python

import struct

ENTITY_POSITION = 0x0001
ENTER_WORLD     = 0x0002
LEAVE_WORLD     = 0x0003

class Position:
    def __init__(self, entity, type = ENTITY_POSITION):
        self.bfmt = "=HIII"
        self.type = type
        self.entity_id = entity.id
        self.x, self.y = entity.position

    def marshal(self):
        return struct.pack(self.bfmt, self.type, self.entity_id, self.x, self.y)

    def unmarshal(self, record):
        return struct.unpack(self.bfmt, self.type, self.entity_id, self.x, self.y)


class enterWorld(Position):
    def __init__(self, entity, type = ENTER_WORLD):
        super (enterScene, self).__init__(entity, type)


class leaveWorld:
    def __init__(self, entity, type = LEAVE_WORLD):
        self.bfmt = "=HI"
        self.type = type
        self.entity_id = entity.id

    def marshal(self):
        return struct.pack(self.bfmt, self.type, self.entity_id)

    def unmarshal(self, record):
        return struct.unpack(self.bfmt, self.type, self.entity_id)
