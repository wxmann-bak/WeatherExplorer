import load
import visual

__author__ = 'tangz'

file = 'hurdat2-1851-2015-070616.txt'


def main():
    all_hurdat = load.hurdat2(file)
    visual.plot_intensity(all_hurdat, 2005, 'Katrina')


if __name__ == '__main__':
    main()
