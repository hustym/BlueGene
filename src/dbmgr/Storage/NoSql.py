# coding: utf-8
#!/usr/bin/python

try:
    import cPickle as pickle
except:
    import pickle

import Storage
import redis

class NoSql(Storage.Storage):

    SUCCEED = 0
    DATABASE_ERROR = 1

    def __init__(self, host, user, passwd, port = 6379, db = 0):
        self.r = redis.StrictRedis(host=host, user=user, passwd=passwd, port=port, db=db)
        self.type_map = {}
        self.spare_ids = []
        self.max_id = 1
        # init type_map

    def _getIndex(self, entity_type, key):
        assert isinstance(key, int)
        entity_index = self.type_map[entity_type]
        index = (entity_index << 32) | key
        return index

    def setloginMapping(self, entity_id, onCompleteHanlder):
        pass

    def executeRawCommand(self, sql, onCompleteHanlder):
        raise Exception("nosql not support executeRawCommand")

    def putEntity(self, entity_type, entity_id, entity, onCompleteHanlder):
        try:
            assert isinstance(entity, list)
            index = self._getIndex(entity_index, entity_id)
            self.r.set(key, pickle.dumps(entity))
            onCompleteHanlder('ok')
        except:
            print 'NoSQL putEntity error'
            onCompleteHanlder('failed')

    def getEntity(self, entity_type, entity_id, onCompleteHanlder):
        try:
            index = self._getIndex(entity_index, entity_id)
            entity = pickle.loads( self.r.get(index) )
            onCompleteHanlder(entity, 'ok')
        except:
            print 'NoSQL getEntity error'
            onCompleteHanlder([], 'failed')

    def delEntity(self, entity_type, entity_id, onCompleteHanlder):
        index = self._getIndex(entity_index, entity_id)
        self.r.delete(index)
        onCompleteHanlder('ok')

    def putIDs(self, ids, onCompleteHanlder):
        # 维护一个空闲id列表
        # 将指定的id 植入空闲ids
        self.spare_ids.extend(ids)
        onCompleteHanlder('ok')

    def getIDs(self, nums, onCompleteHanlder):
        result = []
        if len(self.spare_ids) < nums:
            result = self.spare_ids[:]
            self.spare_ids = []
            for i in xrange(nums - len(spare_ids)):
                result.append(self.max_id)
                self.max_id += 1

            for i in xrange(5000):
                self.spare_ids.append(self.max_id)
                self.max_id += 1
        else:
            result = self.spare_ids[0:nums]
            self.spare_ids = self.spare_ids[nums:]

