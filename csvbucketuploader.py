import pandas as pd
import numpy as np
import requests
import boto3
import os
from io import StringIO
from multiplemodels import make_multimodel_plotdataA1

modelist=['ccsm3_A1B','cgcm3.1_t47_A1B','cnrm_cm3_A1B','echam5_A1B',
                'echo_g_A1B', 'pcm1_A1B']

paths=['reference_csv/ccsm3_A1B.csv',
                'reference_csv/cgcm3.1_t47_A1B.csv',
                'reference_csv/cnrm_cm3_A1B.csv',
                 'reference_csv/echam5_A1B.csv',
                 'reference_csv/echo_g_A1B.csv',
                'reference_csv/pcm1_A1B.csv'
                ]

def get_cumulative_pctchange(dfsqlall):
    #gets average of the five percentile values
    dfsqlallyrgrp=dfsqlall[dfsqlall['percentile']==.05].groupby('year')
    avgdfsql=dfsqlallyrgrp['ratios'].mean()
    avgdflist=list(avgdfsql.values)
    percentchange=[abs(avgdflist[i]-avgdflist[i-1])/avgdflist[i-1]
                    for i in range(len(avgdflist))]
    return  sum(percentchange)


def make_coordlookup(latinterest, loninterest):
    #coordinates are lat and lon combinations
    #strings formatted need to be like so '(48.71875, -122.09375)'
    coordlist=[str((lat,lon)) for lat in latinterest for lon in loninterest]
    return coordlist

def makefoldname_fromcoord(coord):
    key=c[1:3]+c[4:9]+'_'+c[12:15]+c[16:20]
    return key

def csvuploadermain():

    s3=boto3.client("s3")
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
    bucket_name=washingtonwaterwaycsv

    for coord in coordlist:
        downloaddata, ratiodata, avgratio=make_multimodel_plotdataA1(coord, startyear, endyear)
        foldername=makefoldname_fromcoord(coord)
        os.system('mkdir {}'.format(foldername))
        downloaddata.to_csv('{}/download.csv'.format(foldername))
        ratiodata.to_csv('{}/ratio.csv'.format(foldername))
        ratiodata.to_csv('{}/avgratio.csv'.format(foldername))

        bucketloc='s3://{}/{}'.format(bucket_name, foldername)
        aws_base_command='aws s3 sync {}'.format(foldername)
        os.system(aws_base_command+" {}".format(bucketloc))
        os.system('rm -r {}'.format(foldername))

if __name__ == '__main__':
    csvuploadermain()
