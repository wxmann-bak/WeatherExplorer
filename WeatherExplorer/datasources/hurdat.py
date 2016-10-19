import csv
from datetime import datetime
import re

from WeatherExplorer.datasources.loadtc_helper import BasinBuilder
from WeatherExplorer.datasources.logger import log_file_import
from WeatherExplorer.tcdata import BestTrackPoint, StormId


__author__ = 'tangz'


ATLANTIC_FILE = 'WeatherExplorer/datasources/files/hurdat2-1851-2015-070616.txt'

ATLANTIC_FILE_BRIEF = 'WeatherExplorer/datasources/files/hurdat2-2000-2006.txt'


def hurdat2(hurdat_file):
    tc_on = None
    atlantic = 'AL'
    basin_builder = BasinBuilder(atlantic)
    lines_processed = 0
    lines_skipped = 0
    with open(hurdat_file) as csvfile:
        hurdat_data = csv.reader(csvfile)
        for line in hurdat_data:
            if line:
                if line[0].startswith(atlantic):
                    tc_on = parse_storm_title(line)
                else:
                    basin_builder += parse_storm_point(line, tc_on)
                lines_processed += 1
            else:
                lines_skipped += 1

    log_file_import(hurdat_file, lines_processed, lines_skipped)
    return basin_builder.build()


def parse_storm_title(row):
    if len(row) < 3:
        raise ValueError("Invalid row, need at least three entries: " + ','.join(row))
    storm_info = row[0].strip()
    storm_name = row[1].strip()
    lines = row[2].strip()
    # _log('Number of HURDAT rows in storm {0} ({1}): {2}'.format(storm_info, storm_name, lines))

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
    if lon_str[-1] == 'W':
        lon *= -1
    return BestTrackPoint(storm, timestmp, ident, status, lat, lon, windspd, pres)


def storm_id(raw, storm_name):
    matches = re.match(r'(\w{2})(\d{2})(\d{4})', raw)
    if matches:
        basin = matches.group(1)
        storm_number = int(matches.group(2))
        year = int(matches.group(3))
        return StormId(basin, storm_number, year, storm_name, raw)
    else:
        raise ValueError("Invalid TC information: " + raw)