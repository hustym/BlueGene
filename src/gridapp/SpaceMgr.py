# coding: utf-8
#!/usr/bin/python

import bisect


import Proxy
import Entity
import Protocol

class Chunk(object):

    def __init__(self, x, y):
        self.position = x, y
        self.entities = {}

    def addEntity(self, entity):
        self.entities[entity.id] = entity
        self.broadcast(entity, Protocol.enterWorld)

    def removeEntity(self, entity):
        del self.entities[entity.id]
        self.broadcast(entity, Protocol.leaveWorld)

    def broadcast(self, entity, msg):
        for entity in self.entities:
            if isinstance( entity, Proxy):
                entity.talk(msg)


class NoneChunk(Chunk):
    pass


class Space(object):

    CHUNK_HEIGHT = 1024
    CHUNK_WIDTH  = 1024

    def __init__(self, x, y):
        self.chunks={}
        for i in xrange(x):
            for j in xrange(y):
                self.chunks[(x, y)] = Chunk(x, y)
        self.entities = {}

    def addEntity(self, entity):
        self.entities[entity.id] = entity
        self.getChunk(entity).addEntity(entity)

    def removeEntity(self, entity):     # 此处， 是否 entity的position 已经是新场景的position？
        del self.entities[entity.id]
        self.getChunk(entity).removeEntity(entity)

    def entityMove(self, entity, old_pos):
        if entity.position[0]/Space.CHUNK_WIDTH <> old_pos[0]/Space.CHUNK_WIDTH or \
            entity.position[1]/Space.CHUNK_HEIGHT <> old_pos[1]/Space.CHUNK_HEIGHT:
            self.getChunkByPos(old_chunk_pos).removeEntity(entity)
            self.getChunk(entity).addEntity(entity)
        self.getChunk(entity).broadcast(entity, Protocol.Position(entity))

    def getChunk(self, entity):
        return self.chunks.get([(entity.position[0]/Space.CHUNK_WIDTH, entity.position[1]/Space.CHUNK_HEIGHT)], NoneChunk())

    def getChunkByPos(self, pos):
        return self.chunks.get([(pos[0]/Space.CHUNK_WIDTH, pos[1]/Space.CHUNK_HEIGHT)], NoneChunk())

    def broadcast(self, entity, msg):
        for entity in self.entities:
            if isinstance(entity, Proxy):
                entity.talk(msg)
