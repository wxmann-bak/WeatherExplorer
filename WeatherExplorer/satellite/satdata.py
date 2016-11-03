import numpy as np

_KM_TO_M_MULTIPLIER = 1000


def _pixel_to_temp(pixel):
    if pixel >= 176:
        tempK = 418. - pixel
    else:
        tempK = 330 - (pixel / 2.)
    return tempK - 273.15


class GiniSatelliteData(object):
    def __init__(self, dataset, sattype):
        self._sattype = sattype.upper()
        self._alldata = dataset
        self._plotdata = dataset.variables[self._sattype][0]
        self._x = dataset.variables['x'][:]
        self._y = dataset.variables['y'][:]
        self._geog = dataset.variables['LambertConformal']
        self._R_earth = self._geog.earth_radius
        self._orig = (self._geog.latitude_of_projection_origin, self._geog.longitude_of_central_meridian)
        self._std_parallel = self._geog.standard_parallel

    @property
    def pixels(self):
        return self._plotdata & 0xff

    @property
    def brightness_temps(self):
        conversion = np.vectorize(_pixel_to_temp, otypes=[np.float])
        return conversion(self.pixels)

    @property
    def minx(self):
        return min(self._x) * _KM_TO_M_MULTIPLIER

    @property
    def maxx(self):
        return max(self._x) * _KM_TO_M_MULTIPLIER

    @property
    def miny(self):
        return min(self._y) * _KM_TO_M_MULTIPLIER

    @property
    def maxy(self):
        return max(self._y) * _KM_TO_M_MULTIPLIER

    @property
    def proj(self):
        return 'LambertConformal'

    @property
    def earth_radius(self):
        return self._R_earth

    @property
    def orig(self):
        return self._orig

    @property
    def std_parallels(self):
        return tuple([self._std_parallel])