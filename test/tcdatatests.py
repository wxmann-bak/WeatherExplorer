from datetime import datetime
import unittest
from tcdata import StormHistory, BestTrackPoint

__author__ = 'tangz'


class _DummyPoint(object):
    ts = datetime(year=2016, month=6, day=30, hour=0, minute=0)
    ident = 'L'
    status = 'HU'
    lat = 0.1
    lon = 10.1
    windspd = 100
    pres = 999

    @staticmethod
    def point():
        return BestTrackPoint(_DummyPoint.ts, _DummyPoint.ident, _DummyPoint.status,
                              _DummyPoint.lat, _DummyPoint.lon, _DummyPoint.windspd,
                              _DummyPoint.pres)


class StormHistoryTests(unittest.TestCase):
    def test_should_access_storm_properties(self):
        tc = StormHistory('AL', 1, 2016, 'ALEX')
        self.assertEqual(tc.year, 2016)
        self.assertEqual(tc.storm_name, 'ALEX')
        self.assertEqual(tc.storm_number, 1)
        self.assertEqual(tc.basin, 'AL')

    def test_should_add_datapoint(self):
        tc = StormHistory('AL', 1, 2016, 'ALEX')
        tc += _DummyPoint.point()

        for btpt in tc:
            self.assertEqual(btpt.timestamp, _DummyPoint.ts)
            self.assertEqual(btpt.ident, _DummyPoint.ident)
            self.assertEqual(btpt.status, _DummyPoint.status)
            self.assertEqual(btpt.lat, _DummyPoint.lat)
            self.assertEqual(btpt.lon, _DummyPoint.lon)
            self.assertEqual(btpt.windspd, _DummyPoint.windspd)
            self.assertEqual(btpt.pres, _DummyPoint.pres)

    def test_should_iterate_through_datapoints(self):
        tc = StormHistory('AL', 1, 2016, 'ALEX')
        for i in range(10):
            tc += BestTrackPoint(_DummyPoint.ts, _DummyPoint.ident, _DummyPoint.status,
                                 _DummyPoint.lat, _DummyPoint.lon, _DummyPoint.windspd + 5 * i,
                                 _DummyPoint.pres)
        j = 0
        for btpt in tc:
            self.assertEqual(btpt.timestamp, _DummyPoint.ts)
            self.assertEqual(btpt.ident, _DummyPoint.ident)
            self.assertEqual(btpt.status, _DummyPoint.status)
            self.assertEqual(btpt.lat, _DummyPoint.lat)
            self.assertEqual(btpt.lon, _DummyPoint.lon)
            self.assertEqual(btpt.windspd, _DummyPoint.windspd + 5 * j)
            self.assertEqual(btpt.pres, _DummyPoint.pres)
            j += 1

    def test_should_make_read_only(self):
        tc = StormHistory('AL', 1, 2016, 'ALEX')
        tc = tc.read_only()
        with self.assertRaises(NotImplementedError):
            tc += _DummyPoint.point()