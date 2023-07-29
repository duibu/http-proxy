import sys

from argparse import ArgumentParser
from argparse import ArgumentError
import argparse

from lib.core.settings import IS_WIN

def cmdLineParser(argv=None):

    if not argv:
        argv = sys.argv

    # Reference: https://stackoverflow.com/a/4012683 (Note: previously used "...sys.getfilesystemencoding() or UNICODE_ENCODING")
    # _ = getUnicode(os.path.basename(argv[0]), encoding=sys.stdin.encoding)

    parser = ArgumentParser()

    try:

        parser.add_argument("--thread", dest="thread", type = int, default = 1,
            help="Thread number  (e.g. \"5\")")

        args = parser.parse_args()


        return args
    except Exception as e:
        print(e)