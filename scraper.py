import requests
import boto3
from bs4 import BeautifulSoup

s3=boto3.client("s3")
baselink="http://cses.washington.edu/picea/mauger/2018_04_SC2_Culverts/DATA/WA_tr_hb2860/"

linklist=['ccsm3_A1B/hb2860_transient_runs.ccsm3_A1B.nc',
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


def makelink(baselink, link):
    return baselink+link

def fetch_data(url):
    """Fetch data from a URL, raise exception if status code not 200"""
    response = requests.get(url)
    if response.status_code != 200:
        raise IOError("Unable to fetch data, status code " +
                      str(response.status_code) + ": " +
                      response.content.decode())
    return response.content


def fetch_netcdf(baselink, link):
    """Fetch NetCDF data from URL and return Dataset."""
    url=makelink(baselink, link)
    data = fetch_data(url)
    s3.put_object(Bucket='uwmodelfiles',
             Key=link,
             Body=data)

def fetch_all_files(baselink):
    #linklist=retrieveurls(baselink)
    for link in linklist:
        fetch_netcdf(baselink, link)


if __name__=="__main__":
    fetch_all_files(baselink)
