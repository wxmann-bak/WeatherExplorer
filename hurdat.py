import filters
import load

__author__ = 'tangz'

file = 'hurdat2-1851-2015-070616.txt'


def main():
    all_hurdat = load.hurdat2(file)
    kat = all_hurdat.subset(filters.years(begin=2013, end=2013))
    for bt_pt in kat:
        print(bt_pt)


if __name__ == '__main__':
    main()
