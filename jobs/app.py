'''
Henry Pacheco Cachon
17 June 2022
Last Updated: 17 June 2022
app.py file for flask application 
'''

from flask import Flask
from flask import render_template

app = Flask(__name__)

# Creating route in flask
@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')


