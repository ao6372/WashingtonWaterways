from netCDF4 import Dataset
import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

from scipy.stats import genextreme
from math import gamma
from location_parameters import find_sample_pctl
from location_parameters import find_beta_TBFW

from model import convertfiles_toratios

#list of file location references
#order matters to know which models made which percentile that jumped




#associated models with each path for researcher reference
modelnamesA1=['ccsm3_A1B','cgcm3.1_t47_A1B','cnrm_cm3_A1B','echam5_A1B',
                'echo_g_A1B', 'pcm1_A1B']

modelnamesB1=['ccsm3_B1.csv', 'cnrm_cm3_A1B.csv', 'echam5_B1.csv', 'echo_g_B1.csv','hadcm_B1.csv', 'pcm1_B1.csv']


def gevsamps_modelsyears(startyear, coord, endyear, dfpaths):
    #returns the .05,.5,.95 of all the samples GEV values
    pctldfslist=[]
    for dfpath in dfpaths:
        df=pd.read_csv(dfpath)
        df.index=df['wateryear']
        pctldf=convertfiles_toratios(startyear, coord, endyear, dfsource=df)
        pctldfslist.append(pctldf)
    dfpctls=pd.concat(pctldfslist)
    return dfpctls

def get_fivepctl(dfpctls):
    fivepctldf=dfpctls.groupby(dfpctls.index).get_group(.05)
    return fivepctldf

def above_threshold(thresh, fivepctldf, coord):
    #takes list of dataframes and looks for 5th Percentile for all models
    #records year
    vote=fivepctldf[fivepctldf>thresh].count(axis=0)
    votepctls=vote/fivepctldf.shape[0] #divides by number of models
    return votepctls

def get_avgpctls(allyearpctls):
    groupedf=allyearpctls.groupby(allyearpctls.index)
    meandf=groupedf.mean()
    return meandf


def plot_fivepctls(fivepctldf, votepctl, startyear, endyear, thresh, coord):
    #model map
    x=np.arange(startyear+1,endyear+1)
    yscale=np.linspace(.1,1,10)
    fig = plt.figure()
    fig, ax=plt.subplots(figsize=(10,5))
    for row in range(fivepctldf.shape[0]):
        y=fivepctldf.iloc[row:].values[0]
        ax.plot(x, y, 'blue', alpha=.3)
    ax.plot(x, fivepctldf.mean(), 'blue', label='average')
    ax.legend()
    ax.set_xlabel('Year')
    ax.set_ylabel('BFW/BFW0')
    ax.set_title('Ratio of Stream Flow {} - {} for {}'.format(startyear+1,endyear, coord))
    ax.axhline(thresh, label='Threshold', color= 'black')

    #probability graph
    fig2, ax2=plt.subplots(figsize=(10,5))
    ax2.set_title('Probability of Stream Ratio above Threshold {} - {} for {}'.format(startyear+1,endyear, coord))
    ax2.plot(x, votepctl ,'r', label='Probability' )
    ax2.tick_params('y', colors='r')
    ax2.set_yticks(yscale)
    ax2.set_ylabel('Probability Above Threshold (%)')
    ax2.legend()
    return fig, fig2

def make_multimodel_plotdataA1(coord, startyear, endyear):
    paths=['reference_csv/ccsm3_A1B.csv',
                    'reference_csv/cgcm3.1_t47_A1B.csv',
                    'reference_csv/cnrm_cm3_A1B.csv',
                     'reference_csv/echam5_A1B.csv',
                     'reference_csv/echo_g_A1B.csv',
                    'reference_csv/pcm1_A1B.csv'
                    ]
    dfpctls=gevsamps_modelsyears(startyear, coord, endyear, paths)
    downloaddata=get_avgpctls(dfpctls) #for downloading analysis
    ratiodata=get_fivepctl(dfpctls)
    avgratio=ratiodata.mean()
    #probabilitydata=above_threshold(thresh, modelgraphdata, coord)
    return downloaddata, ratiodata, avgratio


def make_multimodel_plotdataB1(coord, startyear, endyear, thresh):
    paths=['reference_csv/ccsm3_B1.csv',
                'reference_csv/cnrm_cm3_B1.csv',
                'reference_csv/echam5_B1.csv',
                'reference_csv/echo_g_B1.csv',
                'reference_csv/hadcm_B1.csv',
                'reference_csv/pcm1_B1.csv'
                ]

    dfpctls=gevsamps_modelsyears(startyear, coord, endyear, paths)
    meandf=get_avgpctls(dfpctls) #for downloading analysis
    fivepctldf=get_fivepctl(dfpctls)
    votepctl=above_threshold(thresh, fivepctldf, coord)
    return
