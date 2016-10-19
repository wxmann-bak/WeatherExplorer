import csv
from datetime import datetime
import re
from WeatherExplorer.datasources.logger import log_file_import
from WeatherExplorer.tcdata import StormHistory, StormId, BestTrackPoint

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

    log_file_import(atcf_file, lines_processed, lines_skipped)
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