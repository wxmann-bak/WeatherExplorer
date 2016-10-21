from WeatherExplorer import maps

#########################################################################
# Much of the code in this module is adapted from the samples found here:
# http://matplotlib.org/basemap/users/examples.html
#
# Many thanks to the MatplotLib community for their examples.
# This would not be possible with it.
#########################################################################

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import addcyclic
from scipy.ndimage.filters import minimum_filter, maximum_filter
from netCDF4 import Dataset


def extrema(mat, mode='wrap', window=10):
    """find the indices of local extrema (min and max)
    in the input array."""
    mn = minimum_filter(mat, size=window, mode=mode)
    mx = maximum_filter(mat, size=window, mode=mode)
    # (mat == mx) true if pixel is equal to the local max
    # (mat == mn) true if pixel is equal to the local in
    # Return the indices of the maxima, minima
    return np.nonzero(mat == mn), np.nonzero(mat == mx)


def plot_slp_extrema(map_obj, x, y, data, low_color='r', high_color='b', window=20):
    found_mins, found_maxes = extrema(data, mode='wrap', window=window)
    xlows, ylows = x[found_mins], y[found_mins]
    xhighs, yhighs = x[found_maxes], y[found_maxes]
    lowvals = data[found_mins]
    highvals = data[found_maxes]

    # don't plot if there is already a L or H within dmin meters.
    plabel_offset = 0.022 * (map_obj.ymax - map_obj.ymin)
    dmin = plabel_offset

    def r(pt1, pt2):
        return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    def plot_labels(xvals, yvals, extremavals, ident, label_color):
        xyplotted = []
        for xval, yval, extremaval in zip(xvals, yvals, extremavals):
            if map_obj.xmax > xval > map_obj.xmin and map_obj.ymax > yval > map_obj.ymin:
                dist = [r((xval, yval), point) for point in xyplotted]
                if not dist or min(dist) > dmin:
                    plt.text(xval, yval, ident, fontsize=14, fontweight='bold',
                             ha='center', va='center', color=label_color)
                    plt.text(xval, yval - plabel_offset, repr(int(extremaval)), fontsize=9,
                             ha='center', va='top', color=label_color,
                             bbox=dict(boxstyle="square", ec='None', fc=(1, 1, 1, 0.5)))
                    xyplotted.append((xval, yval))

    plot_labels(xlows, ylows, lowvals, 'L', low_color)
    plot_labels(xhighs, yhighs, highvals, 'H', high_color)


def to_hPa(pa):
    return pa * 0.01


class ModelOutput(object):
    def __init__(self, modeldata, area):
        self.area = area
        self._data = modeldata
        self._lats = modeldata.variables['lat'][:]
        self._lons = modeldata.variables['lon'][:]
        self._fignum = 1
        self._plotted_figs = []

    def _track_fig(self):
        while self._fignum in self._plotted_figs:
            self._fignum += 1
        self._plotted_figs.append(self._fignum)
        plt.figure(self._fignum)

    def saved(self, fig):
        if fig in self._plotted_figs:
            plt.figure(fig)
            plt.show()
        return None

    # the window parameter controls the number of highs and lows detected.
    # (higher value, fewer highs and lows)
    def mslp(self, contour_intrv, title, window=20):
        self._track_fig()
        prmsl = to_hPa(self._data.variables['prmslmsl'][0])

        m = self.area.make_map()
        # add wrap-around point in longitude.
        prmsl, lons = addcyclic(prmsl, self._lons)
        countour_lvls = np.arange(900, 1100., contour_intrv)
        lons, lats = np.meshgrid(lons, self._lats)
        x, y = m(lons, lats)
        m.contour(x, y, prmsl, countour_lvls, colors='k', linewidths=1.)
        plot_slp_extrema(m, x, y, prmsl, window=window)

        plt.title(title)
        plt.show()
        return self._fignum


#gfs = Dataset("http://nomads.ncep.noaa.gov:9090/dods/gfs_0p50/gfs20161020/gfs_0p50_12z")
#ModelOutput(gfs, maps.atlantic_basin).mslp(contour_intrv=2.5, title='MSLP 12Z GFS')