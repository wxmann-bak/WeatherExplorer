import csv
from datetime import datetime
import re

from tcdata import BestTrackPoint, BasinHistory, StormHistory, StormId


__author__ = 'tangz'


def atcf(atcf_file, storm_name):
    stormpts = set()
    lines_processed = 0
    lines_skipped = 0
    with open(atcf_file) as csvfile:
        atcf_data = csv.reader(csvfile)
        for line in atcf_data:
            if line:
                stormpts.add(_parse_atcf_point(line, storm_name))
                lines_processed += 1
            else:
                lines_skipped += 1

    _log('=======================')
    _log('File: ' + atcf_file)
    _log('Lines processed: ' + str(lines_processed))
    _log('Lines skipped: ' + str(lines_skipped))
    _log('=======================')
    return StormHistory.from_hurdat_points(stormpts)


def _parse_atcf_point(line, storm_name):
    basin = line[0].strip()
    storm_number = int(line[1].strip())
    timestmp = datetime.strptime(line[2].strip(), '%Y%m%d%H')
    lat_str = line[6].strip()
    lon_str = line[7].strip()
    windspd = int(line[8])
    pres = int(line[9])
    status = line[10].strip()

    lat = float(re.sub(r'N|S', '', lat_str)) / 10
    lon = float(re.sub(r'E|W', '', lon_str)) / 10
    if lon_str[-1] == 'W':
        lon *= -1

    stormid = StormId(basin=basin, number=storm_number, name=storm_name.upper(), year=timestmp.year, raw='')
    datapoint = BestTrackPoint(storm=stormid, timestamp=timestmp, ident='', status=status, lat=lat, lon=lon,
                               windspd=windspd, pres=pres)
    return datapoint


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

    _log('=======================')
    _log('File: ' + hurdat_file)
    _log('Lines processed: ' + str(lines_processed))
    _log('Lines skipped: ' + str(lines_skipped))
    _log('=======================')
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


def _log(stmt):
    print(stmt)


class BasinBuilder(object):
    def __init__(self, basin_name):
        self._basin = basin_name
        self._storm_pts = {}

    def __add__(self, pt):
        if pt.storm not in self._storm_pts:
            self._storm_pts[pt.storm] = []
        self._storm_pts[pt.storm].append(pt)
        return self

    def build(self):
        storms = []
        for stormid in self._storm_pts:
            pts_for_storm = self._storm_pts[stormid]
            stormhist = StormHistory.from_hurdat_points(pts_for_storm)
            storms.append(stormhist)
        return BasinHistory(self._basin, storms)


def storm_id(raw, storm_name):
    matches = re.match(r'(\w{2})(\d{2})(\d{4})', raw)
    if matches:
        basin = matches.group(1)
        storm_number = int(matches.group(2))
        year = int(matches.group(3))
        return StormId(basin, storm_number, year, storm_name, raw)
    else:
        raise ValueError("Invalid TC information: " + raw)