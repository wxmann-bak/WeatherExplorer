import unittest

from WeatherExplorer import queries
from WeatherExplorer.tests import samplehurdatfixture

__author__ = 'tangz'


class QueriesTests(unittest.TestCase):
    def test_should_filter_by_statuses(self):
        ts_strength = queries.lifecycle.contains('TS', 'HU')
        ts_storms = samplehurdatfixture.hurdat_for_queries[ts_strength]
        for storm in ts_storms:
            self.assertTrue('TS' in storm.lifecycle or 'HU' in storm.lifecycle)
        self.assertEqual(len(ts_storms), 2)

    def test_should_filter_by_sshs_category_at_least(self):
        cat4 = samplehurdatfixture.hurdat_for_queries[queries.sshs_category.geq(4)]
        for storm in cat4:
            self.assertTrue(storm.max_wind_speed >= 115)
        self.assertEqual(len(cat4), 2)

    def test_should_filter_by_sshs_category_exact(self):
        cat4 = samplehurdatfixture.hurdat_for_queries[queries.sshs_category.eq(4)]
        for storm in cat4:
            self.assertTrue(115 <= storm.max_wind_speed <= 135)
        self.assertEqual(len(cat4), 1)

    def test_should_filter_by_years(self):
        filtered_storms = samplehurdatfixture.hurdat_for_queries[queries.year.eq(2001, 2004)]
        for storm in filtered_storms:
            self.assertTrue(storm.year == 2001 or storm.year == 2004)
        self.assertEqual(len(filtered_storms), 1)

    def test_should_filter_by_year_range(self):
        filtered_storms = samplehurdatfixture.hurdat_for_queries[queries.year.betw(2001, 2004)]
        for storm in filtered_storms:
            self.assertTrue(storm.year in range(2001, 2007))
        self.assertEqual(len(filtered_storms), 1)

    def test_should_filter_by_subtropical_status(self):
        filtered_storms = samplehurdatfixture.hurdat_for_queries[queries.issubtropical]
        for storm in filtered_storms:
            self.assertEqual(storm.year, 2007)
            self.assertTrue(any(status in ('SS', 'SD') for status in storm.lifecycle))
        self.assertEqual(len(filtered_storms), 1)

    def test_should_filter_by_tropical_status(self):
        filtered_storms = samplehurdatfixture.hurdat_for_queries[queries.istropical]
        for storm in filtered_storms:
            self.assertTrue(any(status in ('TD', 'TS', 'HU') for status in storm.lifecycle))
        self.assertEqual(len(filtered_storms), 3)

    def test_should_filter_by_hurricane_status(self):
        filtered_storms = samplehurdatfixture.hurdat_for_queries[queries.ishurricane]
        for storm in filtered_storms:
            self.assertIn('HU', storm.lifecycle)
        self.assertEqual(len(filtered_storms), 2)

    def test_should_filter_by_major_status(self):
        filtered_storms = samplehurdatfixture.hurdat_for_queries[queries.ismajor]
        for storm in filtered_storms:
            self.assertIn('HU', storm.lifecycle)
            self.assertGreaterEqual(storm.max_wind_speed, 100)
        self.assertEqual(len(filtered_storms), 2)

    def test_should_filter_by_both_year_and_strength(self):
        from WeatherExplorer.queries import year, ishurricane
        filtered_storms = samplehurdatfixture.hurdat_for_queries[year.eq(2000)][ishurricane]
        for storm in filtered_storms:
            self.assertEqual(storm.year, 2000)
            self.assertIn('HU', storm.lifecycle)
        self.assertEqual(len(filtered_storms), 1)

    def test_should_filter_by_both_year_or_strength(self):
        from WeatherExplorer.queries import year, ishurricane
        filtered_storms = samplehurdatfixture.hurdat_for_queries[year.eq(2000)] + \
                          samplehurdatfixture.hurdat_for_queries[ishurricane]
        for storm in filtered_storms:
            self.assertTrue(storm.year == 2000 or 'HU' in storm.lifecycle)
        self.assertEqual(len(filtered_storms), 3)

    def test_should_query_by_max_strength(self):
        filtered_storms = samplehurdatfixture.hurdat_for_queries[queries.max_intensity.gt(120)]
        for storm in filtered_storms:
            self.assertTrue(storm.max_wind_speed > 120)
        self.assertEqual(len(filtered_storms), 1)

    def test_should_query_by_min_ctrl_pres(self):
        filtered_storms = samplehurdatfixture.hurdat_for_queries[queries.min_pres.lt(950)]
        for storm in filtered_storms:
            self.assertTrue(storm.min_ctrl_pres < 950)
        self.assertEqual(len(filtered_storms), 1)

    # TODO: patch the distance function
    def test_should_query_by_distance(self):
        miami = (25.76, -80.19)
        filtered_storms = samplehurdatfixture.hurdat_for_queries[queries.distfrom(miami).lt(10)]
        self.assertEqual(len(filtered_storms), 1)
