import glob
import os

import numpy as np
import pandas as pd
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey)

from . import preprocess 
from .base import Base, AutomappedDB, DeclarativeDB
from .base import db_url as default_db_url
#from sss import CITY

# declare CITY data columns and data type
class City(Base):
    """
    Declare the attributes for city table

    Attributes
    ----------
    state: String Column
        name of the state, e.g. WA
    place: String Column
        SSS place name
    city: String Column
        sss_city, some cities of sss place
    census_name: String Column
        the census name of the city
    population: Integer Column
        number of the population of the city
    public_transit: Boolean Column
        whether the city is public transit or not

    """
    __tablename__ = 'city'
    #state = Column('state', String, ForeignKey("self_sufficiency_standard.state"),primary_key = True)
    #place = Column('place', String, ForeignKey("self_sufficiency_standard.place"), primary_key = True)
    state = Column('state', String, primary_key = True)
    place = Column('place', String, primary_key = True)
    sss_city = Column('sss_city', String, primary_key = True)
    census_name = Column('census_name', String)
    population =  Column('population', Integer)
    public_transit = Column('public_transit', Boolean)


def add_city(path, year):
    """
    Reads city data into data frame and prepare for database table
    
    Parameters
    ----------
    path: str
        path name of city excel file
    year: int
        year of the population data collected
    
    Returns
    -------
    pandas.datafranme
        the returned dataframe has population size by city
    
    Raises
    -----
        ValueError
        if the state cannot be extracted from SSS_city
    """
    df = pd.read_excel(path)
    df['state'] = df['SSS_City'].str.split(',').str[1]
    df['state'] = df['state'].str.replace('*','')
    if df.state.isna().sum()>0:
        raise ValueError('could not find state in SSS_City value %s' % (df[df.state.isna()]['SSS_City']))
    df['PublicTransit'] = df['PublicTransit'].astype('bool')
    df = df[['state','SSS_Place','SSS_City', 'Census_Name','POPESTIMATE2021' , 'PublicTransit']]
    df.columns = ['state','place','sss_city', 'census_name','population' , 'public_transit']
    df['year'] = year
    return df


def city_to_db(data_path, year, db_url=default_db_url):
    """
    Reads city data into data frame and insert it to database
    
    Parameters
    ----------
    path: str
        path name of city excel file
    year: int
        year of the population data collected
    """
    db = AutomappedDB(db_url)
    session = db.sessionmaker()
    df_city = add_city(data_path, year)
    session.bulk_insert_mappings(CITY, df_city.to_dict(orient="records"))
    session.commit()
    session.close()


