import os
import glob

from .base import Base, AutomappedDB, get_db_file
from . import preprocess

import pandas as pd
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
)

import warnings
from pandas.errors import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)

puma_state_numbers_to_abbreviations = {
    '53': 'WA',
    '10': 'DE',
    '11': 'DC',
    '55': 'WI',
    '54': 'WV',
    '15': 'HI',
    '12': 'FL',
    '56': 'WY',
    '72': 'PR',
    '34': 'NJ',
    '35': 'NM',
    '48': 'TX',
    '22': 'LA',
    '37': 'NC',
    '38': 'ND',
    '31': 'NE',
    '47': 'TN',
    '36': 'NY',
    '42': 'PA',
    '02': 'AK',
    '32': 'NV',
    '33': 'NH',
    '51': 'VA',
    '08': 'CO',
    '06': 'CA',
    '01': 'AL',
    '05': 'AR',
    '50': 'VT',
    '17': 'IL',
    '13': 'GA',
    '18': 'IN',
    '19': 'IA',
    '25': 'MA',
    '04': 'AZ',
    '16': 'ID',
    '09': 'CT',
    '23': 'ME',
    '24': 'MD',
    '40': 'OK',
    '39': 'OH',
    '49': 'UT',
    '29': 'MO',
    '27': 'MN',
    '26': 'MI',
    '44': 'RI',
    '20': 'KS',
    '30': 'MT',
    '28': 'MS',
    '45': 'SC',
    '21': 'KY',
    '41': 'OR',
    '46': 'SD'
}

new_england_state_nums = ['25', '09', '23', '33', '44', '50']


# declare PUMA data columns and data type
class PUMA(Base):
    """
    This class defines the ``puma`` table.

    PUMA stands for Public Use Microdata Area from the Census.

    Attributes
    ----------
    summary_level : String Column
        Summary Level Code
    state_fips : String Column
        State FIPS Code
    state : String Column
        state name, e.g. WA
    puma_code : String Column
        PUMA Code
    county_fips : String Column
        County FIPS Code
    county_sub_fips : String Column
        County Subdivision FIPS Code
    county_sub : String Column
        name of the county sub
    county : String Column
         name of the county
    puma_area : String Column
        name of the puma area
    place : String Column
        name of the sss place
    population : Integer Column
        population of the puma
    weight : Float Column
        weight of population based on puma
    year : Integer Column
        the year of population

    """
    __tablename__ = 'puma'
    summary_level = Column('summary_level', String)
    state_fips = Column('state_fips', String)
    state = Column('state', String, primary_key=True)
    puma_code = Column('puma_code', String, primary_key=True)
    county_fips = Column('county_fips', String)
    county_sub_fips = Column('county_sub_fips', String)
    county_sub = Column('county_sub', String)
    county = Column('county', String)
    puma_area = Column('puma_area', String)
    place = Column('place', String, primary_key=True)
    population = Column('population', Integer)
    weight = Column('weight', Float)
    year = Column('year', Integer)


def read_puma(path, year):
    """
    Reads puma data into data frame.

    The puma data stores by states in txt format.

    Parameters
    ----------
    path : str
        path name of txt puma file
    year : int
        year of the puma data collected

    Returns
    -------
    pandas.datafranme
        the returned dataframe has different levels of fips,
        population size etc. from the puma txt file

    """
    # Please refer 2010_PUMA_Equivalency_Format_Layout to see record layouts
    colspecs = [
        (0, 3),
        (3, 5),
        (5, 13),
        (13, 18),
        (18, 21),
        (21, 29),
        (29, 34),
        (34, 42),
        (42, 47),
        (47, 55),
        (55, 61),
        (61, 70),
        (70, 79),
        (79, 178)
    ]
    names = [
        'summary_level',
        'state_fips',
        'state_national_standards',
        'puma_code',
        'county_fips',
        'county_national_standards',
        'county_sub_fips',
        'county_sub_national_standards',
        'place_fips',
        'place_national_standards',
        'tract_code',
        'population',
        'house_number',
        'area_name'
    ]
    # Read a table of fixed-width formatted lines from .txt into DataFrame.
    df = pd.read_fwf(
        path,
        colspecs=colspecs,
        names=names,
        dtype=str,
        encoding='latin1')
    # change data type of some variables
    df['population'] = df['population'].astype('float')
    df['house_number'] = df['house_number'].astype('float')
    # add a column called year
    df['year'] = year
    df['state'] = df['state_fips'].map(puma_state_numbers_to_abbreviations)
    return df


