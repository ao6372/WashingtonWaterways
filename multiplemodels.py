from netCDF4 import Dataset
import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

from scipy.stats import genextreme
from math import gamma
from location_parameters import find_sample_pctl
from location_parameters import find_beta_TBFW

from model import gev_samples_allyears

#list of file location references
#order matters to know which models made which percentile that jumped
dfpaths=[]
#associated models with each path
dfpathsnames=[]
pctldfslist=[]

def gevsamps_modelsyears(startyear, coord, endyear):
    #returns the .05,.5,.95 of all the samples GEV values
    for dfpath in dfpaths:
        df=pd.read_csv(dfpath)
        pctldf=convertfiles_toratios(startyear, coord, endyear, dfsource=df)
        pctldfslist.append(pctldf)
    return pd.concat(pctldfslist)

def above_threshold(thresh, dfpctls, coord):
    #takes list of dataframes and looks for 5th Percentile for all models
    #records year
    fivepctldf=dfpctls.groupby(dfpctls.index).get_group(.05)
    vote=fivpctl[fivpctl>thresh].count(axis=0)
    votepctls=vote/fivpctl.shape[0] #divides by number of models
    return votepctls

def
