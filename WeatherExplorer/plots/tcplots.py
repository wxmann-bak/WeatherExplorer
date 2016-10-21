# -*- coding: utf-8 -*-
from datetime import timedelta

import matplotlib.pyplot as plt

from WeatherExplorer import tcdata


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


def plot_on_map(map_area, title, storms, only_classifiable=True, **kwargs):
    m = map_area.make_map()
    storms_to_plot = (storms,) if isinstance(storms, tcdata.StormHistory) else storms
    for storm in storms_to_plot:
        exact_storm = storm.classifiable() if only_classifiable else storm
        all_lat = [datapoint.lat for datapoint in exact_storm]
        all_lon = [datapoint.lon for datapoint in exact_storm]
        x, y = m(all_lon, all_lat)
        m.plot(x, y, **kwargs)
    if title:
        plt.title(title)
    plt.show()