import pandas as pd
from model import convertfiles_toratios
import psycopg2
import os
import io
from sqlalchemy import create_engine
import multiprocessing
import datetime


modelnamesB1=['ccsm3_B1.csv', 'cnrm_cm3_A1B.csv', 'echam5_B1.csv', 'echo_g_B1.csv','hadcm_B1.csv', 'pcm1_B1.csv']

modelnamesA1=['ccsm3_A1B','cgcm3.1_t47_A1B','cnrm_cm3_A1B','echam5_A1B',
                'echo_g_A1B', 'pcm1_A1B']

pathsA1=['reference_csv/ccsm3_A1B.csv',
                'reference_csv/cgcm3.1_t47_A1B.csv',
                'reference_csv/cnrm_cm3_A1B.csv',
                 'reference_csv/echam5_A1B.csv',
                 'reference_csv/echo_g_A1B.csv',
                'reference_csv/pcm1_A1B.csv'
                ]
db_name=os.environ['WW_DB_NAME']
db_host=os.environ['WW_DB_HOST']
db_username=os.environ['WW_DB_USERNAME']
db_password=os.environ['WW_DB_PASSWORD']
port=5432

def makedataframe_sqlformatA1(startyear, coord, endyear, dfpaths=pathsA1, modelist=modelnamesA1):
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


def make_coordlookup(latinterest, loninterest):
    coordlist=[str((latinterest[i],loninterest[i])) for i in range(len(latinterest))]
    return coordlist


def upload_log_entry(coord):
    #a1datalog table schema already loaded
    conn = psycopg2.connect(database=db_name, user=db_username, host=db_host, password=db_password)
    cursor = conn.cursor()
    logentry=[coord, datetime.datetime.now()]
    template = ', '.join(['%s'] * len(logentry))
    querylog = '''INSERT INTO a1datalog
               (coord, uploaded)
               VALUES ({})'''.format(template)

    cursor.execute(query=querylog, vars=logentry)
    conn.commit()

def upload_table_entry(coord):
    conn = psycopg2.connect(database=db_name, user=username, host=host, password=password)
    cursor = conn.cursor()

    template = ', '.join(['%s'] * len(df.columns))

    #table already created with constraints
    query = '''INSERT INTO a1data
       (ratios, percentile, year, model, lat, lon)
           VALUES ({})'''.format(template)

    startyear=2018
    endyear=2099
    df=makedataframe_sqlformatA1(startyear, coord, endyear)

    for index, row in df.iterrows():
        cursor.execute(query=query, vars=row)

    upload_log_entry(coord)
    conn.commit()

if __name__ == '__main__':
    locationparams=pd.read_csv('VIC_Castro_Regions.csv')
    locationparams.columns=['Latitude', 'Longitude', 'Region']

    lat=locationparams['Latitude']
    lon=locationparams['Longitude']

    coordlist=make_coordlookup(lat, lon)

    pool=multiprocessing.Pool(multiprocessing.cpu_count())
    pool.map(upload_table_entry, coordlist)
