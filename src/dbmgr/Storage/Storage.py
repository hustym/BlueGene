# coding: utf-8
#!/usr/bin/python


class Storage(object):

    SUCCEED = 0
    DATABASE_ERROR = 1

    def __init__(self, host, user, passwd, port = 6379, db = 0):
        pass

    def setloginMapping(self, entity_id, onCompleteHandler):
        raise Exception("there is no implement of setloginMapping")

    def executeRawCommand(self, sql, onCompleteHandler):
        raise Exception("there is no implement of executeRawCommand")

    def putEntity(self, entity_type, entity_id, entity, onCompleteHandler):
        raise Exception("there is no implement of putEntity")

    def getEntity(self, entity_type, entity_id, onCompleteHandler):
        raise Exception("there is no implement of getEntity")

    def delEntity(self, entity_type, entity_id, onCompleteHandler):
        raise Exception("there is no implement of delEntity")

    def putIDs(self, ids, onCompleteHandler):
        raise Exception("there is no implement of putIDs")

    def getIDs(self, nums, onCompleteHandler):
        raise Exception("there is no implement of getIDs")
