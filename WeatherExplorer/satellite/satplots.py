import functools
from datetime import datetime

import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import netCDF4 as nc

from WeatherExplorer.satellite import satdata

thredds_opendap_base_url = 'http://thredds.ucar.edu/thredds/dodsC/satellite'

cmaps = {
    'VIS': 'gray_r',
    'IR': 'inferno'
}


def gini_opendap(sattype, sector, cmap=None, timestamp=None):
    if timestamp is None:
        raise NotImplementedError('TODO')
    else:
        full_url = _get_url(sattype, sector, timestamp)

    ds = nc.Dataset(full_url)
    data = satdata.GiniSatelliteData(ds, sattype)
    plotter = GiniSatellitePlotter(data)
    return functools.partial(plotter.plot, cmap=_getcmap(sattype) if cmap is None else cmap)


def _getcmap(sattype):
    return cmaps[sattype.upper()]


def _getres(sattype):
    sattype = sattype.upper()
    if sattype == 'VIS':
        return '1km'
    elif sattype == 'IR':
        return '4km'
    else:
        return '8km'


def _get_url(sattype, sector, timestamp):
    datestr = timestamp.date().strftime('%Y%m%d')
    timestr = timestamp.time().strftime('%H%M')
    relpath = '/{sattype}/{sector}_{res}/{date}/{sector}_{res}_{sattype}_{date}_{time}.gini'.format(
        sattype=sattype.upper(),
        sector=sector.upper(),
        res=_getres(sattype),
        date=datestr, time=timestr)
    return thredds_opendap_base_url + relpath


class GiniSatellitePlotter(object):
    def __init__(self, data):
        self._globe = ccrs.Globe(ellipse='sphere', semimajor_axis=data.earth_radius,
                                 semiminor_axis=data.earth_radius)

        ctrlcoords = data.orig
        self._proj = ccrs.LambertConformal(central_latitude=ctrlcoords[0], central_longitude=ctrlcoords[1],
                                           standard_parallels=data.std_parallels, globe=self._globe)

        self._plotdata = data.plotdata
        self._extent = (data.minx, data.maxx, data.miny, data.maxy)

    def plot(self, cmap):
        ax = plt.axes(projection=self._proj)
        ax.imshow(self._plotdata, extent=self._extent, origin='upper', cmap=cmap)
        ax.coastlines(resolution='50m', color='black', linewidth='1')
        # ax.add_feature(cfeat.BORDERS, linewidth='2', edgecolor='black')
        ax.gridlines()
        plt.show()


x = gini_opendap('ir', 'WEST-CONUS', timestamp=datetime(year=2016, month=10, day=30, hour=18, minute=30))
x()