from collections import namedtuple

__author__ = 'tangz'


def years(begin=None, end=None, eq=None):
    def _yr_func(datapoint):
        if eq:
            return datapoint.storm.year == eq or datapoint.storm.year in eq
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


def storm(year, name=None, number=None):
    def _storm_fn(datapoint):
        if name is None and number is None:
            raise ValueError('Need either a name or a number of a storm')
        if name is None:
            return datapoint.storm.number == number and datapoint.storm.year == year
        else:
            return datapoint.storm.name == name.upper() and datapoint.storm.year == year
    return _storm_fn


_SSHS_CATEGORIES = {1: 65, 2: 85, 3: 100, 4: 115, 5: 140}

def sshws_category(at_least):
    def _sshws_cat_fn(datapoint):
        if at_least not in _SSHS_CATEGORIES:
            raise ValueError('Invalid saffir-simpson category: ' + str(at_least))
        return datapoint.windspd >= _SSHS_CATEGORIES[at_least]
    return _sshws_cat_fn


Strength = namedtuple('Strength', 'td ts hu mh')
_td = statuses('TD', 'TS', 'HU')
_ts = statuses('TS', 'HU')
_hu = statuses('HU')
_mh = sshws_category(3)
strength = Strength(td=_td, ts=_ts, hu=_hu, mh=_mh)

istropical = _td


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