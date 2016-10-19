from datetime import datetime
import unittest

from WeatherExplorer import load
from WeatherExplorer.tcdata import StormId


__author__ = 'tangz'


_DEFAULT_STORM = StormId('AL', 9, 2011, 'IRENE', 'AL092011')


class LoadTests(unittest.TestCase):
    def test_should_parse_storm_info(self):
        line = ['AL092011', '              IRENE', '     43', '']

        storminfo = load.parse_storm_title(line)

        self.assertEqual(storminfo.basin, 'AL')
        self.assertEqual(storminfo.name, 'IRENE')
        self.assertEqual(storminfo.number, 9)
        self.assertEqual(storminfo.year, 2011)
        self.assertEqual(storminfo.raw, 'AL092011')

    def test_should_parse_best_track_pt(self):
        line = ['20110821', ' 0000', '  ', ' TS', ' 15.0N', '  59.0W', '  45', ' 1006', '  105', '', '   0', '    0',
                '   45', '    0', '    0', '    0', '    0', '   0', '    0', '   0', '    0', '']

        bt = load.parse_storm_point(line, _DEFAULT_STORM)

        self.assertEqual(bt.timestamp, datetime(year=2011, month=8, day=21, hour=0, minute=0))
        self.assertEqual(bt.ident, '')
        self.assertEqual(bt.status, 'TS')
        self.assertEqual(bt.lat, 15.0)
        self.assertEqual(bt.lon, -59.0)
        self.assertEqual(bt.windspd, 45)
        self.assertEqual(bt.pres, 1006)
        self.assertEqual(bt.storm, _DEFAULT_STORM)

    def test_should_parse_best_track_pt_with_missing_data(self):
        line = ['20110821', ' 0000', '  ', ' TS', ' 15.0N', '  59.0W', '  45', ' -999', '  105', '', '   0', '    0',
                '   45', '    0', '    0', '    0', '    0', '   0', '    0', '   0', '    0', '']

        bt = load.parse_storm_point(line, _DEFAULT_STORM)

        self.assertEqual(bt.timestamp, datetime(year=2011, month=8, day=21, hour=0, minute=0))
        self.assertEqual(bt.ident, '')
        self.assertEqual(bt.status, 'TS')
        self.assertEqual(bt.lat, 15.0)
        self.assertEqual(bt.lon, -59.0)
        self.assertEqual(bt.windspd, 45)
        self.assertEqual(bt.pres, -999)
        self.assertEqual(bt.storm, _DEFAULT_STORM)