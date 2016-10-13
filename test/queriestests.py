import unittest

import queries
from test import samplehurdatfixture


__author__ = 'tangz'


class QueriesTests(unittest.TestCase):
    def test_should_filter_by_statuses(self):
        ts_strength = queries.statuses('TS', 'HU')
        ts_hu_datapoints = samplehurdatfixture.hurdat_for_queries.query(ts_strength)
        for datapoint in ts_hu_datapoints:
            self.assertIn(datapoint.status, ('TS', 'HU'))
        self.assertEqual(len(ts_hu_datapoints), 6)

    def test_should_filter_by_sshws_category(self):
        cat4 = samplehurdatfixture.hurdat_for_queries.query(queries.sshws_category(4))
        for datapoint in cat4:
            self.assertTrue(datapoint.windspd >= 115)
        self.assertEqual(len(cat4), 2)

    def test_should_filter_by_year_range(self):
        snippet = samplehurdatfixture.hurdat_for_queries.query(queries.years(begin=2004, end=2006))
        for datapoint in snippet:
            self.assertTrue(2004 <= datapoint.storm.year <= 2006)
        self.assertEqual(len(snippet), 2)

    def test_should_filter_by_specific_years(self):
        snippet = samplehurdatfixture.hurdat_for_queries.query(queries.years(eq=(2001, 2004)))
        for datapoint in snippet:
            self.assertTrue(datapoint.storm.year == 2001 or datapoint.storm.year == 2004)
        self.assertEqual(len(snippet), 2)

    def test_should_filter_by_one_year(self):
        snippet = samplehurdatfixture.hurdat_for_queries.query(queries.years(eq=2004))
        for datapoint in snippet:
            self.assertEqual(datapoint.storm.year, 2004)
        self.assertEqual(len(snippet), 2)

    def test_should_filter_by_subtropical_status(self):
        points = samplehurdatfixture.hurdat_for_queries.query(queries.issubtropical)
        for datapoint in points:
            self.assertEqual(datapoint.storm.year, 2007)
            self.assertIn(datapoint.status, ('SS', 'SD'))
        self.assertEqual(len(points), 2)

    def test_should_filter_by_tropical_status(self):
        points = samplehurdatfixture.hurdat_for_queries.query(queries.istropical)
        for datapoint in points:
            self.assertIn(datapoint.status, ('TD', 'TS', 'HU'))
        self.assertEqual(len(points), 10)

    def test_should_filter_by_classified_status(self):
        points = samplehurdatfixture.hurdat_for_queries.query(queries.isclassifiable)
        for datapoint in points:
            self.assertIn(datapoint.status, ('TD', 'TS', 'HU', 'SS', 'SD'))
        self.assertEqual(len(points), 12)

    def test_should_filter_by_hurricane_status(self):
        points = samplehurdatfixture.hurdat_for_queries.query(queries.ishurricane)
        for datapoint in points:
            self.assertIn(datapoint.status, 'HU')
        self.assertEqual(len(points), 4)

    def test_should_filter_by_major_status(self):
        points = samplehurdatfixture.hurdat_for_queries.query(queries.ismajor)
        for datapoint in points:
            self.assertIn(datapoint.status, 'HU')
        self.assertEqual(len(points), 2)

    def test_should_filter_by_both_year_and_strength(self):
        from queries import years, allof, ishurricane
        points = samplehurdatfixture.hurdat_for_queries.query(allof(years(eq=2000), ishurricane))
        for datapoint in points:
            self.assertEqual(datapoint.storm.year, 2000)
            self.assertEqual(datapoint.status, 'HU')
        self.assertEqual(len(points), 2)

    def test_should_filter_by_both_year_or_strength(self):
        from queries import years, anyof, ishurricane
        points = samplehurdatfixture.hurdat_for_queries.query(anyof(years(eq=2000), ishurricane))
        for datapoint in points:
            self.assertTrue(datapoint.storm.year == 2000 or datapoint.status == 'HU')
        self.assertEqual(len(points), 12)