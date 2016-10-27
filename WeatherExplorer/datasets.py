import netCDF4 as nc
from WeatherExplorer import calculations

__author__ = 'tangz'


def ncep_nomads(url):
    dataset = nc.Dataset(url)
    return GradsDataset(dataset)


class GradsDataset(object):
    def __init__(self, data):
        self._data = data
        self._lats = data.variables['lat'][:]
        self._lons = data.variables['lon'][:]
        units = data.variables['time'].units
        self._times = [nc.num2date(x, units) for x in data.variables['time']]
        self._lvls = data.variables['lev'][:]

    @property
    def lats(self):
        return self._lats

    @property
    def lons(self):
        return self._lons

    @property
    def times(self):
        return self._times

    @property
    def plevels(self):
        return self._lvls

    def var(self, varname):
        vardata = self._data.variables[varname]
        plevel_aware = 'lev' in vardata.dimensions
        time_aware = 'time' in vardata.dimensions
        latlon_aware = 'lat' in vardata.dimensions and 'lon' in vardata.dimensions
        return _VarWrapper(vardata[:], self,
                           time_aware=time_aware,
                           plevel_aware=plevel_aware,
                           latlon_aware=latlon_aware)


class _VarWrapper(object):
    def __init__(self, vardata, parent, time_aware=True, latlon_aware=True, plevel_aware=True):
        self._parent = parent
        self._vardata = vardata
        self._time_aware = time_aware
        self._latlon_aware = latlon_aware
        self._plevel_aware = plevel_aware

    def values(self, time=None, lev=None, latlon=None):
        data_to_return = self._vardata
        if self._time_aware and time is not None:
            data_to_return = data_to_return[self._parent.times.index(time)]
            if self._plevel_aware and lev is not None:
                data_to_return = data_to_return[self._parent.plevels.tolist().index(lev)]
                if self._latlon_aware and latlon is not None:
                    all_latlons = [(lat, lon) for lat in self._parent.lats for lon in self._parent.lons]
                    closest = calculations.closest_node(latlon, all_latlons)
                    closest_lat, closest_lon = closest[0], closest[1]
                    data_to_return = data_to_return[closest_lon][closest_lat]
        return data_to_return