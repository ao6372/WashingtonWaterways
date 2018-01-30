from netCDF4 import Dataset
import pandas as pd
import numpy as np
from collections import defaultdict
import requests
import shutil
import boto3
import os

def main(filepath="Database files/hb2860_transient_runs.ccsm3_A1B.example (2).nc"):
    #for each saved file it will clean it up and produce the DataFrame
    #add in a different file path if you want
    #This code has specifications for taking top value per year for
    #dates above 1985-10-1 for a specific file set
    group=Dataset(filepath)
    clist=makecoordlist(group)
    tlist=maketimelist(group)
    runoffdf=makedfrunoff(group, clist, tlist)
    baseflowdf=makedfbaseflow(group, clist, tlist)
    df=runoffdf+baseflowdf
    #this file already includes dates from 19850
    #change date if you want to include different window
    df=df[[c for c in df.columns if c >pd.to_datetime('1985-10-1')]]
    #add water yearfirst
    waterdf=addwateryear(df)
    #take top 30 values per year
    maxyearly=take_top_yearly_values(waterdf)
    #convert to cfs
    finaldf=maxyearly.apply(convertocfs)

    #saving example file -take out when actually running for other files
    finaldf.to_csv('CCSM3_A1BExample.csv')
    return finaldf

def awsmain(key, filename):
    s3=boto3.client("s3")
    #downloads from s3 bucket 'uwmodelfiles'
    #filename is the csv filename for the final cleaned df
    #This code has specifications for taking top value per year for
    #dates above 1985-10-1 for a specific file set
    response=s3.download_file(Bucket='uwmodelfiles',
                         Key=key,
                         Filename='placeholder.nc')
    group=Dataset('placeholder.nc')
    clist=makecoordlist(group)
    tlist=maketimelist(group)
    runoffdf=makedfrunoff(group, clist, tlist)
    baseflowdf=makedfbaseflow(group, clist, tlist)
    df=runoffdf+baseflowdf
    #this file already includes dates from 19850
    #change date if you want to include different window
    df=df[[c for c in df.columns if c >pd.to_datetime('1985-10-1')]]
    #add water yearfirst
    waterdf=addwateryear(df)
    #take top 30 values per year
    maxyearly=take_top_yearly_values(waterdf)
    #convert to cfs
    finaldf=maxyearly.apply(convertocfs)
    #finaldf.index=finaldf['wateryear']
    finaldf.to_csv(filename)
    os.remove('placeholder.nc')
    return finaldf


def makecoordlist(group):
    lats=group.variables['LAT'][:]
    lons=group.variables['LON'][:]
    coordlist=[str((lat,lon)) for lat in lats for lon in lons]
    return coordlist

def maketimelist(group):
    timestart=group.variables['TIME'].units[11:]
    totaldays=len(group.variables['TIME'][:])
    startstamp=pd.to_datetime(timestart, yearfirst=True)
    rng = pd.date_range(startstamp, periods=totaldays, freq='d')
    return rng

def makedfbaseflow(group,coordlist, timelist):
    coorddict=defaultdict(list)

    for i,timestamp in zip(range(len(timelist)),timelist):
        entry=group.variables['BASEFLOW'][i]
        entrylist=np.arange(0, len(entry.ravel()))
        coorddict[timestamp]=(entry.ravel())

    df=pd.DataFrame(coorddict, index=coordlist)
    return df

def makedfrunoff(group,coordlist, timelist=3):
    coorddict=defaultdict(list)

    for i,timestamp in zip(range(len(timelist)),timelist):
        entry=group.variables['RUNOFF'][i]
        entrylist=np.arange(0, len(entry.ravel()))
        coorddict[timestamp]=(entry.ravel())

    df=pd.DataFrame(coorddict, index=coordlist)
    return df

def addwateryear(df):
    #receives df with columns as datetime and columns as lat/lon in string
    #this is transposed to have datetime as index and lat/lon as columns
    df=df.T
    df['wateryear']=1
    for row in range(len(df)):
        year=df.index[row].year
        startdate=pd.to_datetime(str(year)+'-10'+'-1')
        if df.index[row]>=startdate:
            df['wateryear'][row]=year+1
        if df.index[row]<=startdate:
            df['wateryear'][row]=year
    return df

