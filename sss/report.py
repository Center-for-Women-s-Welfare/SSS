import glob
import os
from datetime import datetime, date

import numpy as np
import pandas as pd
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Date)

from . import preprocess 
from .base import Base,DB, DeclarativeDB
from .base import db_url as default_db_url
#from sss import REPORT

# declare REPORT data columns and data type
class REPORT(Base):
    '''
    Attributes
    ----------
    year: int
        year of report
    state: str
        name of state
    analysis_type: str
        analysis type of sss, e.g. full, partial
    cpi_month: str
        cpi month of the report
    cpi_year
        cpi year of the report
    update_date: date
        update date
    update_person: str
        who update the report
    '''
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
    # split column into meaningful column
    df['update_person'] = df['upload_status'].str.split(' ').str[0]
    df['update_date'] = df['upload_status'].str.split(' ').str[1]
    df["update_date"] = pd.to_datetime(df["update_date"])
    # convert to datetime that sql can recognize
    df['update_date'] = df['update_date'].map(lambda x: datetime.date(x))
    df['year'] = df['year'].astype(int)
    df['cpi_year'] = df['cpi_year'].astype(int)
    df.rename(columns={'type':'analysis_type'}, inplace=True)
    # Note: there are some columns has no names (e.g. unnamed: 1)
    df = df[['year', 'state', 'analysis_type', 'cpi_month','cpi_year','update_date','update_person']]
    return df 

def report_to_db(path, db_url= default_db_url):
    db = AutomappedDB(db_url)
    session = db.sessionmaker()
    df_report = add_report(path)
    print(df_report)
    session.bulk_insert_mappings(REPORT, df_report.to_dict(orient="records"))
    session.commit()
    session.close()



