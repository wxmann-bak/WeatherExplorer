from collections import namedtuple
from operator import attrgetter

from WeatherExplorer.base import BaseCollection, LazyEvalResultSet

from WeatherExplorer.tcutils import sshs_category


__author__ = 'tangz'

_NEED_TO_IMPLEMENT_THIS_MSG = 'Subclass needs to implement this'


class StormRetrievable(object):
    def get_tc(self, year, name=None, number=None):
        raise NotImplementedError(_NEED_TO_IMPLEMENT_THIS_MSG)


class BasinHistory(BaseCollection, StormRetrievable):
    def __init__(self, basin, storms):
        BaseCollection.__init__(self, storms)
        self._basin = basin
        self._storms_by_year = BasinHistory._index_storms_by_year(storms)

    @staticmethod
    def _index_storms_by_year(storms):
        year_map = {}
        for storm in storms:
            yr = storm.year
            if yr not in year_map:
                year_map[yr] = []
            year_map[yr].append(storm)
        return year_map

    @property
    def basin(self):
        return self._basin

    def query(self, queryfunc):
        return _BasinQueryResult(self, queryfunc)

    def get_tc(self, year, name=None, number=None):
        if year is None:
            raise ValueError('Must supply a year')
        elif name is None and number is None:
            raise ValueError('Must supply either a name or a number for a storm')
        return self._get_tc_from_params(name, number, year)

    def _get_tc_from_params(self, name, number, year):
        if year not in self._storms_by_year:
            return None
        storms_for_year = self._storms_by_year[year]
        for storm in storms_for_year:
            if name is not None and storm.name == name.upper() and storm.year == year:
                return storm
            elif number is not None and storm.number == number and storm.year == year:
                return storm
        return None


class _BasinQueryResult(LazyEvalResultSet, StormRetrievable):
    def __init__(self, basin_hist, queryfn):
        LazyEvalResultSet.__init__(self, basin_hist, queryfn)

    def _new_instance(self, queryfn):
        return _BasinQueryResult(self.source, queryfn)

    def get_tc(self, year, name=None, number=None):
        possible_tc = self.source.get_tc(year, name, number)
        return possible_tc if self._queryfn(possible_tc) else None


class StormHistory(object):
    @classmethod
    def from_hurdat_points(cls, datapoints):
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
        stormid = all_storms.pop()
        return cls(stormid, all_points)

    def __init__(self, stormid, pts):
        self._stormid = stormid
        self._pts = pts
        # self._time_key_map = {}

    # def _build_time_key_map(self):
    #     for pt in self._pts:
    #         self._time_key_map[pt.timestamp] = pt

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
    def longevity(self):
        return self.last.timestamp - self.first.timestamp

    @property
    def max_wind_speed(self):
        return max([pt.windspd for pt in self._pts])

    @property
    def min_ctrl_pres(self):
        return min([pt.pres for pt in self._pts])

    @property
    def max_sshs_category(self):
        hu_windspds = [pt.windspd for pt in self._pts if pt.status == 'HU']
        return sshs_category(max(hu_windspds)) if hu_windspds else -1

    @property
    def lifecycle(self):
        statuses = []
        for datapoint in self:
            if not statuses or statuses[-1] != datapoint.status:
                statuses.append(datapoint.status)
        return tuple(statuses)

    def classifiable(self):
        classified_pts = [pt for pt in self._pts if pt.status in ('HU', 'TS', 'TD', 'SS', 'SD')]
        return StormHistory.from_hurdat_points(classified_pts)

    def slice(self, slice_fn):
        on_slice = False
        slice_on = []
        slices = []
        for pt in self:
            if slice_fn(pt):
                slice_on.append(pt)
                on_slice = True
            else:
                if on_slice:
                    slices.append(slice_on)
                    slice_on = []
                on_slice = False
        if slice_on:
            slices.append(slice_on)
        return tuple([StormHistory(self._stormid, section) for section in slices])

    def __iter__(self):
        return iter(self._pts)

    def __len__(self):
        return len(self._pts)


StormId = namedtuple('StormId', 'basin number year name raw')
BestTrackPoint = namedtuple('BestTrackPoint', 'storm timestamp ident status lat lon windspd pres')
# Location = namedtuple('Location', 'lat lon')
