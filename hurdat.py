import sys
import load
import tcdata

__author__ = 'tangz'

# __all__ = ['load_basin']
#
# _available_basins = """
# \n Valid basins:
# \n   * atlantic = ATLANTIC basin 1851-2015
# """
#
#
# def _log_error_message(msg):
#     print('ERROR: ' + msg)
#
#
# class _MissingBasinHook(tcdata.Queryable, tcdata.StormRetrievable):
#     _ERROR_MESSAGE = \
#         "Need to load data before running a query. Please execute load_basin(<basin_name>) first. " + _available_basins
#
#     def __init__(self):
#         pass
#
#     def query(self, queryfunc):
#         _log_error_message(_MissingBasinHook._ERROR_MESSAGE)
#
#     def get_tc(self, year, name=None, number=None):
#         _log_error_message(_MissingBasinHook._ERROR_MESSAGE)
#
#
wb = ()

_ATLANTIC_FILE = 'data/hurdat2-1851-2015-070616.txt'
#
#
# def load_basin(basin_str):
#     global wb
#     if basin_str.lower() == 'atlantic':
#         wb = load.hurdat2(_ATLANTIC_FILE)
#     else:
#         _log_error_message('Basin: {0} not supported yet. {1}'.format(basin_str, _available_basins))


def main():
    global wb
    if sys.argv[1] == '--atlantic':
        wb = load.hurdat2(_ATLANTIC_FILE)


if __name__ == '__main__':
    main()
