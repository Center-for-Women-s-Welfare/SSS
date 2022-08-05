import glob
import os

import numpy as np
import pandas as pd
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean)

from . import preprocess 
from .base import Base, DB, DeclarativeDB

# declare CITY data columns and data type
class CITY(Base):
    __tablename__ = 'city'
    state = Column('state', String, ForeignKey("self_sufficiency_standard.state"),primary_key = True)
    place = Column('place', String, ForeignKey("self_sufficiency_standard.place"), primary_key = True)
    sss_city = Column('sss_city', String, primary_key = True)
    census_name = Column('census_name', String)
    population =  Column('population', Integer)
    public_transit = Column('public_transit', Boolean)


def add_city(path, year):
    
    """
    Reads city data into data frame and perprare for database table
    
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
    """
    df = pd.read_excel(path)
    df['state'] = df['SSS_City'].str.split(',').str[1]
    df['PublicTransit'] = df['PublicTransit'].astype('bool')
    df = df[['state','SSS_Place','SSS_City', 'Census_Name','POPESTIMATE2021' , 'PublicTransit']]
    df.columns = ['state','place','sss_city', 'census_name','population' , 'public_transit']
    df['year'] = year
    return df

df_add_city = add_city('2020_PopulationDatabyCity_20220804_Ama.xlsx', 2021)
session = DB.sessionmaker()
session.bulk_insert_mappings(SSS, df_add_city.to_dict(orient="records"))
session.commit()


