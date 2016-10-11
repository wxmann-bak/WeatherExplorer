import csv
from datetime import datetime
import re

from tcdata import BestTrackPoint, BasinHistory, storm_id


__author__ = 'tangz'


def hurdat2(hurdat_file):
    tc_on = None
    atlantic = 'AL'
    all_storms = BasinHistory(atlantic)
    lines_processed = 0
    lines_skipped = 0
    with open(hurdat_file) as csvfile:
        hurdat_data = csv.reader(csvfile)
        for line in hurdat_data:
            if line:
                if line[0].startswith(atlantic):
                    tc_on = parse_storm_title(line)
                else:
                    all_storms += parse_storm_point(line, tc_on)
                lines_processed += 1
            else:
                lines_skipped += 1

    _log('=======================')
    _log('File: ' + hurdat_file)
    _log('Lines processed: ' + str(lines_processed))
    _log('Lines skipped: ' + str(lines_skipped))
    _log('=======================')
    return all_storms


def parse_storm_title(row):
    if len(row) < 3:
        raise ValueError("Invalid row, need at least three entries: " + ','.join(row))
    storm_info = row[0].strip()
    storm_name = row[1].strip()
    lines = row[2].strip()
    _log('Number of HURDAT rows in storm {0} ({1}): {2}'.format(storm_info, storm_name, lines))

    return storm_id(storm_info, storm_name)


def parse_storm_point(row, storm):
    date_str = row[0].strip()
    time_str = row[1].strip()
    ident = row[2].strip()
    status = row[3].strip()
    lat_str = row[4].strip()
    lon_str = row[5].strip()
    windspd = int(row[6].strip())
    pres = int(row[7].strip())

    timestmp = datetime.strptime(date_str + time_str, '%Y%m%d%H%M')
    lat = float(re.sub(r'N|S', '', lat_str))
    lon = float(re.sub(r'E|W', '', lon_str))
    return BestTrackPoint(storm, timestmp, ident, status, lat, lon, windspd, pres)


def _log(stmt):
    print(stmt)