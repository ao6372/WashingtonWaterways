from netCDF4 import Dataset
import pandas as pd
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt


from scipy.stats import genextreme
from math import gamma
from location_parameters import find_sample_pctl
from location_parameters import find_beta_TBFW

#dfsource=pd.read_csv('CCSM3_A1BExample.csv')
#dfsource.index=dfsource['wateryear']
#reads in the saved file on the server that has all necessary values for reference

def get_extreme_values(year, coord, dfsource):
    #takes the dataframe that is already cleaned (should be processed
    #through NetCDFDataClean.py) and has wateryear as the index
    #should have lat/lon in columns
    #design lifetime is in years
    #this function returns the top values for the last 30 years in reference to year
    #GEV are based on year of interest -30 to year of interest
    #coord must be in string with a space formatted like so '(48.71875, -122.09375)'
    startyr=year-30
    dfyears=dfsource[(dfsource.index>startyr) & (dfsource.index<=year)][coord]
    return np.array(dfyears)

def calc_betas(dataarray):
    #Data is max points
    #n is count of Data
    #Data needs to be in descending order
    n=len(dataarray)
    data=np.sort(dataarray)[::-1]
    #rank is an array of integers from 1 to n inclusive of n
    rank=np.arange(1,len(data)+1)
    B0=data.mean()
    B1=sum((n-rank)/(n*(n-1))*data)
    B2=sum(((n-rank)*(n-rank-1))/(n*(n-1)*(n-2))*data)
    B3=sum(((n-rank)*(n-rank-1)*(n-rank-2))/(n*(n-1)*(n-2)*(n-3))*data)
    return B0, B1, B2, B3

def calc_LMoments(B0, B1, B2, B3):
    L1=B0
    L2 = 2*B1-B0
    L3 = 6*B2-6*B1+B0
    L4 = 20*B3-30*B2+12*B1-B0
    return L1, L2, L3, L4

def calc_skew_kurt(L2, L3, L4):
    skew=L3/L2
    kurt=L4/L3
    return skew, kurt

def calc_shape_scale_loc(skew, kurt, L1, L2):
    #shape = Kappa in notes = c in scipy
    #scale=Alpha in notes=scale in scipy
    #location=Xi in notes=loc in scipy
    c = 2/(3+skew)-np.log(2)/np.log(3)
    shape = 7.859*c+2.9554*(c**2) #kappa

    if shape==0:
        scale=L2/np.log(2)
        loc=L1-.5772*scale
    else:
        g1=gamma(1+shape)
        scale=shape*L2/(g1*(1-2**(-shape)))
        loc=L1+scale*(g1-1)/shape

    return shape, loc, scale


#modeling portion
def make_gev(dataarray, pctl):
    #sample from datarray already filtered for year and coord
    #right now sample 20
    #the .1667 is based on 1.2 yr and this changes with different regions
    extreme_vals_samp=np.random.choice(dataarray, 20, replace=False)
    #calculate new moments for each sample group
    B0,B1,B2,B3=calc_betas(extreme_vals_samp)
    L1,L2,L3,L4=calc_LMoments(B0,B1,B2,B3)
    skew, kurt=calc_skew_kurt(L2,L3,L4)
    shape, loc, scale=calc_shape_scale_loc(skew, kurt, L1,L2)
    #ppf is inverse of cdf
    #given percentile returns value
    #use L moment evaluation
    if shape==0:
        Qpctl=loc-scale*np.log(-np.log(pctl))
    else:
        Qpctl=loc+scale/shape*(1-(-np.log(pctl))**shape)

    return Qpctl

def make_gev_samples(dataarray, year, pctl, n=1000):
    #makes 1000 gevs
    #dataarray should already be filtered for the year and coord
    #returns dataframe with columns of the year
    samplist=[]
    for i in range(n):
        #each iteration makes a new subsample of 20 points and makes a new GEV
        Qpctl=make_gev(dataarray, pctl)
        samplist.append(Qpctl)

    sampdf=pd.DataFrame(samplist)
    sampdf.columns=[year]
    return sampdf

def gev_samples_allyears(startyear, coord, endyear, dfsource):
    #coord must be in string with a space formatted like so '(48.71875, -122.09375)'
    #returns dfs with n (default 1000) samples per year
    sampdflist=[]
    #adjusts for different TBFW in different regions
    #adjusts for beta in different regions
    beta, TBFW=find_beta_TBFW(coord)
    pctl=find_sample_pctl(TBFW)

    for year in range(startyear, endyear+1):
        dataarray=get_extreme_values(year, coord, dfsource)
        sampdf=make_gev_samples(dataarray, year, pctl)
        sampdflist.append(sampdf)

    gevsampsallyrs=pd.concat(sampdflist, axis=1)

    return gevsampsallyrs

def make_ratios(gevsampsallyrs):
    #makes ratios of the year over current year
    #makes dataframe with number of sample entries in rows and columns are yeari/year0
    ratiolist=[]
    for year in gevsampsallyrs.columns[1:]:
        ratioentry=gevsampsallyrs[year]/gevsampsallyrs[gevsampsallyrs.columns[0]]
        entrycol=pd.DataFrame(ratioentry)
        entrycol.columns=[str(year)]
        ratiolist.append(entrycol)
        #always divide by start current year
    ratiodf=pd.concat(ratiolist, axis=1)
    return ratiodf

def find_percentiles(df):
    #this is set to take the quantiles for 95 and 5
    #returns an array with 5 and 95 percentile in that order
    return df.quantile(q=[.05,.5,.95])

#plot one model
def plot_dist_quantiles(yearstart, yearend, df):
    fig = plt.figure()
    fig, ax=plt.subplots(figsize=(10,5))
    ax.plot(df.columns, df.iloc[0], label='5th Percentile')
    ax.plot(df.columns, df.iloc[1], label='50th Percentile')
    ax.plot(df.columns, df.iloc[2], label='95th Percentile')
    ax.set_xlabel('Year')
    ax.set_ylabel('Ratio')
    ax.set_title('Ratio of Stream Flow {} - {}'.format(yearstart,yearend))
    ax.legend()
    return fig


def convertfiles_toratios(startyear, coord, endyear, dfsource):
    beta, TBFW=find_beta_TBFW(coord)
    gevsampsallyrs=gev_samples_allyears(startyear, coord, endyear, dfsource)
    ratiodf=make_ratios(gevsampsallyrs)
    ratiodfbeta=ratiodf**beta
    pctldf=find_percentiles(ratiodf)
    return pctldf
