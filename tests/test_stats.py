import unittest
import numpy as np
import pandas as pd
import sys, os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.core import descriptive_stats # Add other modules as testing expands

class TestDescriptiveStats(unittest.TestCase):
    def test_calculate_descriptive_stats_numeric(self):
        series = pd.Series([1.0, 2.0, 3.0, 4.0, 5.0])
        stats_res = descriptive_stats.calculate_descriptive_stats(series)
        self.assertAlmostEqual(stats_res['Mean'], 3.0)
        self.assertEqual(stats_res['Median'], 3.0)

    def test_calculate_descriptive_stats_non_numeric(self):
        series = pd.Series(['a', 'b', 'c'])
        stats_res = descriptive_stats.calculate_descriptive_stats(series)
        self.assertIn('Error', stats_res)
        self.assertEqual(stats_res['Error'], 'Data is empty or non-numeric')

if __name__ == '__main__':
    unittest.main()
