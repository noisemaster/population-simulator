import sqlite3

# Name of the table in the database
tab_nam = "PopulationData"

# Column titles in the database
col_cou = "Country"
col_pop = "Population"
col_mig = "Migration Rate"
col_bir = "Birth Rate"
col_dea = "Death Rate"

# Name of the database file
db = sqlite3.connect("population.db")
cur = db.cursor()

# General get column for country method
# Using format on the sql string technically puts us at risk for sql injection for production code
def get_col(country, column):
	cur.execute('SELECT "{col1}" FROM "{t}" WHERE "{col2}"="{val}"'.format(col1=column, t=tab_nam, col2=col_cou, val=country))
	return cur.fetchone()[0]

# Gets a list of all countries in database
def get_countries():
	cur.execute('SELECT "{col}" FROM "{tab}"'.format(col=col_cou, tab=tab_nam))
	col = cur.fetchall()
	ret = []
	for arr in col:
		ret.extend(arr)
	return ret

# More specific methods for each column
def get_pop(country):
	return int(get_col(country, col_pop))

def get_mig(country):
	return float(get_col(country, col_mig))

def get_bir(country):
	return float(get_col(country, col_bir))

def get_dea(country):
	return float(get_col(country, col_dea))

# Calculate a prediction of the population in the country and year specified
def get_pop_pred(country, year):
	pop = get_pop(country)
	mig = get_mig(country)
	bir = get_bir(country)
	dea = get_dea(country)
	
	for i in range(year - data_year):
		pop = pop + ((mig + bir - dea) * (pop/1000))
	
	return int(pop)

# Main code starts here
# If first argument is "-countries", a list of all countries in the database will be printed
# Otherwise, a prediction of the population will be printed
#	The first argument is expected to be the name of a country in the database
#	The second argument is expected to be a year later than the year the data was taken
# ex: DatabaseTest.py "United States" 2020
if (len(sys.argv) > 1):
	if (sys.argv[1] == "-countries"):
		print(get_countries())
	else:
		if (len(sys.argv) > 2):
			print(get_pop_pred(sys.argv[1], int(sys.argv[2])))

db.close()