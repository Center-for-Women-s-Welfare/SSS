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

# declare REPORT data columns and data type
class REPORT(Base):
    __tablename__ = 'report'
    year = Column('year', Integer, primary_key = True)
    state = Column('state', String, primary_key = True)
    analysis_type = Column('analysis_type', String, primary_key = True)
    cpi_month = Column('cpi_month', String)
    cpi_year =  Column('cpi_year', Integer)
    update_date = Column('update_date', Date)
    update_person = Column('update_person', String)

def add_report(path):
	"""
	Reads report data into data frame and perprare for database report table
	Parameters
    ----------
    path: str
        path name of report excel file
    Returns
    -------
    pandas.datafranme
        the returned dataframe has report record
	"""
	df = pd.read_excel(path)
	df.columns = df.columns.str.lower().str.replace(' ','_')
	# split 
	df['update_person'] = df['upload_status'].str.split(' ').str[0]
	df['update_date'] = df['upload_status'].str.split(' ').str[1]
		df["update_date"] = pd.to_datetime(df["update_date"])
	df.rename(columns={'type':'analysis_type'}, inplace=True)
	# Note: there are some columns has no names (e.g. unnamed: 1)
	df = df[['year', 'state', 'analysis_type', 'cpi_month','cpi_year','update_date','update_person']]
	return df 

df_add_report = add_report('Year_Type_SSS_CPI month year_20220715_DBu.xlsx')
session = DB.sessionmaker()
session.bulk_insert_mappings(SSS, df_add_report.to_dict(orient="records"))
session.commit()
