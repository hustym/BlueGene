# coding: utf-8
#!/usr/bin/python

import sys
import time
import logging

class Log(object):

    # 日志级别
    LOG_NOTSET   = logging.NOTSET
    LOG_DEBUG    = logging.DEBUG
    LOG_INFO     = logging.INFO
    LOG_WARNING  = logging.WARNING
    LOG_ERROR    = logging.ERROR
    LOG_CRITICAL = logging.CRITICAL

    PREFIX = {
           LOG_DEBUG    : "Debug:" ,\
           LOG_INFO     : "Info:",\
           LOG_WARNING  : "Warning:",\
           LOG_ERROR    : "Error:",\
           LOG_CRITICAL : "Critical:",\
           }

    def __init__(self, filename, format='%(asctime)s %(levelname)-12s %(message)s'):
        # 日志输出阈值，小于当前等级的，不输出
        self.filename = filename
        self.format = format
        self.level = Log.LOG_INFO
        logging.basicConfig(level=logging.DEBUG,
                    format=format, filename= filename, filemode='w')
        self.logger = logging.getLogger()

    def getLevelName(self, level):
        return Log.PREFIX.get(level, '')

    def setLevel(self, level):
        self.level = level

    def getText(self, desc, msg):
        return "[%s]  %s" % (desc, msg)

    def log(self, level, desc, msg, *args):
        if level < self.level:
            return
        print level, desc, msg, args
        self.logger.log(level, self.getText(desc, msg), *args)

    def debug(self, desc, msg, *args):
        self.logger.debug(self.getText(desc, msg), *args)

    def info(self, desc, msg, *args):
        self.logger.info(self.getText(desc, msg), *args)

    def warning(self, desc, msg, *args):
        self.logger.warning(self.getText(desc, msg), *args)

    warn = warning

    def error(self, desc, msg, *args):
        self.logger.error(self.getText(desc, msg), *args)

    def critical(self, desc, msg, *args):
        self.logger.critical(self.getText(desc, msg), *args)

    fatal = critical

    def exception(self, desc, msg, *args):
        self.logger.exception(self.getText(desc, msg), *args)