def puma_crosswalk(path, year, nyc_wa_path=None):
    """
    Create a puma crosswalk with county and subcounty.

    If the puma is in New England Area, use sub county(level 797)
    as sss_place(place). Otherwise the county is assigned to
    sss_place(place). For State of Washington and New York City,
    some puma code area names are replace by more meaningful names.

    Parameters
    ----------
    path : str
        path name of txt puma file
    year : int
        year of the puma data collected
    nyc_wa_path : str
        excel file path that create special areas in NYC and WA

    Returns
    -------
    pandas.datafranme
        the returned crosswalk dataframe has variables for database such as
        county_fips, subcounty_fips, puma_code, population, population weight

    """
    # read txt file into datdframe
    puma_txt = read_puma(path, year)
    # save the population of each puma are
    puma_pop = puma_txt[
        ['puma_code', 'population']].groupby(
            'puma_code').agg('max').reset_index()
    a_set = set(puma_txt['state_fips'])
    # if the area is in new england area, use sub county(level 797) as place
    if ('797' in set(
        puma_txt['summary_level'])) and (
                any(x in a_set for x in new_england_state_nums)):
        # retrieve sub county information
        county_sub = puma_txt[puma_txt['summary_level'] == '797']
        county_sub = county_sub.rename(columns={'area_name': 'county_sub'})
        # retrieve sub county fips code and area name
        county = puma_txt[puma_txt['summary_level'] == '796']
        county = county[['county_fips', 'area_name']]
        county = county.drop_duplicates()
        county.columns = ['county_fips', 'county']
        # retrieve puma code and area name
        puma = puma_txt[puma_txt['summary_level'] == '795']
        puma = puma[['puma_code', 'area_name']]
        puma = puma.drop_duplicates()
        puma.columns = ['puma_code', 'puma_area']
        # merge subcounty, county and
        # puma to create a crosswalk file for 3 geos
        crosswalk = county_sub.merge(county, how='left')
        crosswalk = crosswalk.merge(puma, how='left')
        # only keep columns of interests
        crosswalk = crosswalk[[
            'summary_level',
            'state_fips',
            'state',
            'puma_code',
            'county_fips',
            'county_sub_fips',
            'county_sub',
            'county',
            'puma_area',
            'population',
            'year']]
        crosswalk['place'] = crosswalk['county_sub']
    # if the area is not in new england, only use puma and county
    else:
        # retrieve sub county information
        county = puma_txt[puma_txt['summary_level'] == '796']
        county = county.rename(columns={'area_name': 'county'})
        # retrieve puma code and area name
        puma = puma_txt[puma_txt['summary_level'] == '795']
        puma = puma[['puma_code', 'area_name']]
        puma = puma.drop_duplicates()
        puma.columns = ['puma_code', 'puma_area']
        # left join county and puma by puma code
        crosswalk = county.merge(puma, how='left')
        # only keep columns of interests
        crosswalk = crosswalk[[
            'summary_level',
            'state_fips',
            'state',
            'puma_code',
            'county_fips',
            'county',
            'puma_area',
            'population',
            'year']]
        # create place(sssplace)
        crosswalk['place'] = crosswalk['county']
    # attach population of each puma to the crosswalk file
    crosswalk = crosswalk.merge(
        puma_pop, on='puma_code', suffixes=('', '_max'))
    # use the population of each row and
    #   population of puma to create a population weight
    crosswalk['weight'] = crosswalk[
        'population']/crosswalk['population_max']

    # TODO: if puma name & city file is better designed, code could be easier
    # if the file is State of Washington, replace some 'place' name
    #   to meaningful names e.g. "King(part)"-->"Seattle"
    if (('53' in set(crosswalk[
        'state_fips'])) or ('36' in set(crosswalk[
            'state_fips']))) and (nyc_wa_path is None):
        raise ValueError('Must pass the nyc_wa_path if processing NY or WA')
    if '53' in set(crosswalk['state_fips']):
        # read file and sheet_name 0 is the state of washington
        wa = pd.read_excel(
            nyc_wa_path, sheet_name=0)
        # the length of puma code should be 5. Some are not due to data type.
        # If it is not 5 digits, add "0" s to make it len()==5
        wa['PUMA'] = wa['PUMA'].astype('int').astype('str').str.zfill(5)
        wa = wa[[
            'PUMA',
            'Place',
            'Area_Name']]
        wa.columns = [
            'puma_code',
            'new_place',
            'part_county']
        # left join between crosswalk and wa
        crosswalk = crosswalk.merge(
            wa,
            left_on=['puma_code', 'county'],
            right_on=['puma_code', 'part_county'],
            how='left')
        # meaningful names are in the column 'new_place'.
        # If it is NA in 'new_place', filled by old 'place'
        crosswalk['new_place'] = crosswalk[
            'new_place'].fillna(crosswalk['place'])
        # drop 'place'
        crosswalk = crosswalk.drop(
            ['place', 'part_county'], axis=1)
        # rename new_place --> place
        crosswalk.rename(
            columns={'new_place': 'place'}, inplace=True)

    # if the file is NYC, replace some 'place' names to meaningful names
    if '36' in set(crosswalk['state_fips']):
        # read file and sheet_name 1 is NYC
        nyc = pd.read_excel(nyc_wa_path, sheet_name=1)
        # add "0" s to make it len()==5
        nyc['PUMA'] = nyc['PUMA'].astype('int').astype('str').str.zfill(5)
        nyc = nyc[['PUMA', 'AreaName']]
        nyc.columns = ['puma_code', 'new_place']
        crosswalk = crosswalk.merge(nyc, how='left')
        crosswalk['new_place'] = crosswalk[
            'new_place'].fillna(crosswalk['place'])
        crosswalk = crosswalk.drop('place', axis=1)
        # rename new_place --> place
        crosswalk.rename(columns={'new_place': 'place'}, inplace=True)
    return crosswalk


def puma_to_db(path, year, nyc_wa_path=None, testing=False):
    """
    This function is to put puma into database

    Need the PUMA .txt files found from
    https://www2.census.gov/geo/docs/reference/puma/.
    The year is 2021.
    Need the crosspath file "SSSplaces_NY&WA_PUMAcode.xlsx"

    Parameters
    ----------
    path : str
        path name of the PUMA .txt file or folder containing puma .txt files
        to read into the database
    year : int
        year of the puma data collected
    nyc_wa_path : str
        excel file path of nyc and washington replacement name list
    testing : bool
        If true, use the testing database rather than the default database

    """
    data_files = preprocess.data_path_to_file_list(path, extension_match="txt")
    db_file = get_db_file(testing=testing)
    db = AutomappedDB(db_file)
    session = db.sessionmaker()
    for file in data_files:
        df_puma = puma_crosswalk(file, year, nyc_wa_path)
        session.bulk_insert_mappings(
            PUMA, df_puma.to_dict(orient="records"))
        session.commit()
    session.close()
