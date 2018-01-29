#location influences several factors
#the year window average the quantile needed to sample from each GEV
#the beta to raise the ratios of BFW
import pandas as pd

locationparams=pd.read_csv('VIC_Castro_Regions.csv')
locationparams.columns=['Lattitude', 'Longitude', 'Region']

def find_sample_pctl(TBFW):
    q=1-1/TBFW
    return q

def find_beta_TBFW(coord, dfsource=locationparams):
    #coord must be a string like '(48.71875, -122.09375)'
    #returns the region and the TBFW and beta
    lat=coord[1:9]
    lon=coord[11:21]
    #extracts region from reference file
    r=locationparams[(locationparams['Lattitude']==float(lat))&
               (locationparams['Longitude']==float(lon))]['Region'].values[0]

    if r=='CP':
        beta=.6
        TBFW=1.4

    if r=='WC':
        beta=.44
        TBFW=1.5

    if r=='PM':
        beta=.5
        TBFW=1.2

    return beta, TBFW
