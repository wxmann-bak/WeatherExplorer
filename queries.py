from collections import namedtuple

__author__ = 'tangz'


def years(*valid_years):
    return lambda storm: storm.year in valid_years


def statuses(*args):
    def _status_func(storm):
        for status in args:
            storm_statuses = storm.lifecycle
            if status in storm_statuses:
                return True
        return False
    return _status_func


_SSHS_CATEGORIES = {1: 65, 2: 85, 3: 100, 4: 115, 5: 140}

def sshs_category(cat):
    def _sshs_cat_fn(storm):
        if cat not in _SSHS_CATEGORIES:
            raise ValueError('Invalid saffir-simpson category: ' + str(cat))
        return storm.max_wind_speed >= _SSHS_CATEGORIES[cat] and ishurricane(storm)
    return _sshs_cat_fn


def allof(*queries):
    def _all_fn(storm):
        for query in queries:
            if not query(storm):
                return False
        return True
    return _all_fn


def anyof(*queries):
    def _any_of(storm):
        for query in queries:
            if query(storm):
                return True
        return False
    return _any_of


_tropical = ('TD', 'TS', 'HU')
_subtrop = ('SD', 'SS')

istropical = statuses(*_tropical)
issubtropical = lambda storm: statuses(*_subtrop)(storm) and not istropical(storm)
ishurricane = statuses('HU')
ismajor = sshs_category(3)