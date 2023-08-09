import sys

from argparse import ArgumentParser
from argparse import ArgumentError

def cmdLineParser(argv=None):

    if not argv:
        argv = sys.argv

    parser = ArgumentParser()

    try:

        parser.add_argument("--host", dest="host", type = str, default = '127.0.0.1',
            help="代理IP地址  (e.g. \"127.0.0.1\")")

        parser.add_argument("--port", dest="port", type = int, default = 8372,
            help="代理监听端口  (e.g. 8372)")

        parser.add_argument("--listen", dest="listen", type = int, default = 10,
            help="监听客户端数量,默认10  (e.g. 10)")
        
        parser.add_argument("--buf", dest="buf", type = int, default = 8,
            help="缓存区大小,默认8kb  (e.g. 8)")
        
        parser.add_argument("--delay", dest="delay", type = int, default = 1,
            help="延时时间,单位ms,默认1ms  (e.g. 1)")

        args = parser.parse_args()


        return args
    except Exception as e:
        print(e)