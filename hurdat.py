import load
import visual

__author__ = 'tangz'

# file = 'hurdat2-1851-2015-070616.txt'


def main():
    matthew_storm = 'MATTHEW'
    matthew = load.atcf('bal142016.dat', matthew_storm)
    for datapoint in matthew:
        print(datapoint)


if __name__ == '__main__':
    main()
