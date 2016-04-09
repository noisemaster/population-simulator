import unittest
import sqlite3

# Name of the table in the database
tab_nam = "pop"

# Column titles in the database (We might want to get rid of the parenthesis)
col_cou = "Country"
col_pop = "Population"
col_mig = "Migration Rate (Migrants per 1000 people)"
col_bir = "Birth Rate (per 1000 people)"
col_dea = "Death Rate (per 1000 people)"

class TestDatabase(unittest.TestCase):
    def test_us_pop(self):
        db = sqlite3.connect("population.db")
        cur = db.cursor()
        self.assertEqual(int(cur.execute('SELECT "{col1}" FROM "{t}" WHERE "{col2}"="{val}"'.format(col1=col_pop, t=tab_nam, col2=col_cou, val="United States")).fetchone()[0]), 321368864)
        db.close()

    def test_spain_mig(self):
        db = sqlite3.connect("population.db")
        cur = db.cursor()
        self.assertEqual(float(cur.execute('SELECT "{col1}" FROM "{t}" WHERE "{col2}"="{val}"'.format(col1=col_mig, t=tab_nam, col2=col_cou, val="Spain")).fetchone()[0]), 8.31)
        db.close()

    def test_ru_birth(self):
        db = sqlite3.connect("population.db")
        cur = db.cursor()
        self.assertEqual(float(cur.execute('SELECT "{col1}" FROM "{t}" WHERE "{col2}"="{val}"'.format(col1=col_bir, t=tab_nam, col2=col_cou, val="Russia")).fetchone()[0]), 11.6)
        db.close()

    def test_ger_death(self):
        db = sqlite3.connect("population.db")
        cur = db.cursor()
        self.assertEqual(float(cur.execute('SELECT "{col1}" FROM "{t}" WHERE "{col2}"="{val}"'.format(col1=col_dea, t=tab_nam, col2=col_cou, val="Germany")).fetchone()[0]), 11.42)
        db.close()

if __name__ == "__main__":
    unittest.main()
