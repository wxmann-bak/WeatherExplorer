import datetime
import unittest
from tcdata import StormId, StormHistory
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

    def test_should_find_storm_based_on_idtuple(self):
        id = StormId(basin='AL', number=3, year=2000, name='ALBERTO', raw='')
        albertohist = self.basindata.tc(idtuple=id)
        self.assertEqual(albertohist.name, id.name)
        self.assertEqual(albertohist.number, id.number)
        self.assertEqual(albertohist.basin, id.basin)
        self.assertEqual(albertohist.year, id.year)
        self.assertEqual(len(albertohist), 7)

    def should_get_length_equal_to_number_of_storms(self):
        self.assertEqual(len(self.basindata), 4)


class StormHistoryTests(unittest.TestCase):
    def setUp(self):
        self.tcpts = samplehurdatfixture.just_alberto_2000_points
        self.tcname = 'ALBERTO'
        self.tcnumber = 3
        self.tcyear = 2000
        self.tcbasin = 'AL'
        self.tcid = 'AL032000'

    def test_create_storm_history_from_points(self):
        tc = StormHistory.from_hurdat_points(self.tcpts)
        self.assertEqual(tc.name, self.tcname)
        self.assertEqual(tc.number, self.tcnumber)
        self.assertEqual(tc.year, self.tcyear)
        self.assertEqual(tc.basin, self.tcbasin)
        self.assertEqual(tc.id, self.tcid)

    def test_should_get_length_from_storm(self):
        tc = StormHistory.from_hurdat_points(self.tcpts)
        self.assertEqual(len(tc), 7)

    def test_should_get_classifiable_points_from_tc(self):
        tc = StormHistory.from_hurdat_points(self.tcpts).classifiable()
        for point in tc:
            self.assertIn(point.status, ('TS', 'HU', 'TD', 'SS', 'SD'))
        self.assertEqual(len(tc), 6)

    def test_should_get_longevity_from_tc(self):
        tc = StormHistory.from_hurdat_points(self.tcpts)
        first_date = datetime.datetime(2000, 8, 3, 18, 0)
        last_date = datetime.datetime(2000, 8, 23, 18, 0)
        self.assertEqual(tc.longevity, last_date - first_date)
