import json
from lib.core.settings import DEFAULT_CONFIG_PATH
from lib.core.common import file_is_exits
from lib.core.log import logger

def inject_headers(header = {}, data = None):
    costum = config()
    for key in list(costum.keys()):
        if key.encode() in header:
            del costum[key]
            continue
    return costum

def inject_request():
    #TODO
    return

def config():
    if not file_is_exits(DEFAULT_CONFIG_PATH + '/header.json'):
        logger.error('config/header.json配置文件不存在')
        return {}
    with open(DEFAULT_CONFIG_PATH + '/header.json') as f:
        data = json.load(f)
    return data