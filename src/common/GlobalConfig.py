# coding: utf-8
#!/usr/bin/python

from xml.dom import minidom

class GlobalConfig(object):
    def __init__(self, config_file):
        self.config_file = config_file

    def parse(self):
        xmldoc = minidom.parse(filepath)     #load the xml file from localhost
        root = xmldoc.documentElement        #get the root element

        gamesvr = root.getElementsByTagName('gamesvr')
        for node in gamesvr:
            name = node.childNodes[1].firstChild.data.encode('gbk') #get the recever name
            ip = node.childNodes[3].firstChild.data                    #get the recever mail address
            port = node.childNodes[5].firstChild.data                  #get the checker name
            check_mail=node.childNodes[7].firstChild.data              #get the checker mail address
