from collections import namedtuple
from operator import attrgetter
import re
import queries

__author__ = 'tangz'


class Queryable(object):
    def query(self, queryfunc):
        raise NotImplementedError('Subclass must implement this')


class StormRetrievable(object):
    def storm(self, year, name=None, number=None):
        raise NotImplementedError('Subclass must implement this')


class BasinHistory(Queryable, StormRetrievable):
    def __init__(self, basin):
        self._basin = basin
        self._pts = []

    @property
    def basin(self):
        return self._basin

    def query(self, queryfunc):
        return _BasinHistoryView(self, queryfunc)

    def storm(self, year, name=None, number=None):
        datapoints = []
        for datapoint in self:
            if name is not None:
                if datapoint.storm.name == name.upper() and datapoint.storm.year == year:
                    datapoints.append(datapoint)
            elif number is not None:
                if datapoint.storm.number == number and datapoint.storm.year == year:
                    datapoints.append(datapoint)
            else:
                raise ValueError('Must supply either a name or a number for a storm')
        return StormHistory.from_hurdat_points(datapoints)

    def __len__(self):
        return len(self._pts)

    def __iter__(self):
        return iter(self._pts)

    def __add__(self, pt):
        self._pts.append(pt)
        return self


class StormHistory(Queryable):
    @staticmethod
    def from_hurdat_points(datapoints):
        if not datapoints:
            return None
        all_points = []
        all_storms = set()
        for datapoint in datapoints:
            all_points.append(datapoint)
            all_storms.add(datapoint.storm)
        if len(all_storms) != 1:
            raise ValueError('Invalid set of datapoints, more than one storm in set')
        all_points = sorted(all_points, key=attrgetter('timestamp'))
        stormhist = StormHistory(all_storms.pop())
        stormhist._pts = tuple(all_points)
        return stormhist

    def __init__(self, stormid):
        self._stormid = stormid
        self._pts = []

    def _check_contains_pts(self):
        if not self._pts:
            raise ValueError('Invalid storm history, empty points, for storm: ' + str(self._stormid))

    @property
    def name(self):
        return self._stormid.name

    @property
    def number(self):
        return self._stormid.number

    @property
    def year(self):
        return self._stormid.year

    @property
    def id(self):
        return self._stormid.raw

    @property
    def basin(self):
        return self._stormid.basin

    @property
    def first(self):
        self._check_contains_pts()
        return self._pts[0]

    @property
    def last(self):
        self._check_contains_pts()
        return self._pts[-1]

    @property
    def lifetime(self):
        return self.last.timestamp - self.first.timestamp

    def classifiable(self):
        classified_pts = [pt for pt in self._pts if queries.isclassifiable(pt)]
        return StormHistory.from_hurdat_points(classified_pts)

    def __iter__(self):
        return iter(self._pts)

    def query(self, queryfunc):
        filtered_pts = [pt for pt in self._pts if queryfunc(pt)]
        return _BasinHistoryView(filtered_pts, queryfunc)


class _BasinHistoryView(Queryable):
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