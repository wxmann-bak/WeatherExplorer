import netCDF4 as nc

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
        return _VarWrapper(vardata, self,
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

    @property
    def wrapped(self):
        return self._vardata

    def _indices(self, time, lev, latlon):
        timeindex, levindex, latindex, lonindex = None, None, None, None
        if time is not None:
            timeindex = self._parent.times.index(time)
        if lev is not None:
            levindex = self._parent.plevels.tolist().index(lev)
        if latlon is not None:
            lat, lon = latlon[0], latlon[1]
            latindex = self._parent.lats.tolist().index(lat)
            lonindex = self._parent.lons.tolist().index(lon)
        return timeindex, levindex, latindex, lonindex

    def values(self, time=None, lev=None, latlon=None):
        usetime = self._time_aware and time is not None
        uselev = self._plevel_aware and lev is not None
        uselatlon = self._latlon_aware and latlon is not None

        timeindex, levindex, latindex, lonindex = self._indices(time, lev, latlon)

        if usetime:
            if uselev:
                if uselatlon:
                    return self._vardata[timeindex][levindex][latindex][lonindex]
                else:
                    return self._vardata[timeindex][levindex]
            elif uselatlon:
                return self._vardata[timeindex][:][latindex][lonindex]
            else:
                return self._vardata[timeindex]
        elif uselev:
            if uselatlon:
                return self._vardata[:][levindex][latindex][lonindex]
            else:
                return self._vardata[:][levindex]
        elif uselatlon:
            return self._vardata[:][:][latindex][lonindex]
        else:
            return self._vardata[:]
