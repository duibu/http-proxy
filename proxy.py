from lib.core.common import banner
from lib.parse.command import cmdLineParser
from lib.core.proxy_core import HttpProxy
from lib.core.init import init_all

def main():
    banner()
    init_all()
    args = cmdLineParser()
    HttpProxy(host=args.host, port=args.port, listen=args.listen, bufsize=args.buf, delay=args.delay).start()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        pass
    except SystemExit:
        raise