'''
Henry Pacheco Cachon
17 June 2022
Last Updated: 17 June 2022
app.py file for flask application 
'''

from flask import Flask
from flask import render_template, g, request, redirect, url_for
import sqlite3
import datetime

# Initializing a Flask object
app = Flask(__name__)
# Initializing the PATH variable to sql database
PATH = 'db/jobs.sqlite'

# Function starts a sqlite3 connection to a database
def open_connection():
    connection = getattr('g','_connection',None)


    if connection == None:
        connection = g._connection = sqlite3.connect(PATH)
    
    connection.row_factory = sqlite3.Row

    return connection

# Function handles database queries
def execute_sql(sql, values=(), commit=False, single=False):

    # Connect to sql database
    connection = open_connection()
    # Execute query
    cursor = connection.execute(sql, values)

    if commit:
        # Get confirmation of change to database
        results = connection.commit()
    else:
        # Get results from query (one or many)
        results = cursor.fetchone() if single else cursor.fetchall()
    
    # Closing connection to database
    connection.close()
    
    return results

# Function is responsible for closing the connection to the database
@app.teardown_appcontext
def close_connection(exception):

    # Getting the current connection
    connection = getattr('g', '_connection', None)

    # If there is a connection, close it
    if connection:
        connection.close()


# Creating route in flask
@app.route('/')
@app.route('/jobs')
def jobs():
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id')
    return render_template('index.html', jobs=jobs)


# Job page
@app.route('/job/<job_id>')
def job(job_id):
    job = execute_sql('SELECT job.id, job.title, job.description, job.salary, employer.id as employer_id, employer.name as employer_name FROM job JOIN employer ON employer.id = job.employer_id WHERE job.id = ?', [job_id], single=True)
    return render_template('job.html', job=job)

# Employer page
@app.route('/employer/<employer_id>')
def employer(employer_id):
    employer = execute_sql('SELECT * FROM employer WHERE id=?', [employer_id], single=True)
    jobs = execute_sql('SELECT job.id, job.title, job.description, job.salary FROM job JOIN employer ON employer.id = job.employer_id WHERE employer.id = ?', [employer_id])
    reviews = execute_sql('SELECT review, rating, title, date, status FROM review JOIN employer ON employer.id = review.employer_id WHERE employer.id = ?', [employer_id])
    return render_template('employer.html', employer=employer, jobs=jobs, reviews=reviews)

# Review form
@app.route('/employer/<employer_id>/review', methods=('GET','POST'))
def review(employer_id):

    if request.method == 'POST':

        review = request.form['review']
        rating = request.form['rating']
        title = request.form['title']
        status = request.form['status']

        date = datetime.datetime.now().strftime("%m/%d/%y")

        execute_sql('INSERT INTO review (review, rating, title, date, status, employer_id) VALUES (?, ?, ?, ?, ?, ?)', (review, rating, title, date, status, employer_id), commit=True)

        return redirect(url_for('employer',employer_id=employer_id))

    return render_template('review.html', employer_id=employer_id)

