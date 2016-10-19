from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

import numpy as np
import tcdata

__author__ = 'tangz'


class MapArea(object):
    @classmethod
    def centered(cls, loc, lat_delta=10, lon_delta=10, projection='cyl', resolution='i'):
        ll_coords = (loc[0] - lat_delta, loc[1] - lon_delta)
        ur_coords = (loc[0] + lat_delta, loc[1] + lon_delta)
        dlat_labels = lat_delta / 2
        dlon_labels = lon_delta / 2
        return cls(projection, ll_coords, ur_coords, dlat_labels, dlon_labels, resolution)

    def __init__(self, projection, ll_coords, ur_coords, dlat_labels, dlon_labels, resolution='l'):
        self._projection = projection
        self._ll_coords = ll_coords
        self._ur_coords = ur_coords
        self.dlat_labels = dlat_labels
        self.dlon_labels = dlon_labels
        self.resolution = resolution

    def draw_map(self):
        m = Basemap(projection=self._projection, llcrnrlon=self._ll_coords[1], llcrnrlat=self._ll_coords[0],
                    urcrnrlon=self._ur_coords[1], urcrnrlat=self._ur_coords[0], resolution=self.resolution)
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()
        m.drawparallels(np.arange(-90, 90, self.dlat_labels), labels=[1, 0, 0, 1])
        m.drawmeridians(np.arange(-360, 360, self.dlon_labels), labels=[1, 0, 0, 1])
        return m


atlantic_basin = MapArea('cyl', (5.0, -105.0), (60.0, -5.0), 10, 15)


def plot_on_map(map_area, title, storms, **kwargs):
    m = map_area.draw_map()
    storms_to_plot = (storms,) if isinstance(storms, tcdata.StormHistory) else storms
    for storm in storms_to_plot:
        all_lat = [datapoint.lat for datapoint in storm.classifiable()]
        all_lon = [datapoint.lon for datapoint in storm.classifiable()]
        x, y = m(all_lon, all_lat)
        m.plot(x, y, **kwargs)
    if title:
        plt.title(title)
    plt.show()