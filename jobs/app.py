'''
Henry Pacheco Cachon
17 June 2022
Last Updated: 17 June 2022
app.py file for flask application 
'''


import flask as fl
from flask import render_template

app = fl.Flask(__name__)

# Creating route in flask
@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')


