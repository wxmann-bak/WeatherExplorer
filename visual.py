# -*- coding: utf-8 -*-
from datetime import timedelta
from matplotlib import pylab
import matplotlib.pyplot as plt
import load
import queries


def _days_from_init(pt, t0):
    dt = pt.timestamp - t0
    return dt / timedelta(days=1)


def plot_storm_windspeed(storm_to_plot, **kwargs):
    time_pts = []
    intensity_pts = []
    t0 = storm_to_plot.first.timestamp

    for datapoint in storm_to_plot:
        time_pts.append(_days_from_init(datapoint, t0))
        intensity_pts.append(datapoint.windspd)

    plt.ylabel('Storm Intensity (kts)')
    plt.xlabel('Number of days after being initially classified')
    plt.plot(time_pts, intensity_pts, **kwargs)


all_hurdat = load.hurdat2('hurdat2-1851-2015-070616.txt')
first_year = 1960
last_year = 2015
last_decade = all_hurdat.query(queries.year_range(first_year, last_year))
    
matthew_storm = 'MATTHEW'
matthew = load.atcf('bal142016.dat', matthew_storm)

for storm in last_decade:
    plot_storm_windspeed(storm.classifiable(), color='blue', alpha=0.1, linewidth=0.5)
plot_storm_windspeed(matthew.classifiable(), color='red', linewidth=1)
plt.axis([0, 15, 10, 160])
plt.grid(True)
plt.title('Hurricane Matthew (Red) vs. \nAll Atlantic TCs {0}-{1}'.format(first_year, last_year))
pylab.savefig('matthew-{0}-{1}.png'.format(first_year, last_year), dpi=200, transparent=False)
