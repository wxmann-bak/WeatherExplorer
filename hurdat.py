import load

__author__ = 'tangz'

file = 'hurdat2-1851-2015-070616.txt'


def main():
    all_hurdat = load.hurdat2(file)
    for storm in all_hurdat:
        for bt_pt in storm:
            print(bt_pt)


if __name__ == '__main__':
    main()
