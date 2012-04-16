# coding: utf-8
#!/usr/bin/python

import MySQLdb
import Storage

class MySql(Storage.Storage):

    def __init__(self, host, user, passwd, port = 3306, db = 'mysql'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.db_conn = MySQLdb.connect(host = host, user = user, passwd = passwd, port = port, db = db)
        self.db_cursor = self.db_conn.cursor()

        sql = 'select typeID, name from BlueGeneEntityTypes'
        self.executeRawCommand(sql, _initEntityTypes)

    def _initEntityTypes(self, dataset, affected, result):
        if error_code == 'OK':
            self.entity_types = {}
            for row in dataset:
                self.entity_types[row[0]]=row[1]
        else:
            raise 'dbmgr: init EntityTypes Failed'

    def setloginMapping(self, entity_id, onCompleteHandler):
        pass

    def executeRawCommand(self, sql, onCompleteHandler):
        try:
            affected = self.db_cursor.execute(sql)
            dataset = self.db_cursor.fetchall()
            result = 'ok'
        except:
            affected = 0
            dataset = []
            result = 'failed'
        onCompleteHandler(dataset, affected, result)

    def putEntity(self, entity_type, entity_id, entity, onCompleteHandler):
        try:
            assert isinstance(entity, list)
            onCompleteHanlder('ok')
        except:
            print 'MySQL putEntity error'
            onCompleteHanlder('failed')

    def getEntity(self, entity_type, entity_id, onCompleteHandler):
        try:
            onCompleteHanlder(entity, 'ok')
        except:
            print 'MySQL getEntity error'
            onCompleteHanlder([], 'failed')

    def delEntity(self, entity_type, entity_id, onCompleteHandler):
        onCompleteHanlder('ok')

    def putIDs(self, ids, onCompleteHanlder):
        pass

    def getIDs(self, nums, onCompleteHanlder):
        pass

