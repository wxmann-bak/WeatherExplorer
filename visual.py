# -*- coding: utf-8 -*-
from datetime import timedelta
import matplotlib.pyplot as plt
import load


def plot_intensity(basin_hist, year, name=None, number=None):
    storm_to_plot = basin_hist.tc(year, name, number).classifiable()
    time_pts = []
    intensity_pts = []
    t0 = storm_to_plot.first.timestamp

    def days_from_start(pt):
        dt = pt.timestamp - t0
        return dt / timedelta(days=1)

    for datapoint in storm_to_plot:
        time_pts.append(days_from_start(datapoint))
        intensity_pts.append(datapoint.windspd)

    plt.plot(time_pts, intensity_pts)

all_hurdat = load.hurdat2('hurdat2-2000-2006.txt')
plot_intensity(all_hurdat, 2005, 'Katrina')