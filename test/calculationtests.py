import unittest
import calculations

__author__ = 'tangz'


class CalculationsTests(unittest.TestCase):
    def test_should_use_haversine_formula_to_calculate_distances(self):
        latlon1 = (40.7486, -73.9864)
        latlon2 = (50, -50)
        self.assertAlmostEqual(1319.792, calculations.dist_mi(latlon1, latlon2), delta=0.1)