def take_top_yearly_values(df):
    #take df already with wateryear as a column
    #returns df of top 30 values per year
    #groupdf=df.groupby('wateryear')
    #dflist=[]
    #for col in df.columns:
        #df=groupdf[col].nlargest(30)
        #df.reset_index(level=1, drop=True, inplace=True)
        #dflist.append(df)
    #top30df=pd.concat(dflist, axis=1)

    groupdf=df.groupby('wateryear')
    return groupdf.max()


def convertocfs(entry):
    #Area of a 1/16 deg x 1/16 deg grid cell = 352006285.6 sq ft.
    #Conversion from mm to feet = 0.00328084 ft/mm
    #Conversion from days to seconds = 1/86400 days/sec
    #Product of all 3 = 13.36662
    return (entry)*13.36662


#scraping from database portion for multiple models
import time
import requests
from bs4 import BeautifulSoup

#scraping UW database portion
#make list of baselinks
def retrieveurls(baselink):
    response = requests.get(baselink)
    soup=BeautifulSoup(response.text, "html.parser")
    links=soup.find_all('a')
    #Note the [5:] is specific for the baselink
    #if using for another baselink, check manually the parse [5:]
    linklist=[datedlink for datedlink in [l['href'] for l in links][5:] if int(datedlink[32:38])>=198510]
    return linklist

def makelink(baselink, link):
    return baselink+link

def fetch_netcdf(url):
    """Fetch NetCDF data from URL and return Dataset."""

    data = requests.get(url).content
    with open('temp.nc', 'wb') as f:
        f.write(data)
    return Dataset('temp.nc')

def dl_allfiles(baselink, linklist):
    #each link is by month
    #concats all the monthly data sets into one
    #this is still raw and needs to be processed to take max val
    #and convert to cfs
    dflist=[]
    for link in linklist:
        group=dl_one_netcdf(baselink, link)
        clist=makecoordlist(group)
        tlist=maketimelist(group)
        baseflowdf=makedfbaseflow(group, clist,tlist)
        runoffdf=makedfrunoff(group, clist,tlist)
        df=runoffdf+baseflowdf
        dflist.append(df)
    totaldf=pd.concat(dflist,axis=1)
    return totaldf


if __name__ == '__main__':
    #reads off the bucket files to make dataframes with water year as index
    #columns are lat/lon combination
    keylist=['ccsm3_A1B/hb2860_transient_runs.ccsm3_A1B.nc',
                'ccsm3_B1/hb2860_transient_runs.ccsm3_B1.nc',
                'cgcm3.1_t47_A1B/hb2860_transient_runs.cgcm3.1_t47_A1B.nc',
                'cnrm_cm3_A1B/hb2860_transient_runs.cnrm_cm3_A1B.nc',
                'cnrm_cm3_B1/hb2860_transient_runs.cnrm_cm3_B1.nc',
                'echam5_A1B/hb2860_transient_runs.echam5_A1B.nc',
                'echam5_B1/hb2860_transient_runs.echam5_B1.nc',
                'echo_g_A1B/hb2860_transient_runs.echo_g_A1B.nc',
                'echo_g_B1/hb2860_transient_runs.echo_g_B1.nc',
                'hadcm_B1/hb2860_transient_runs.hadcm_B1.nc',
                'pcm1_A1B/hb2860_transient_runs.pcm1_A1B.nc',
                'pcm1_B1/hb2860_transient_runs.pcm1_B1.nc'
                ]
    filenames=['reference_csv/ccsm3_A1B.csv', 'reference_csv/ccsm3_B1.csv',
                'reference_csv/cgcm3.1_t47_A1B.csv', 'reference_csv/cnrm_cm3_A1B.csv',
                'reference_csv/cnrm_cm3_B1.csv', 'reference_csv/echam5_A1B.csv',
                'reference_csv/echam5_B1.csv', 'reference_csv/echo_g_A1B.csv',
                'reference_csv/echo_g_B1.csv', 'reference_csv/hadcm_B1.csv',
                'reference_csv/pcm1_A1B.csv', 'reference_csv/pcm1_B1.csv'
                ]

    for key,fn in zip(keylist, filenames):
        awsmain(key, fn)
