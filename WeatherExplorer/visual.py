# -*- coding: utf-8 -*-
from datetime import timedelta

import matplotlib.pyplot as plt


def _days_from_init(pt, t0):
    dt = pt.timestamp - t0
    return dt / timedelta(days=1)


def plot_storm_windspeed(storms_to_plot, **kwargs):
    def _plot_single_storm(storm, **kwargs):
        time_pts = []
        intensity_pts = []
        t0 = storm.first.timestamp

        for datapoint in storm:
            time_pts.append(_days_from_init(datapoint, t0))
            intensity_pts.append(datapoint.windspd)

        plt.ylabel('Storm Intensity (kts)')
        plt.xlabel('Number of days after being initially classified')
        plt.plot(time_pts, intensity_pts, **kwargs)

    for storm in storms_to_plot:
        _plot_single_storm(storm, **kwargs)
