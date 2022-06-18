'''
Henry Pacheco Cachon
17 June 2022
Last Updated: 17 June 2022
app.py file for flask application 
'''

from email.policy import default
from flask import Flask
from flask import render_template, g
import sqlite3

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
    return render_template('index.html')


