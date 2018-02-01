import pandas as pd
import numpy as np
from model import convertfiles_toratios
import requests
import boto3
import psycopg2
import os
from io import StringIO
from multiplemodels import make_multimodel_plotdataA1


def convertdf_tosql(startyear, coord, endyear, dfpaths=paths, modelist=modelist):
    pctldfslist=[]
    lat=float(coord[1:9])
    lon=float(coord[11:20])
    for dfpath,modelname in zip(dfpaths, modelist):
        df=pd.read_csv(dfpath)
        df.index=df['wateryear']
        pctldf=convertfiles_toratios(startyear, coord, endyear, dfsource=df)

        #format portion
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
