__author__ = 'tangz'


def log_file_import(file, lines_processed, lines_skipped):
    _log('=======================')
    _log('File: ' + file)
    _log('Lines processed: ' + str(lines_processed))
    _log('Lines skipped: ' + str(lines_skipped))
    _log('=======================')


def _log(stmt):
    print(stmt)