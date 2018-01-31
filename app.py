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
from multiplemodels import make_multimodel_plotdataA1

app = Flask(__name__)
#data_model = DataModel()

@app.route('/')
def mainpage():
    return render_template('index1.html')


#Make download option for fivepctldf
# @app.route('/download')
# def generatefile():
#     #save the contact.html in template directory
#     #in the future put render_template('contact.html')
#     output=post(dffilepath)
#     return output

@app.route('/calculate', methods=['POST'])
def getinputs():
    user_data=request.json
    print(user_data)
    thresh=int(user_data['thresh'])
    startyr=int(user_data['startyr'])
    coord=user_data['lat']+user_data['lon']
    endyr=int(user_data['endyr'])


def graph():
    #image = BytesIO()
    #fig.savefig(image)
    return 'went through' #image.getvalue(), 200, {'Content-Type': 'image/png'}

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
    output.headers["Content-Disposition"] = "attachment; filename=bfwratios.csv"
    output.headers["Content-type"] = "text/csv"
    #message to browser to return text as csv
    return output


if __name__ == '__main__':
    #do not actually run website with debug=True
    #or from terminal export FLASK_DEBUG=1
    app.run(host='0.0.0.0', threaded=True)
