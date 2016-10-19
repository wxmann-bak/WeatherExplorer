import sys

import load


__author__ = 'tangz'


wb = ()

ATLANTIC_FILE = 'data/hurdat2-1851-2015-070616.txt'

ATLANTIC_FILE_BRIEF = 'data/hurdat2-2000-2006.txt'


def main():
    global wb
    if sys.argv[1] == '--atlantic':
        wb = load.hurdat2(ATLANTIC_FILE)


if __name__ == '__main__':
    main()
