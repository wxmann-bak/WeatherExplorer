import queries
import load

__author__ = 'tangz'

file = 'hurdat2-1851-2015-070616.txt'


def main():
    all_hurdat = load.hurdat2(file)
    kat = all_hurdat.subset(queries.years(begin=2006, end=2015))
    for bt_pt in kat:
        print(bt_pt)


if __name__ == '__main__':
    main()
