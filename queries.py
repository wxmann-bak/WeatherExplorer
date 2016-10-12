__author__ = 'tangz'


def years(begin=None, end=None, specific=None):
    if specific:
        return lambda btpoint: btpoint.storm.year in specific
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


def storm(year, name=None, number=None):
    year_fn = lambda btpoint: btpoint.storm.year == year
    if name is None and number is None:
        raise ValueError('Need either a name or a number of a storm')
    if name is None:
        return lambda btpt: btpt.storm.number == number and year_fn(btpt)
    else:
        return lambda btpt: btpt.storm.name == name.upper and year_fn(btpt)
