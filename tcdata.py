from collections import namedtuple
import re

__author__ = 'tangz'


class BasinHistory(object):
    def __init__(self, basin):
        self._basin = basin
        self._pts = []

    @property
    def basin(self):
        return self._basin

    @property
    def datapoints(self):
        return tuple(self._pts)

    def subset(self, filter_func):
        return _BasinHistoryView(self, filter_func)

    def __iter__(self):
        return iter(self._pts)

    def __add__(self, pt):
        self._pts.append(pt)
        return self


class _BasinHistoryView(object):
    def __init__(self, basin_hist, filter_func):
        self._basin_hist = basin_hist
        self._filter = filter_func

    def __iter__(self):
        return iter((pt for pt in self._basin_hist if self._filter(pt)))


StormId = namedtuple('StormId', 'basin number year name raw')
BestTrackPoint = namedtuple('BestTrackPoint', 'storm timestamp ident status lat lon windspd pres')


def storm_id(raw, storm_name):
    matches = re.match(r'(\w{2})(\d{2})(\d{4})', raw)
    if matches:
        basin = matches.group(1)
        storm_number = int(matches.group(2))
        year = int(matches.group(3))
        return StormId(basin, storm_number, year, storm_name, raw)
    else:
        raise ValueError("Invalid TC information: " + raw)
