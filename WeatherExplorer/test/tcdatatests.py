import datetime
import unittest

from WeatherExplorer import queries
from WeatherExplorer.tcdata import StormHistory, BasinHistory
from WeatherExplorer.test import samplehurdatfixture


__author__ = 'tangz'


class BasinHistoryTest(unittest.TestCase):
    def setUp(self):
        self.basindata = samplehurdatfixture.hurdat_for_tcdata

    def test_should_return_basin(self):
        self.assertEqual(self.basindata.basin, samplehurdatfixture.TEST_BASIN_FOR_TCDATA)

    def test_should_find_storm_based_on_year_and_name(self):
        alberto = 'Alberto'
        year = 2000
        albertohist = self.basindata.get_tc(year, alberto)
        self.assertEqual(albertohist.name, alberto.upper())
        self.assertEqual(albertohist.basin, samplehurdatfixture.TEST_BASIN_FOR_TCDATA)
        self.assertEqual(albertohist.year, year)
        self.assertEqual(len(albertohist), 7)

    def test_should_find_storm_based_on_year_and_number(self):
        num = 3
        year = 2000
        albertohist = self.basindata.get_tc(year, number=3)
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

    def test_should_query_storms(self):
        year2000 = self.basindata.query(queries.year.eq(2000))
        for storm in year2000:
            self.assertEqual(storm.year, 2000)
        self.assertEqual(len(year2000), 2)

    def test_should_throw_error_if_try_to_get_tc_without_name_and_number(self):
        with self.assertRaises(ValueError):
            self.basindata.get_tc(2000)


class TCResultSetTests(unittest.TestCase):
    def setUp(self):
        self.basindata = samplehurdatfixture.hurdat_for_tcdata

    def test_should_query_storms_multiple_times(self):
        pass_2000 = queries.year.eq(2000)
        pass_cat4 = queries.sshs_category.eq(4)
        year2000_cat4s = self.basindata.query(pass_2000).query(pass_cat4)

        for storm in year2000_cat4s:
            self.assertEqual(storm.year, 2000)
            self.assertTrue(115 <= storm.max_wind_speed)
        self.assertEqual(len(year2000_cat4s), 1)

    def test_should_union_two_result_sets(self):
        pass_2000 = queries.year.eq(2000)
        pass_cat4 = queries.sshs_category.geq(4)
        year2000_or_cat4s = self.basindata.query(pass_2000) + self.basindata.query(pass_cat4)

        for storm in year2000_or_cat4s:
            self.assertTrue(storm.year == 2000 or storm.max_wind_speed >= 115)
        self.assertEqual(len(year2000_or_cat4s), 3)

    def test_should_subtract_one_result_from_another(self):
        pass_2000 = queries.year.eq(2000)
        pass_cat4 = queries.sshs_category.eq(4)
        year2000_not_cat4 = self.basindata.query(pass_2000) - self.basindata.query(pass_cat4)

        for storm in year2000_not_cat4:
            self.assertEqual(storm.year, 2000)
            self.assertFalse(storm.max_wind_speed >= 115)
        self.assertEqual(len(year2000_not_cat4), 1)

    def test_should_find_complement_of_result(self):
        pass_2000 = queries.year.eq(2000)
        not_year_2000 = -self.basindata.query(pass_2000)

        for storm in not_year_2000:
            self.assertNotEqual(storm.year, 2000)
        self.assertEqual(len(not_year_2000), 2)

    def test_should_find_storms_in_queried_history(self):
        alberto2000 = self.basindata.get_tc(2000, 'Alberto')
        alberto2004 = self.basindata.get_tc(2004, 'Alberto')
        year2000storms = self.basindata.query(queries.year.eq(2000))

        self.assertTrue(alberto2000 in year2000storms)
        self.assertFalse(alberto2004 in year2000storms)

    def test_should_test_for_empty_query_result(self):
        year2222storms = self.basindata.query(queries.year.eq(2222))
        year2000storms = self.basindata.query(queries.year.eq(2000))

        self.assertFalse(year2222storms)
        self.assertTrue(year2000storms)

    def test_should_throw_error_if_not_same_source(self):
        year2000 = self.basindata.query(queries.year.eq(2000))
        dummy = BasinHistory('another_dummy', ())
        year2001 = dummy.query(queries.year.eq(2001))

        with self.assertRaises(AssertionError):
            should_throw_error = year2000 - year2001


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
        classifiable_snippet = self.tc.classifiable()
        for point in classifiable_snippet:
            self.assertIn(point.status, ('TS', 'HU', 'TD', 'SS', 'SD'))
        self.assertEqual(len(classifiable_snippet), 6)

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

    def test_should_get_max_sshs_category_from_tc(self):
        self.assertEqual(self.tc.max_sshs_category, 4)

    def test_should_get_ts_slices_from_tc(self):
        slices = self.tc.slice(lambda storm: storm.status == 'TS')
        for section in slices:
            for datapoint in section:
                self.assertEqual(datapoint.status, 'TS')
            self.assertEqual(len(section), 1)
        self.assertEqual(len(slices), 2)

