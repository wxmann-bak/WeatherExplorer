from mpl_toolkits.basemap import Basemap
import numpy as np


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

    def _negative_lon_workaround(self, coordinate):
        if coordinate[1] < 0:
            new_lon = 360 + coordinate[1]
            return coordinate[0], new_lon
        return coordinate[0], coordinate[1]

    def make_map(self):
        llcrnrlat, llcrnlon = self._negative_lon_workaround(self._ll_coords)
        urcrnlat, urcrnlon = self._negative_lon_workaround(self._ur_coords)
        m = Basemap(projection=self._projection, llcrnrlon=llcrnlon, llcrnrlat=llcrnrlat,
                    urcrnrlon=urcrnlon, urcrnrlat=urcrnlat, resolution=self.resolution)
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()
        m.drawparallels(np.arange(-90, 90, self.dlat_labels), labels=[1, 0, 0, 1])
        m.drawmeridians(np.arange(0, 360, self.dlon_labels), labels=[1, 0, 0, 1])
        return m


atlantic_basin = MapArea('cyl', (5.0, -105.0), (60.0, -5.0), 10, 15)