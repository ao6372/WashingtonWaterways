#location influences several factors
#the year window average the quantile needed to sample from each GEV
#the beta to raise the ratios of BFW
import pandas as pd

locationparams=pd.read_csv('VIC_Castro_Regions.csv')
locationparams.columns=['Lattitude', 'Longitude', 'Region']

def find_sample_pctl(TBFW):
    q=1-1/TBFW
    return q

def make_latlon(coord):
    latlon=coord.strip('()').split(',')

    lat=latlon[0]
    lon=latlon[1][1:]
    return lat, lon

def find_beta_TBFW(coord, dfsource=locationparams):
    #coord must be a string like '(48.71875, -122.09375)'
    #returns the region and the TBFW and beta
    lat, lon=make_latlon(coord)
    #extracts region from reference file
    #based on
    try:
        r=locationparams[(locationparams['Lattitude']==float(lat))&
               (locationparams['Longitude']==float(lon))]['Region'].values[0]
    except IndexError as e:
        with open('missing.log', 'a') as f:
            f.write(coord + '\n')
            return (0, 0)
        #msg=f"lat is {lat}, lon is {lon}, shape of r is {r.shape}, error is {repr(e)}"
        #raise IndexError(msg)
    except ValueError as e:
        msg=f"lat is {lat}, lon is {lon}, error is {repr(e)}"
        raise ValueError(msg)

    if r=='CP':
        beta=.6
        TBFW=1.4

    if r=='WC':
        beta=.44
        TBFW=1.5

    if r=='PM':
        beta=.5
        TBFW=1.2

    return .6, 1.4
