from collections import namedtuple

__author__ = 'tangz'


def years(begin=None, end=None, eq=None):
    def _yr_func(datapoint):
        if eq:
            return datapoint.storm.year in eq if hasattr(eq, '__iter__') else datapoint.storm.year == eq
        if begin and end:
            return begin <= datapoint.storm.year <= end
        elif begin:
            return begin <= datapoint.storm.year
        elif end:
            return datapoint.storm.year <= end
        raise ValueError("Need some valid input into years function")
    return _yr_func


def statuses(*args):
    return lambda datapoint: datapoint.status in args


_SSHS_CATEGORIES = {1: 65, 2: 85, 3: 100, 4: 115, 5: 140}

def sshws_category(at_least):
    def _sshws_cat_fn(datapoint):
        if at_least not in _SSHS_CATEGORIES:
            raise ValueError('Invalid saffir-simpson category: ' + str(at_least))
        return datapoint.windspd >= _SSHS_CATEGORIES[at_least]
    return _sshws_cat_fn


def allof(*queries):
    def _all_fn(datapoint):
        for query in queries:
            if not query(datapoint):
                return False
        return True
    return _all_fn


def anyof(*queries):
    def _any_of(datapoint):
        for query in queries:
            if query(datapoint):
                return True
        return False
    return _any_of


_tropical = ('TD', 'TS', 'HU')
_subtrop = ('SD', 'SS')

istropical = statuses(*_tropical)
issubtropical = statuses(*_subtrop)
isclassifiable = statuses(*(_tropical + _subtrop))
ishurricane = statuses('HU')
ismajor = sshws_category(3)