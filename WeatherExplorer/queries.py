import operator

from WeatherExplorer import calculations


__author__ = 'tangz'


class QueryBuilder(object):
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


year = QueryBuilder(lambda storm: storm.year)
lifecycle = QueryBuilder(lambda storm: storm.lifecycle)
ishurricane = lifecycle.contains('HU')
istropical = lifecycle.contains('HU', 'TS', 'TD')
issubtropical = allof(lifecycle.contains('SS', 'SD'), noneof(istropical))
max_intensity = QueryBuilder(lambda storm: storm.max_wind_speed)
min_pres = QueryBuilder(lambda storm: storm.min_ctrl_pres)
sshs_category = QueryBuilder(lambda storm: storm.max_sshs_category)
ismajor = sshs_category.geq(3)


def _min_dist_from(latlonpt, storm):
    distances = [calculations.dist(latlonpt, (storm_pt.lat, storm_pt.lon)) for storm_pt in storm]
    return min(distances)


def distfrom(latlonpt):
    return QueryBuilder(lambda storm: _min_dist_from(latlonpt, storm))
    # TODO: figure out why partials don't work in this case.
    # return Query(functools.partial(_min_dist_from, latlonpt=latlonpt))