__author__ = 'tangz'


def years(begin=None, end=None, years=None):
    if years:
        return lambda btpoint: btpoint.storm.year in years
    else:
        if begin and end:
            return lambda btpoint: begin <= btpoint.storm.year <= end
        elif begin:
            return lambda btpoint: begin <= btpoint.storm.year
        elif end:
            return lambda btpoint: btpoint.storm.year <= end
        raise ValueError("Need some valid input into years function")


def statuses(*args):
    return lambda btpoint: btpoint.status in args

named_storm = statuses('TS', 'HU')


def storm(name, year=None, basin=None):
    if year is None:
        year_fn = lambda btpoint: True
    else:
        year_fn = lambda btpoint: btpoint.storm.year == year
    if basin is None:
        basin_fn = lambda btpoint: True
    else:
        basin_fn = lambda btpoint: btpoint.storm.basin == basin
    return lambda btpoint: btpoint.storm.name == name.upper() and year_fn(btpoint) and basin_fn(btpoint)
