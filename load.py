import csv
from datetime import datetime
import re

from tcdata import StormHistory, BestTrackPoint

__author__ = 'tangz'


def hurdat2(hurdat_file):
    tc_on = None
    all_storms = []
    lines_processed = 0
    lines_skipped = 0
    with open(hurdat_file) as csvfile:
        hurdat_data = csv.reader(csvfile)
        for line in hurdat_data:
            if line:
                if line[0].startswith('AL'):
                    if tc_on:
                        all_storms.append(tc_on.read_only())
                    tc_on = parse_storm_title(line, 'AL')
                else:
                    tc_on += parse_storm_point(line)
                lines_processed += 1
            else:
                lines_skipped += 1

    _log('=======================')
    _log('File: ' + hurdat_file)
    _log('Lines processed: ' + str(lines_processed))
    _log('Lines skipped: ' + str(lines_skipped))
    return all_storms


def parse_storm_title(row, basin):
    if len(row) < 3:
        raise ValueError("Invalid row, need at least three entries: " + ','.join(row))
    storm_info = row[0].strip()
    storm_name = row[1].strip()
    lines = row[2].strip()

    info_matches = re.match(re.escape(basin) + r'(\d{2})(\d{4})', storm_info)
    if info_matches:
        _log('Number of HURDAT rows in storm {0} ({1}): {2}'.format(storm_info, storm_name, lines))
        storm_number = int(info_matches.group(1))
        year = int(info_matches.group(2))
        return StormHistory(basin, storm_number, year, storm_name)
    else:
        raise ValueError("Invalid TC information: " + storm_info)


def parse_storm_point(row):
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
    return BestTrackPoint(timestmp, ident, status, lat, lon, windspd, pres)


def _log(stmt):
    print(stmt)