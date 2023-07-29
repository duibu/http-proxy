from lib.core.common import banner
from lib.parse.command import cmdLineParser
from lib.core.proxy_core import HttpProxy

def main():
    banner()
    args = cmdLineParser()
    HttpProxy().start()

if __name__ == '__main__':
    try:
        main()
    # except Exception as e:
    #     print(e)
    except KeyboardInterrupt:
        pass
    except SystemExit:
        raise