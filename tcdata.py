from collections import namedtuple
import operator

__author__ = 'tangz'


# class query(object):
#     @staticmethod
#     def where(**kwargs):
#         if 'status' in kwargs:
#
#     def __init__(self):
#         self.


class BasinHistory(object):
    def __init__(self, basin):
        self._status_indexed = {}
        self._year_indexed = {}
        self._month_indexed = {}
        self._basin = basin

    @property
    def basin(self):
        return self._basin

    def __add__(self, tc):
        for bt_pt in tc:
            timestamp = bt_pt.timestamp
            status = bt_pt.status
            year = timestamp.year
            month = timestamp.month

            BasinHistory._add_indexed(self._status_indexed, status, (tc, bt_pt))
            BasinHistory._add_indexed(self._year_indexed, year, (tc, bt_pt))
            BasinHistory._add_indexed(self._month_indexed, month, (tc, bt_pt))
        return self

    @staticmethod
    def _add_indexed(index_dict, elem_key, elem):
        if elem_key not in index_dict:
            index_dict[elem_key] = []
        index_dict[elem_key].append(elem)


BestTrackPoint = namedtuple('BestTrackPoint', 'timestamp ident status lat lon windspd pres')


class StormHistory(object):
    def __init__(self, basin, storm_number, year, storm_name):
        self._basin = basin
        self._storm_number = storm_number
        self._year = year
        self._storm_name = storm_name
        self._datapoints = []
        self._locked = False

    @property
    def basin(self):
        return self._basin

    @property
    def storm_number(self):
        return self._storm_number

    @property
    def storm_name(self):
        return self._storm_name

    @property
    def year(self):
        return self._year

    def __iter__(self):
        sorted_datapts = sorted(self._datapoints, key=operator.attrgetter('timestamp'))
        return iter(sorted_datapts)

    def __add__(self, datapt):
        if self._locked:
            raise NotImplementedError
        StormHistory._check_datapt(datapt)
        self._datapoints.append(datapt)
        return self

    def read_only(self):
        self._locked = True
        return self

    @staticmethod
    def _check_datapt(datapt):
        assert datapt.timestamp is not None
        assert datapt.status is not None
        assert datapt.lat is not None
        assert datapt.lon is not None
        assert datapt.windspd is not None
