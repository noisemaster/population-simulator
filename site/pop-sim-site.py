import sqlite3
from flask import Flask, g, render_template, request

DATABASE = '../PopulationSimulator.db'
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_pop_pred(country, year):
    pop = int(query_db('SELECT "{col1}" FROM "{t}" WHERE "{col2}"="{val}"'.format(col1 = "Population", t = "PopulationData", col2 = "Country", val = country))[0][0])
    mig = float(query_db('SELECT "{col1}" FROM "{t}" WHERE "{col2}"="{val}"'.format(col1 = "Migration Rate", t = "PopulationData", col2 = "Country", val = country))[0][0])
    bir = float(query_db('SELECT "{col1}" FROM "{t}" WHERE "{col2}"="{val}"'.format(col1 = "Birth Rate", t = "PopulationData", col2 = "Country", val = country))[0][0])
    dea = float(query_db('SELECT "{col1}" FROM "{t}" WHERE "{col2}"="{val}"'.format(col1 = "Death Rate", t = "PopulationData", col2 = "Country", val = country))[0][0])

    for i in range(year):
        pop = pop + ((mig + bir - dea) * (pop/1000))

    return int(pop)

@app.route('/')
def show_all():
    query = query_db('select * from PopulationData')
    countries = [dict(country=row[0]) for row in query]
    return render_template('population.html', countries=countries)

@app.route('/calculate-years', methods=['GET', 'POST'])
def calculate_pop():
    years = int(request.form['years'])
    country = request.form['countries']
    new_pop = get_pop_pred(country, years)
    return render_template('information.html', z=str(new_pop), years=str(years))

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
        app.run()
