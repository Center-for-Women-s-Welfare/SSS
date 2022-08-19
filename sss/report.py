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

from sss import db_check

from . import preprocess 
from .base import Base, AutomappedDB
from .base import default_db_file
#from sss import REPORT

# declare Report data columns and data type
class Report(Base):
    """
    declare columns in Report table in the database
    
    Attributes
    ----------
    year: Integer Column
        year of report
    state: String Column
        name of state
    analysis_type: String Column
        analysis type of sss, e.g. full, partial
    cpi_month: String Column
        cpi month of the report
    cpi_year: Integer Column
        cpi year of the report
    update_date: Date Column
        update date
    update_person: String Column
        who update the report
    """
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

def report_to_db(path, db_file=default_db_file):
    """
    Insert report file to the report table in the db
    
    Parameters
    ----------
    path: str
        path name of report excel file
    """
    db = AutomappedDB(db_file)
    session = db.sessionmaker()
    df_report = add_report(path)
    session.bulk_insert_mappings(Report, df_report.to_dict(orient="records"))
    session.commit()
    session.close()

def add_one_entry_reportdb(year, 
                           state,
                           analysis_type,
                           cpi_month,
                           cpi_year,
                           update_date,
                           update_person,
                           db_url=default_db_url):
    """
    This function inserts one record into report table
    
    Parameters
    ----------
    year: Integer
        year of report
    state: String
        name of state
    analysis_type: String
        analysis type of sss, e.g. full, partial
    cpi_month: String
        cpi month of the report, like May
    cpi_year: int
        cpi year of the report
    update_date: Date
        update date, the format is date(2021,6,22)
    update_person: String Column
        who update the report
    """
    db = AutomappedDB(db_url)
    session = db.sessionmaker()
    new_record = Report(year = int(year),
                        state=  str(state),
                        analysis_type = str(analysis_type),
                        cpi_month = str(cpi_month),
                        cpi_year = int(cpi_year),
                        update_date = update_date,
                        update_person = str(update_person))
    #add to db
    session.add(new_record)
    session.commit()
    session.close()


def delete_one_entry_reportdb(year,
                              state,
                              analysis_type,
                              db_url=default_db_url):
    """
    This function delete one record. In case some records were insert accidentally. 
    
    Parameters
    ----------
    year: Integer
        year of report
    state: String
        name of state
    analysis_type: String
        analysis type of sss, e.g. full, partial
    """
    db = AutomappedDB(db_url)
    session = db.sessionmaker()
    #delete the records that meets criteria
    session.query(Report).filter(Report.year == year, 
                                 Report.state == state, 
                                 Report.analysis_type == analysis_type).delete()
    session.commit()
    session.close()
    
