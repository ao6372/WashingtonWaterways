import pandas as pd
import numpy as np
from model import convertfiles_toratios

import psycopg2
import os
from io import StringIO

modelist=['ccsm3_A1B','cgcm3.1_t47_A1B','cnrm_cm3_A1B','echam5_A1B',
                'echo_g_A1B', 'pcm1_A1B']

paths=['reference_csv/ccsm3_A1B.csv',
                'reference_csv/cgcm3.1_t47_A1B.csv',
                'reference_csv/cnrm_cm3_A1B.csv',
                 'reference_csv/echam5_A1B.csv',
                 'reference_csv/echo_g_A1B.csv',
                'reference_csv/pcm1_A1B.csv'
                ]
def convertdf_tosql(startyear, coord, endyear, dfpaths=paths, modelist=modelist):
    pctldfslist=[]
    lat=float(coord[1:9])
    lon=float(coord[11:20])
    for dfpath,modelname in zip(dfpaths, modelist):
        df=pd.read_csv(dfpath)
        df.index=df['wateryear']
        pctldf=convertfiles_toratios(startyear, coord, endyear, dfsource=df)
        tpctldf=pctldf.T
        five=tpctldf.iloc[:,0]
        fifty=tpctldf.iloc[:,1]
        ninetyfive=tpctldf.iloc[:,2]

        dfsql5=pd.DataFrame(data=five.values, columns=['ratios'])
        dfsql5['percentile']=.05
        dfsql5['year']=pctldf.columns
        dfsql50=pd.DataFrame(data=fifty.values, columns=['ratios'])
        dfsql50['percentile']=.5
        dfsql50['year']=pctldf.columns
        dfsql95=pd.DataFrame(data=ninetyfive.values, columns=['ratios'])
        dfsql95['percentile']=.95
        dfsql95['year']=pctldf.columns


        dfsql=pd.concat([dfsql5,dfsql50,dfsql95])
        dfsql['model']=modelname
        pctldfslist.append(dfsql)

    dfsqlall=pd.concat(pctldfslist)
    dfsqlall['lat']=lat
    dfsqlall['lon']=lon

    return dfsqlall

def make_coordlookup(latinterest, loninterest):
    #coordinates are lat and lon combinations
    #strings formatted need to be like so '(48.71875, -122.09375)'
    coordlist=[str((lat,lon)) for latinterest in lats for lon in loninterest]
    return coordlist

def main():
    latinterest=[47.03125, 47.09375, 47.15625, 47.21875,
            47.28125, 47.34375, 47.40625, 47.46875, 47.53125,
            47.59375, 47.65625, 47.71875, 47.78125,47.84375,
            47.90625, 47.96875, 48.03125, 48.09375]
    loninterest=[-122.7812,-122.7187,-122.6562,-122.5937,-122.5312,
                -122.4687,-122.4062,-122.3437,-122.2812,-122.2187,
                -122.1562,-122.0937,-122.0312, -121.9687,-121.9062,
                -121.8437,-121.7812,-121.7187]
    startyear=2015
    endyear=2099
    coordlist=make_coordlookup(latinterest, loninterest)

    for coord in coordlist:
        sqldf=convertdf_tosql(startyear, coord, endyear)
        #add to SQL?
