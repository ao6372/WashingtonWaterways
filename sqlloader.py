import pandas as pd
from model import convertfiles_toratios
from multiplemodels import make_multimodel_plotdataA1
import psycopg2
import os
import io
from sqlalchemy import create_engine
import multiprocessing


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



def write_to_table(df, db_engine, table_name, if_exists='fail'):
    string_data_io = io.StringIO()
    df.to_csv(string_data_io, sep='|', index=False)
    pd_sql_engine = pd.io.sql.pandasSQL_builder(db_engine)
    table = pd.io.sql.SQLTable(table_name, pd_sql_engine, frame=df,
                               index=False, if_exists=if_exists)
    table.create()
    string_data_io.seek(0)
    string_data_io.readline()  # remove header
    with db_engine.connect() as connection:
        with connection.connection.cursor() as cursor:
            copy_cmd = "COPY %s FROM STDIN HEADER DELIMITER '|' CSV" % table_name
            cursor.copy_expert(copy_cmd, string_data_io)
        connection.connection.commit()

def make_coordlookup(latinterest, loninterest):
    #coordinates are lat and lon combinations
    #strings formatted need to be like so '(48.71875, -122.09375)'
    coordlist=[str((lat,lon)) for lat in latinterest for lon in loninterest]
    return coordlist

def main(coordlist):
    db_name=os.environ['DB_NAME']
    db_host=os.environ['DB_HOST']
    db_username=os.environ['DB_USERNAME']
    db_password=os.environ['DB_PASSWORD']
    port=5432
    # conn = psycopg2.connect('dbname={}, host={}, user={}, password={}, port={}'
    #                     .format(db_name, db_host, db_username, db_password, port))
    startyear=2015
    endyear=2099
    address = "postgresql://{}:{}@{}:{}/{}".format(db_username, db_password, db_host, port, db_name)
    engine = create_engine(address)
    for coord in coordlist:
        df=makedataframe_sqlformatA1(startyear, coord, endyear)

        write_to_table(df, engine, 'A1Data', 'append')

if __name__ == '__main__':
    latinterest=[47.03125, 47.09375, 47.15625, 47.21875,
                47.28125, 47.34375, 47.40625, 47.46875, 47.53125,
                47.59375, 47.65625, 47.71875, 47.78125,47.84375,
                47.90625, 47.96875, 48.03125, 48.09375]
    loninterest=[-122.78125,-122.71875,-122.65625,-122.59375,-122.53125,
                    -122.46875,-122.40625,-122.34375,-122.28125,-122.21875,
                    -122.15625,-122.09375,-122.03125, -121.96875,-121.90625,
                    -121.84375,-121.78125,-121.71875]

    coordlist=make_coordlookup(latinterest, loninterest)

    main(coordlist)
