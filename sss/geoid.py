import os
import glob

import pandas as pd
from sqlalchemy import Column, String
from .base import Base, AutomappedDB, DeclarativeDB
from .base import default_db_file
#from sss import GEOID


# declare GeoID data columns and data type
class GeoID(Base):
    """
    This class defines the ``geo_identifier`` table.
    
    The data for this table comes from the Census.

    Attributes
    ----------
    state : String Column
        name of the state, e.g. WA
    place : String Column
        SSS place name
    state_fips : String Column
        fips code of state
    county_fips : String Column
        fips code of county
    place_fips : String Column
        fips code of place
    cpi_region : String Column
        name of cpi region

    """
    __tablename__ = 'geo_identifier'
    state = Column('state', String ,primary_key = True)
    place = Column('place', String , primary_key = True)
    #state = Column('state', String, ForeignKey("self_sufficiency_standard.state"),primary_key = True)
    #place = Column('place', String, ForeignKey("self_sufficiency_standard.place"), primary_key = True)
    state_fips = Column('state_fips',String)
    county_fips = Column('county_fips', String)
    place_fips =  Column('place_fips', String)
    cpi_region = Column('cpi_region', String)
    
def geo_identifier_creator(county_table, cpi_table):
    """
    The function to create geoidentifier

    Parameters
    ----------
    county_file : string
            The path of the county table including FIPS code
    cpi_file : string
            The path of the cpi_table including cpi region
    Returns
    -------
    df_combine : dataframe
            Return the merged table from county_table and cpi_table

    Raises
    ------
    ValueError
        If columns are not named properly in the input files

    """

    xl = pd.ExcelFile(county_table)
    # n_sheets = len(xl.sheet_names)
    df_l = pd.read_excel(county_table, sheet_name = 0, dtype=str)
    print("Read the first sheet of COUNTY table"+' '+ xl.sheet_names[0]+'. \
        Please adjust the sheet order if your tagret table is not the first one')
    df_l['state_fips'] = df_l['fips2010'].str[:2]
    df_l['county_fips'] = df_l['fips2010'].str[2:5]
    df_l['place_fips'] = df_l['fips2010'].str[5:]
    

    xl_r = pd.ExcelFile(cpi_table)
    # n_sheets_r = len(xl_r.sheet_names)
    df_r = pd.read_excel(cpi_table, sheet_name = 0)
    print("Read the first sheet of CPI table"+' '+ xl_r.sheet_names[0]+'.\
         Please adjust the sheet order if your tagret table is not the first one')

    try:
        df_combine = df_l.merge(df_r,left_on = 'state_alpha', right_on = 'USPS Abbreviation', how='left')
        df_combine = df_combine.rename(columns={"state_alpha": "state", "CPI Region": "cpi_region","SSS_Place":"place"})
        if df_combine.shape[0] != df_l.shape[0]:
            print('Merge sucessfully but new rows were created due to duplications in right(CPI) table')
    except:
        raise ValueError('Cannot merge, please check the two columns are named as "state_alpha" and "USPS Abbreviation"')

    if df_combine.duplicated(['state','place']).sum()>0:
        places = df_combine.loc[df_combine.duplicated(['state','place'],keep=False),'place'].values
        counties = df_combine.loc[df_combine.duplicated(['state','place'],keep=False),'countyname'].values
        value_com = places +' (' + counties +')'
        df_combine.loc[df_combine.duplicated(['state','place'],keep=False),'place'] = value_com
    return df_combine



def geoid_to_db(county_table, cpi_table, db_file=default_db_file):
    """
    Reads city data into data frame and insert it to database
    
    Parameters
    ----------
    county_file : str
            The path of the county table including FIPS code
    cpi_file : str
            The path of the cpi_table including cpi region
    db_file : str
            database file name, ends with '.sqlite'.

    """
    db = AutomappedDB(db_file)
    session = db.sessionmaker()
    df_geoid = geo_identifier_creator(county_table, cpi_table)
    session.bulk_insert_mappings(GeoID, df_geoid.to_dict(orient="records"))
    session.commit()
    session.close()

