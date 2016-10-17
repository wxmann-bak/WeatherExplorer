import operator

import calculations


__author__ = 'tangz'


class Query(object):
    def __init__(self, accessor):
        self._accessor = accessor

    def _get_func(self, operation, value):
        def _func_to_return(inp):
            return operation(self._accessor(inp), value)
        return _func_to_return

    def _get_func_multiple_values(self, operation, values):
        def _func_to_return(inp):
            for value in values:
                if operation(self._accessor(inp), value):
                    return True
            return False
        return _func_to_return

    def lt(self, value):
        return self._get_func(operator.lt, value)

    def leq(self, value):
        return self._get_func(operator.le, value)

    def gt(self, value):
        return self._get_func(operator.gt, value)

    def geq(self, value):
        return self._get_func(operator.ge, value)

    def eq(self, *values):
        return self._get_func_multiple_values(operator.eq, values)

    def contains(self, *values):
        return self._get_func_multiple_values(operator.contains, values)

    def betw(self, lower, upper):
        return lambda inp: lower <= self._accessor(inp) <= upper

    def neq(self, value):
        return self._get_func(operator.ne, value)


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


def noneof(*queries):
    def _none_of(storm):
        for query in queries:
            if query(storm):
                return False
        return True

    return _none_of


class QueryingException(Exception):
    pass


year = Query(lambda storm: storm.year)
lifecycle = Query(lambda storm: storm.lifecycle)
ishurricane = lifecycle.contains('HU')
istropical = lifecycle.contains('HU', 'TS', 'TD')
issubtropical = allof(lifecycle.contains('SS', 'SD'), noneof(istropical))
max_intensity = Query(lambda storm: storm.max_wind_speed)
min_pres = Query(lambda storm: storm.min_ctrl_pres)

_SSHS_CATEGORIES = {1: 65, 2: 85, 3: 100, 4: 115, 5: 140}


def _sshs_cat(storm):
    if not ishurricane(storm):
        return -1
    elif storm.max_wind_speed >= _SSHS_CATEGORIES[5]:
        return 5
    else:
        for cat in range(1, 5):
            if _SSHS_CATEGORIES[cat] <= storm.max_wind_speed < _SSHS_CATEGORIES[cat + 1]:
                return cat
        raise QueryingException('Cannot find saffir-simpson category for windspeed: ' + storm.max_wind_speed)


sshs_category = Query(_sshs_cat)
ismajor = sshs_category.geq(3)


def _min_dist_from(latlonpt, storm):
    distances = [calculations.dist_mi(latlonpt, (storm_pt.lat, storm_pt.lon)) for storm_pt in storm]
    return min(distances)


def distfrom(latlonpt):
    return Query(lambda storm: _min_dist_from(latlonpt, storm))
    # TODO: figure out why partials don't work in this case.
    # return Query(functools.partial(_min_dist_from, latlonpt=latlonpt))