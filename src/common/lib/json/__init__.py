# -*- coding:utf-8 -*-

import json

def json_read( string ):
    try:
        return json.read( string )
    except:
        return {}

def json_write( dict ):
    try:
        return json.write( dict )
    except:
        return ""
