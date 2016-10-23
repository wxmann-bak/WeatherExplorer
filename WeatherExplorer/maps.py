from mpl_toolkits.basemap import Basemap
import numpy as np


__author__ = 'tangz'


def world_cyl(lonctr=0, dlat_labels=20, dlon_labels=20, resolution='l'):
    llcrnrlon, urcrnrlon = lonctr - 180, lonctr + 180
    llcrnrlat, urcrnrlat = -90, 90
    m = Basemap(projection='cyl', llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat,
                urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, resolution=resolution, area_thresh=1000)
    return MapWrapper(m, dlat_labels, dlon_labels, resolution)


def world_ortho(ctr, dlat_labels=20, dlon_labels=20, resolution='l'):
    m = Basemap(projection='ortho', lat_0=ctr[0], lon_0=ctr[1], area_thresh=1000)
    return MapWrapper(m, dlat_labels, dlon_labels, resolution)


def region_cyl(lowerleft, upperright, dlat_labels=10, dlon_labels=10, resolution='l'):
    llcrnrlon, urcrnrlon = lowerleft[1], upperright[1]
    llcrnrlat, urcrnrlat = lowerleft[0], upperright[0]
    m = Basemap(projection='cyl', llcrnrlon=llcrnrlon, llcrnrlat=llcrnrlat,
                urcrnrlon=urcrnrlon, urcrnrlat=urcrnrlat, resolution=resolution, area_thresh=1000)
    return MapWrapper(m, dlat_labels, dlon_labels, resolution)


def lcc(ctr, width, height, dlat_labels=10, dlon_labels=10, resolution='l'):
    m = Basemap(projection='lcc', lat_0=ctr[0], lon_0=ctr[1], width=width, height=height, resolution=resolution,
                area_thresh=1000)
    return MapWrapper(m, dlat_labels, dlon_labels, resolution)


def nhem(lon0, dlat_labels=20, dlon_labels=20, resolution='l'):
    m = Basemap(projection='npstere', lon_0=lon0, boundinglat=10, resolution=resolution, area_thresh=1000)
    return MapWrapper(m, dlat_labels, dlon_labels, resolution, draw_labels=False)


class MapWrapper(object):
    def __init__(self, m, dlat_labels=None, dlon_labels=None, resolution='l', draw_labels=True):
        self._map = m
        self.dlat_labels = dlat_labels
        self.dlon_labels = dlon_labels
        self.resolution = resolution
        self.draw_labels = draw_labels

    @property
    def map(self):
        return self._map

    def make_map(self):
        self._map.drawcoastlines()
        self._map.drawcountries()
        self._map.drawstates()
        if self.dlat_labels:
            labels = [1, 0, 0, 0] if self.draw_labels else [0, 0, 0, 0]
            self._map.drawparallels(np.arange(-90, 90, self.dlat_labels), labels=labels)
        if self.dlon_labels:
            labels = [0, 0, 0, 1] if self.draw_labels else [0, 0, 0, 0]
            self._map.drawmeridians(np.arange(-180, 180, self.dlon_labels), labels=labels)
        return self.map


atlantic_basin = region_cyl((5.0, -105.0), (60.0, -5.0), dlat_labels=10, dlon_labels=15)
north_america = lcc((45, -100), width=11000000, height=8500000, resolution='l')
nhem_us = nhem(-100)
conus = region_cyl((20, -130), (55, -65), dlat_labels=10, dlon_labels=10, resolution='i')