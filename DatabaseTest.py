import sqlite3

# Name of the table in the database
tab_nam = "PopulationData"

# Column titles in the database (We might want to get rid of the parenthesis)
col_cou = "Country"
col_pop = "Population"
col_mig = "Migration Rate"
col_bir = "Birth Rate"
col_dea = "Death Rate"

# Name of the database file
db = sqlite3.connect("PopulationSimulator.db")
cur = db.cursor()

# General get column for country method
# Using format on the sql string technically puts us at risk for sql injection for production code
def get_col(country, column):
	cur.execute('SELECT "{col1}" FROM "{t}" WHERE "{col2}"="{val}"'.format(col1=column, t=tab_nam, col2=col_cou, val=country))
	return cur.fetchone()[0]

# More specific methods for each column
def get_pop(country):
	return int(get_col(country, col_pop))

def get_mig(country):
	return float(get_col(country, col_mig))

def get_bir(country):
	return float(get_col(country, col_bir))

def get_dea(country):
	return float(get_col(country, col_dea))

print("US Population:        ", get_pop("United States"))
print("Spain Migration Rate: ", get_mig("Spain"))
print("Russia Birth Rate:    ", get_bir("Russia"))
print("Germany Death Rate:   ", get_dea("Germany"))

db.close()
