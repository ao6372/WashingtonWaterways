from __future__ import division
from flask import Flask, render_template, request, jsonify
from math import sqrt
import numpy as np
import pandas as pd
from io import StringIO, BytesIO
import csv
from flask import make_response
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
from random import random
from model import ( onclick_main)

app = Flask(__name__)
#data_model = DataModel()

@app.route('/')
def contactform():
    return render_template('index.html')
#
# @app.route('/download')
# def generatefile():
#     #save the contact.html in template directory
#     #in the future put render_template('contact.html')
#     output=post(dffilepath)
#     return output

# def post(dffilepath):



@app.route('/foo')
def foo():
    return '''
        <h2>Here's my plot!</h2>
        <img src='/foo/plot/5'>
        <img src='/foo/plot/10'>
        <img src='/foo/plot/15'>
        '''


@app.route('/foo/plot/<int:n>')
def get_graph(n):
    plt.figure()
    plt.plot(range(n), [random() for i in range(n)])
    image = BytesIO()
    plt.savefig(image)
    return image.getvalue(), 200, {'Content-Type': 'image/png'}



@app.route('/calculate')
def graph():
    #graphs for a specific coordinate
    #supposed to have input year and design year and coordinates
    startyr=int(user_data['Startyear'])
    coord=user_data['Lattitude']+user_data['Longitude']
    endyr=int(user_data['Endyear'])
    fig=onclick_main(2030, '(48.71875, -122.09375)', 2070)
    image = BytesIO()
    fig.savefig(image)
    return image.getvalue(), 200, {'Content-Type': 'image/png'}

@app.route('/download')
def generatefile():
    #save the contact.html in template directory
    #in the future put render_template('contact.html')
    output=post(dffilepath)
    return output

def post(dffilepath):
    with open('dffilepath', 'r' )as f:
        content=f.read()

    si = StringIO.StringIO()
    cw = csv.writer(si)
    cw.write(content)
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=fraud.csv"
    output.headers["Content-type"] = "text/csv"
    #message to browser to return text as csv
    return output


if __name__ == '__main__':
    #do not actually run website with debug=True
    #or from terminal export FLASK_DEBUG=1
    app.run(host='0.0.0.0', threaded=True)
