import os
import glob
import pandas as pd
import warnings
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)



def read_puma(path):
    """
    Reads puma data into data frame. The puma data stores by states in txt format.
    
    Parameters
    ----------
    path: str
        path name of txt puma file
    Returns
    -------
    pandas.datafranme
        the returned dataframe has different levels of fips, population size etc. from txt file
    """

    # Please refer 2010_PUMA_Equivalency_Format_Layout to check he record layouts for each field 
    colspecs = [(0,3),(3,5),(5,13),(13,18),(18,21),(21,29),(29,34),(34,42),(42,47),(47,55),(55,61),(61,70),(70,79),(79,178)]
    names = ['sl','state_fips','state_national_standards','puma_code','county_fips','county_national_standards',
        'county_sub_fips','county_sub_national_standards','place_fips','place_national_standards','tract_code',
        'population','house_number','area_name']
    # Read a table of fixed-width formatted lines from .txt into DataFrame.
    df = pd.read_fwf(path,colspecs=colspecs,names=names,dtype=str,encoding='latin1')
    # change data type of some variables
    df['population'] = df['population'].astype('float')
    df['house_number'] = df['house_number'].astype('float')
    # add a column called year
    df['year'] = 2010
    return df

def puma_crosswalk(path, nyc_wa_path):
    """
    This function is to create a puma crosswalk with county and subcounty.
    If the puma is in Aew England Area, use sub county(level 797) as sss_place(place).
    Otherwise the county is assigned to sss_place(place).
    For State of Washington and New York City, some puma code area names are replace by more meaningful names.
    
    Parameters
    ----------
    path: str
        path name of txt puma file
    nyc_wa_path: str
        excel file path of nyc and statement of washington replacement name list 
    Returns
    -------
    pandas.datafranme
        the returned crosswalk dataframe has variables for database such as county_fips, subcounty_fips, puma_code,
        population, population weight
    """

    # read txt file into datdframe
    puma_txt = read_puma(path)
    # save the population of each puma are
    puma_pop = puma_txt[['puma_code','population']].groupby('puma_code').agg('max').reset_index()
    a_set = set(puma_txt['state_fips'])
    matches = ['25','09','23','33','44','50']
    # if the area is in new england area, use sub county(level 797) as place
    if ('797' in set(puma_txt['sl'])) and (any(x in a_set for x in matches)):
        # retrieve sub county information
        county_sub = puma_txt[puma_txt['sl'] == '797']
        county_sub.rename(columns={'area_name':'county_sub'}, inplace=True)
        # retrieve sub county fips code and area name
        county = puma_txt[puma_txt['sl'] == '796']
        county =county[['county_fips','area_name']]
        county = county.drop_duplicates()
        county.columns=['county_fips','county']
        # retrieve puma code and area name
        puma = puma_txt[puma_txt['sl'] == '795']
        puma =puma[['puma_code','area_name']]
        puma = puma.drop_duplicates()
        puma.columns=['puma_code','puma_area']
        # merge subcounty, county and puma to create a crosswalk file for these three geos
        crosswalk = county_sub.merge(county, how='left')
        crosswalk = crosswalk.merge(puma, how='left')
        # only keep columns of interests
        crosswalk = crosswalk[['sl', 'state_fips', 'puma_code','county_fips', 'county_sub_fips',
               'county_sub', 'county', 'puma_area','population','year']]
        crosswalk['place'] = crosswalk['county_sub']
    # if the area is not in new england, only use puma and county 
    else:
        # retrieve sub county information
        county = puma_txt[puma_txt['sl'] == '796']
        county.rename(columns={'area_name':'county'}, inplace=True)
        # retrieve puma code and area name
        puma = puma_txt[puma_txt['sl'] == '795']
        puma =puma[['puma_code','area_name']]
        puma = puma.drop_duplicates()
        puma.columns=['puma_code','puma_area']
        # left join county and puma by puma code
        crosswalk = county.merge(puma, how='left')
        # only keep columns of interests
        crosswalk = crosswalk[['sl', 'state_fips', 'puma_code','county_fips', 'county', 'puma_area','population']]
        #creat place(sssplace)
        crosswalk['place'] = crosswalk['county']
    # attach population of each puma to the crosswalk file
    crosswalk = crosswalk.merge(puma_pop, on = 'puma_code',suffixes=('_self','_max'))
    # accoridng to population of each row and population of puma to create a population weight
    crosswalk['weight'] = crosswalk['population_self']/crosswalk['population_max']

    # TODO: if the puma name and city file is better designed, the code could be easier
    #if the file is State of Washington, replace some 'place' name to meaningful names e.g. "King(part)"-->"Seattle"
    if '53' in set(crosswalk['state_fips']):
        # read file and sheet_name 0 is the state of washington
        wa = pd.read_excel(nyc_wa_path, sheet_name = 0)
        # the length of puma code should be 5. Some are not due to data type. 
        # If it is not 5 digits, add "0" s to make it len()==5
        wa['PUMA'] = wa['PUMA'].astype('int').astype('str').str.zfill(5)
        wa = wa[['PUMA','Place']]
        wa.columns = ['puma_code','new_place']
        # left join between crosswalk and wa
        crosswalk = crosswalk.merge(wa, how='left')
        # meaningful names are in the column 'new_place'. If it is NA in 'new_place', filled by old 'place'
        crosswalk['new_place'] = crosswalk['new_place'].fillna(crosswalk['place'])
        # drop 'place'
        crosswalk = crosswalk.drop('place',axis=1)
        # rename new_place --> place 
        crosswalk.rename(columns={'new_place':'place'}, inplace=True)

    #if the file is NYC, replace some 'place' names to meaningful names      
    if '36' in set(crosswalk['state_fips']):
        # read file and sheet_name 1 is NYC
        nyc = pd.read_excel(nyc_wa_path, sheet_name = 1)
        # add "0" s to make it len()==5
        nyc['PUMA'] = nyc['PUMA'].astype('int').astype('str').str.zfill(5)
        nyc = nyc[['PUMA','AreaName']]
        nyc.columns = ['puma_code','new_place']
        crosswalk = crosswalk.merge(nyc, how='left')
        crosswalk['new_place'] = crosswalk['new_place'].fillna(crosswalk['place'])
        crosswalk = crosswalk.drop('place',axis=1)
        # rename new_place --> place 
        crosswalk.rename(columns={'new_place':'place'}, inplace=True)
    
    return crosswalk
