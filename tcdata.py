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

    def query(self, queryfunc):
        return _BasinHistoryView(self, queryfunc)

    def __len__(self):
        return len(self._pts)

    def __iter__(self):
        return iter(self._pts)

    def __add__(self, pt):
        self._pts.append(pt)
        return self


class _BasinHistoryView(object):
    def __init__(self, basin_hist, queryfunc):
        self._original_pts = (pt for pt in basin_hist)
        self._query = queryfunc
        self._saved_pts = []

    def query(self, queryfunc):
        self._query = lambda x: self._query(x) and queryfunc(x)
        self._saved_pts = []
        return self

    def _cache_pts_if_needed(self):
        if not self._saved_pts:
            self._saved_pts = [pt for pt in self._original_pts if self._query(pt)]

    def __len__(self):
        self._cache_pts_if_needed()
        return len(self._saved_pts)

    def __iter__(self):
        self._cache_pts_if_needed()
        return iter(self._saved_pts)


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
