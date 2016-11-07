#########################################################################
# Much of the code in this module is adapted from the samples found here:
# http://matplotlib.org/basemap/users/examples.html
#
# Many thanks to the MatplotLib community for their examples.
# This would not be possible with it.
#########################################################################
from datetime import timedelta

import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from mpl_toolkits.basemap import addcyclic

from WeatherExplorer import calculations


def plot_slp_extrema(map_obj, x, y, data, low_color='r', high_color='b', window=20):
    found_maxes, highvals = calculations.maxima(data, window=window)
    found_mins, lowvals = calculations.minima(data, window=window)
    xlows, ylows = x[found_mins], y[found_mins]
    xhighs, yhighs = x[found_maxes], y[found_maxes]
    # lowvals = data[found_mins]
    # highvals = data[found_maxes]

    # don't plot if there is already a L or H within dmin meters.
    plabel_offset = 0.015 * (map_obj.ymax - map_obj.ymin)
    dmin = plabel_offset * 2

    def r(pt1, pt2):
        return np.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)

    def plot_labels(xvals, yvals, extremavals, ident, label_color):
        xyplotted = []
        for xval, yval, extremaval in zip(xvals, yvals, extremavals):
            if map_obj.xmax > xval > map_obj.xmin and map_obj.ymax > yval > map_obj.ymin:
                dist = [r((xval, yval), point) for point in xyplotted]
                if not dist or min(dist) > dmin:
                    plt.text(xval, yval, ident, fontsize=18, fontweight='bold',
                             ha='center', va='center', color=label_color)
                    plt.text(xval, yval - plabel_offset, repr(int(extremaval)), fontsize=9,
                             ha='center', va='top', color=label_color,
                             bbox=dict(boxstyle="square", ec='None', fc=(1, 1, 1, 0.5)))
                    xyplotted.append((xval, yval))

    plot_labels(xlows, ylows, lowvals, 'L', low_color)
    plot_labels(xhighs, yhighs, highvals, 'H', high_color)


def pa_to_hPa(pa):
    return pa * 0.01


def gpm_to_dam(gpm):
    return gpm * 0.1


def to_mmhr(kgm2s1):
    return 3600 * kgm2s1
    # to inches: add * 0.03937


def to_in(kgm2):
    return kgm2 / 1000 * 39.3701


class CoardsNetcdfPlotter(object):
    def __init__(self, modeldata, maparea):
        self._maparea = maparea
        self._map = None
        self._data = modeldata
        self._map_drawn = False
        self._fignum = 1

    def newplot(self):
        self._map_drawn = False
        self._fignum += 1

    def _prune_geogr_data(self, plotdata):
        if not self._map:
            self._draw_init()
        # add wrap-around point in longitude.
        reviseddata, lons = addcyclic(plotdata, self._data.lons)
        lons, lats = np.meshgrid(lons, self._data.lats)
        # adjust longitude point mismatch for negative values in map
        lons, reviseddata = self._map.shiftdata(lons, datain=reviseddata)
        return lons, lats, reviseddata

    def _draw_init(self):
        if not self._map_drawn:
            plt.figure(self._fignum)
            self._map = self._maparea.draw_map()
            self._map_drawn = True

    def _abs_time(self, hrs_from_t0):
        t0 = self._data.times[0]
        t_targ = t0 + timedelta(hours=hrs_from_t0)
        return t_targ

    # the window parameter controls the number of highs and lows detected.
    # (higher value, fewer highs and lows)
    def mslp(self, hr=0, contour_delta=4, window=30):
        plotdata = pa_to_hPa(self._data.var('prmslmsl').values(time=self._abs_time(hr)))
        lons, lats, plotdata = self._prune_geogr_data(plotdata)

        self._draw_init()
        x, y = self._map(lons, lats)
        contour_lvls = np.arange(900, 1080., contour_delta)
        self._map.contour(lons, lats, plotdata, contour_lvls, colors='k', linewidths=1., transform=ccrs.PlateCarree())
        plot_slp_extrema(self._map, x, y, plotdata, window=window)

    def geoptnl_hgt(self, lev, hr=0, contour_delta=6):
        plotdata = gpm_to_dam(self._data.var('hgtprs').values(time=self._abs_time(hr), lev=lev))
        lons, lats, plotdata = self._prune_geogr_data(plotdata)

        mindata = np.amin(plotdata)
        maxdata = np.amax(plotdata)
        min_contour = contour_delta * (mindata // contour_delta)
        max_contour = contour_delta * (maxdata // contour_delta) + contour_delta
        contour_lvls = np.arange(min_contour, max_contour, contour_delta)

        self._draw_init()
        x, y = self._map(lons, lats)
        CS = self._map.contour(x, y, plotdata, contour_lvls, colors='k', linewidths=1.)
        plt.clabel(CS, contour_lvls, fontsize=9, fmt='%1.0f', inline_spacing=-3)

    def absvort(self, lev, hr=0):
        plotdata = self._data.var('absvprs').values(time=self._abs_time(hr), lev=lev)
        lons, lats, plotdata = self._prune_geogr_data(plotdata)

        self._draw_init()
        contour_lvls = np.arange(10e-5, 60e-5, 2e-5)
        x, y = self._map(lons, lats)
        self._map.contourf(x, y, plotdata, contour_lvls, cmap='hot_r', extend='both')

    # def precip_rate(self, hr=0):
    #     hrindex = self._hr_to_arrindex(hr)
    #     plotdata = to_mmhr(self._data.variables['pratesfc'][hrindex])
    #     lons, lats, plotdata = self._prune_geogr_data(plotdata)
    #
    #     self._draw_init()
    #     contour_lvls = np.arange(0.1, 18, 0.1)
    #     x, y = self._map(lons, lats)
    #     CS = self._map.contourf(x, y, plotdata, contour_lvls, cmap='RdYlGn_r', extend='max')
    #
    #     ticks = [min(contour_lvls)] + [i for i in range(1, int(max(contour_lvls)) + 1)]
    #     plt.colorbar(CS, ticks=ticks, label='Precipitation Rate (mm/hr)')

    def accum_precip(self, hr=0):
        plotdata = to_in(self._data.var('apcpsfc').values(time=self._abs_time(hr)))
        lons, lats, plotdata = self._prune_geogr_data(plotdata)

        self._draw_init()
        contour_lvls = np.arange(0.02, 3.6, 0.05)
        x, y = self._map(lons, lats)
        CS = self._map.contourf(x, y, plotdata, contour_lvls, cmap='RdYlGn_r', extend='max')

        ticks = [0.1, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
        plt.colorbar(CS, ticks=ticks, label='Precipitation Total (in)')