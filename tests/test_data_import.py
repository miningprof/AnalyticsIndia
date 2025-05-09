import unittest
import pandas as pd
import os, sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils.data_handler import load_data_from_file

class TestDataImport(unittest.TestCase):
    def setUp(self):
        self.test_dir = os.path.join(os.path.dirname(__file__), "temp_test_data_import")
        os.makedirs(self.test_dir, exist_ok=True)
        self.csv_file = os.path.join(self.test_dir, "test.csv")
        with open(self.csv_file, "w") as f: f.write("colA,colB\n1,10\n2,20")

    def tearDown(self):
        if os.path.exists(self.csv_file): os.remove(self.csv_file)
        if os.path.exists(self.test_dir): os.rmdir(self.test_dir)

    def test_load_csv(self):
        df = load_data_from_file(self.csv_file)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (2,2))

if __name__ == '__main__':
    unittest.main()
