import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from cartopy import crs as ccrs, feature as cfeat

basemap = 'basemap'
cartopy = 'cartopy'


class MapProjection(object):
    _basemap_res = {
        'low': 'c',
        'medium': 'l',
        'high': 'h'
    }

    _cartopy_res = {
        'low': '110m',
        'medium': '50m',
        'high': '10m'
    }

    lib_unavailable_msg = "{} library unavailable: must install it or try with a different library."

    def __init__(self):
        pass

    def draw_map(self, lib=basemap, res='medium'):
        if lib == basemap:
            return self._draw_basemap(res)
        elif lib == cartopy:
            return self._draw_cartopy(res)

    def _draw_basemap(self, res):
        m = self._basemap_object(res)
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()
        # TODO: draw lat/lon grids
        return m

    def _basemap_object(self, res):
        raise NotImplementedError("Basemap object creation must be implemented in subclasses")

    def _draw_cartopy(self, res):
        m = self._cartopy_object(res)
        res_str = MapProjection._cartopy_res[res]
        m.coastlines(resolution=res_str, color='black', linewidth='1')
        m.add_feature(cfeat.BORDERS, linewidth='1', edgecolor='black')
        states = cfeat.NaturalEarthFeature(category='cultural', name='admin_1_states_provinces_lakes',
                                           scale=res_str, facecolor='none')
        m.add_feature(states, linewidth='0.5')
        # TODO: draw lat/lon grids
        return m

    def _cartopy_object(self, res):
        raise NotImplementedError("Cartopy object creation must be implemented in subclasses")


class LambertConformalCartopy(MapProjection):
    def __init__(self, lat0, lon0, stdlat1, stdlat2=None, r_earth=6370997):
        MapProjection.__init__(self)
        self.lat0 = lat0
        self.lon0 = lon0
        self.stdlat1 = stdlat1
        self.stdlat2 = stdlat2
        self.r_earth = r_earth

    def draw_map(self, lib=cartopy, res='medium'):
        if lib == basemap:
            raise NotImplementedError("This instance of MapProjection does not support Basemap.")
        else:
            return super(LambertConformalCartopy, self).draw_map(lib, res)

    def _cartopy_object(self, res):
        globe = ccrs.Globe(ellipse='sphere', semimajor_axis=self.r_earth,
                           semiminor_axis=self.r_earth)
        stdparas = [self.stdlat1]
        if self.stdlat2 is not None:
            stdparas.append(self.stdlat2)
        proj = ccrs.LambertConformal(central_latitude=self.lat0, central_longitude=self.lon0,
                                     standard_parallels=stdparas, globe=globe)
        return plt.axes(projection=proj)
