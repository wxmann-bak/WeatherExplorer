import unittest

import queries
from test import samplehurdatfixture


__author__ = 'tangz'


class QueriesTests(unittest.TestCase):
    def test_should_filter_by_statuses(self):
        ts_strength = queries.statuses('TS', 'HU')
        ts_hu_datapoints = samplehurdatfixture.sample_hurdat.query(ts_strength)
        for datapoint in ts_hu_datapoints:
            self.assertIn(datapoint.status, ('TS', 'HU'))
        self.assertEqual(len(ts_hu_datapoints), 4)

    def test_should_filter_by_storm_name(self):
        alberto = 'Alberto'
        alberto_pts = samplehurdatfixture.sample_hurdat.query(queries.storm(2000, alberto))
        for datapoint in alberto_pts:
            self.assertEqual(datapoint.storm.name, alberto.upper())
            self.assertEqual(datapoint.storm.year, 2000)
        self.assertEqual(len(alberto_pts), 7)

    def test_should_filter_by_storm_number(self):
        alberto_num = 3
        alberto_pts = samplehurdatfixture.sample_hurdat.query(queries.storm(2000, number=alberto_num))
        for datapoint in alberto_pts:
            self.assertEqual(datapoint.storm.name, 'ALBERTO')
            self.assertEqual(datapoint.storm.number, 3)
            self.assertEqual(datapoint.storm.year, 2000)
        self.assertEqual(len(alberto_pts), 7)

    def test_should_filter_by_sshws_category(self):
        cat4 = samplehurdatfixture.sample_hurdat.query(queries.sshws_category(4))
        for datapoint in cat4:
            self.assertTrue(datapoint.windspd >= 115)
        self.assertEqual(len(cat4), 1)

    def test_should_filter_by_year_range(self):
        snippet = samplehurdatfixture.sample_hurdat.query(queries.years(begin=2004, end=2006))
        for datapoint in snippet:
            self.assertTrue(2004 <= datapoint.storm.year <= 2006)
        self.assertEqual(len(snippet), 2)

    def test_should_filter_by_specific_years(self):
        snippet = samplehurdatfixture.sample_hurdat.query(queries.years(eq=(2001, 2004)))
        for datapoint in snippet:
            self.assertTrue(datapoint.storm.year == 2001 or datapoint.storm.year == 2004)
        self.assertEqual(len(snippet), 2)

    def test_should_filter_by_one_year(self):
        snippet = samplehurdatfixture.sample_hurdat.query(queries.years(eq=2004))
        for datapoint in snippet:
            self.assertEqual(datapoint.storm.year, 2004)
        self.assertEqual(len(snippet), 2)

    def test_should_filter_by_both_storm_and_strength(self):
        alberto = 'Alberto'
        from queries import storm, allof, strength
        alberto_pts = samplehurdatfixture.sample_hurdat.query(allof(storm(2000, alberto), strength.hu))
        for datapoint in alberto_pts:
            self.assertEqual(datapoint.storm.name, alberto.upper())
            self.assertEqual(datapoint.storm.year, 2000)
            self.assertEqual(datapoint.status, 'HU')
        self.assertEqual(len(alberto_pts), 2)

    def test_should_filter_by_multiple_storms(self):
        alberto = 'Alberto'
        from queries import storm, anyof

        alberto_pts = samplehurdatfixture.sample_hurdat.query(anyof(storm(2000, alberto), storm(2004, alberto)))
        for datapoint in alberto_pts:
            self.assertEqual(datapoint.storm.name, alberto.upper())
            self.assertIn(datapoint.storm.year, (2000, 2004))
        self.assertEqual(len(alberto_pts), 9)