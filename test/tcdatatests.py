import datetime
import unittest

from tcdata import StormHistory
from test import samplehurdatfixture


__author__ = 'tangz'


class BasinHistoryTest(unittest.TestCase):
    def setUp(self):
        self.basindata = samplehurdatfixture.hurdat_for_tcdata

    def test_should_return_basin(self):
        self.assertEqual(self.basindata.basin, samplehurdatfixture.TEST_BASIN_FOR_TCDATA)

    def test_should_find_storm_based_on_year_and_name(self):
        alberto = 'Alberto'
        year = 2000
        albertohist = self.basindata.tc(year, alberto)
        self.assertEqual(albertohist.name, alberto.upper())
        self.assertEqual(albertohist.basin, samplehurdatfixture.TEST_BASIN_FOR_TCDATA)
        self.assertEqual(albertohist.year, year)
        self.assertEqual(len(albertohist), 7)

    def test_should_find_storm_based_on_year_and_number(self):
        num = 3
        year = 2000
        albertohist = self.basindata.tc(year, number=3)
        self.assertEqual(albertohist.number, num)
        self.assertEqual(albertohist.basin, samplehurdatfixture.TEST_BASIN_FOR_TCDATA)
        self.assertEqual(albertohist.year, year)
        self.assertEqual(len(albertohist), 7)

    def test_should_get_length_equal_to_number_of_storms(self):
        self.assertEqual(len(self.basindata), 4)

    def test_should_iterate_through_storms(self):
        length = 4
        i = 0
        for storm in self.basindata:
            self.assertIsNotNone(storm)
            i += 1
        self.assertEqual(length, i)


class StormHistoryTests(unittest.TestCase):
    def setUp(self):
        self.tcpts = samplehurdatfixture.just_alberto_2000_points
        self.tcname = 'ALBERTO'
        self.tcnumber = 3
        self.tcyear = 2000
        self.tcbasin = 'AL'
        self.tcid = 'AL032000'
        self.tc = StormHistory.from_hurdat_points(self.tcpts)

    def test_create_storm_history_from_points(self):
        self.assertEqual(self.tc.name, self.tcname)
        self.assertEqual(self.tc.number, self.tcnumber)
        self.assertEqual(self.tc.year, self.tcyear)
        self.assertEqual(self.tc.basin, self.tcbasin)
        self.assertEqual(self.tc.id, self.tcid)

    def test_should_get_length_from_storm(self):
        self.assertEqual(len(self.tc), 7)

    def test_should_get_classifiable_points_from_tc(self):
        tc = self.tc.classifiable()
        for point in tc:
            self.assertIn(point.status, ('TS', 'HU', 'TD', 'SS', 'SD'))
        self.assertEqual(len(tc), 6)

    def test_should_get_longevity_from_tc(self):
        first_date = datetime.datetime(2000, 8, 3, 18, 0)
        last_date = datetime.datetime(2000, 8, 23, 18, 0)
        self.assertEqual(self.tc.longevity, last_date - first_date)

    def test_should_get_max_wind_speed_from_tc(self):
        self.assertEqual(self.tc.max_wind_speed, 115)

    def test_should_get_min_ctrl_pres_from_tc(self):
        self.assertEqual(self.tc.min_ctrl_pres, 977)

    def test_should_get_lifecycle_from_tc(self):
        self.assertEqual(self.tc.lifecycle, ('TD', 'TS', 'HU', 'TS', 'SS', 'EX'))

