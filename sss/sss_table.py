"""
Creates a primary table for SSS data.

First, reads SSS data and conducts preprocessing. 
Then we create a primary table for SSS data.
"""

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
from .base import Base, AutomappedDB, DeclarativeDB
from .base import default_db_file

#TODO: Add docstrings to classes

# create class
class SSS(Base):
    __tablename__ = 'self_sufficiency_standard'
    family_type = Column('family_type', String, primary_key=True)
    state = Column('state', String, primary_key=True)
    place = Column('place', String, primary_key=True)
    year = Column('year', Integer, primary_key=True)
    analysis_type =  Column('analysis_type', String, primary_key=True)
    adult = Column('adult', Integer)
    infant = Column('infant', Integer)
    preschooler = Column('preschooler', Integer)
    schoolager = Column('schoolager', Integer)
    teenager = Column('teenager', Integer)
    weighted_child_count = Column('weighted_child_count', Integer)
    housing = Column('housing', Float)
    child_care = Column('child_care', Float)
    transportation = Column('transportation', Float)
    health_care = Column('health_care', Float)
    miscellaneous = Column('miscellaneous', Float)
    taxes = Column('taxes', Float)
    earned_income_tax_credit = Column('earned_income_tax_credit',
                                        Float)
    child_care_tax_credit = Column('child_care_tax_credit', Float)
    child_tax_credit = Column('child_tax_credit', Float)
    hourly_self_sufficiency_wage = Column(
        'hourly_self_sufficiency_wage', Float)
    monthly_self_sufficiency_wage = Column(
        'monthly_self_sufficiency_wage', Float)
    annual_self_sufficiency_wage = Column(
        'annual_self_sufficiency_wage', Float)
    emergency_savings = Column('emergency_savings', Float)
    
    miscellaneous_is_secondary = Column(
        'miscellaneous_is_secondary', Boolean)
    health_care_is_secondary = Column(
        'health_care_is_secondary', Boolean)

    analysis_is_secondary = Column(
        'analysis_is_secondary', Boolean)
    
# declare table columns and data type
class HealthCare(Base):
    __tablename__ = "health_care"
    family_type = Column("family_type", String, primary_key = True)
    state = Column("state", String, primary_key = True)
    place = Column("place", String, primary_key = True)
    year = Column("year", Integer, primary_key = True)
    analysis =  Column("analysis", String, primary_key = True)
    premium = Column("premium", Float)
    out_of_pocket = Column("out_of_pocket", Float)


# declare table columns and data type
class Miscellaneous(Base):
    __tablename__ = "miscellaneous"
    family_type = Column("family_type", String, primary_key = True)
    place = Column("place", String, primary_key = True)
    state = Column("state", String, primary_key = True)
    year = Column("year", String, primary_key = True)
    analysis =  Column("analysis", String, primary_key = True)
    broadband_and_cell_phone = Column("broadband_and_cell_phone", Float)
    other_necessities = Column("other_necessities", Float)

#TODO: Add docstring
class ARPA(Base):
    __tablename__ = 'arpa'
    family_type = Column('family_type', String, primary_key = True)
    state = Column('state', String, primary_key = True)
    place = Column('place', String, primary_key = True)
    year = Column('year', Integer, primary_key = True)
    analysis =  Column('analysis', String, primary_key = True)
    federal_oregon_eitc = Column('federal_state_eitc', Float)
    #federal_state_eitc = Column('federal_state_eitc', Float)
    federal_cdctc = Column('federal_cdctc', Float)
    federal_income_taxes = Column('federal_income_taxes', Float)
    payroll_taxes = Column('payroll_taxes', Float)
    state_sales_taxes = Column('state_sales_taxes', Float)
    total_annual_resources = Column('total_annual_resources', Float)

# map the excel file to the database
# session.bulk_insert_mappings(HealthCare,health_cost_clean_col.to_dict(orient="records"))



def read_file(file):
    """
    This function takes in a xls file and makes it into a pandas dataframe.
    
    As a dataframe, we read the sheet of interest (family_type).
    Then we standardize the column names

    Parameters
    ----------
    file: str
        file is the path of the file you want to add to the database


    Returns
    -------
    pandas.datafranme
        the returned dataframe has columns similar to that of the primary table
    files: str
        file name that was read into the dataframe

    """
    try:
        xl = pd.ExcelFile(file)

        # gets the number of spreadsheets
        n_sheets = len(xl.sheet_names)

        if n_sheets == 1:
            df = pd.read_excel(file, sheet_name=0)

        # if there are two sheets, we read the sheetname that is not the notes
        if n_sheets == 2:
            state_frame = [y for y in range(len(xl.sheet_names))
                           if 'note' not in xl.sheet_names[y].lower()]
            df = pd.read_excel(file, sheet_name=state_frame[0])

        if n_sheets > 2:
            family_frame = [sheet for sheet in xl.sheet_names
                            if 'Fam' in sheet]
            df = pd.read_excel(file, sheet_name=family_frame[0])
        
        # call the packages from preprocess
        df = preprocess.std_col_names(df)
    
    except:
        print('This file cannot be read' + ' ' + file.split('/')[-1])
    return df, file


def pre_check(df):
    print(df.dtypes)


def check_extra_columns(df):
    """
    This function takes in a pandas dataframe and adds a boolean column(s)

    Specifically, this function checks if broadband_&_cell_phone,
    and health_care are included the dataframe

    Parameters
    ----------
    df: pandas.dataframe
        this is the dataframe


    Returns
    -------
    pandas.datafranme
        the returned dataframe has additional columns
        these columns indicate whether there is a secondary table

    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df should be a pandas dataframe.")

    miscellaneous = pd.DataFrame()
    if ('other_necessities'or'broadband_and_cell_phone') in df.columns:
        df['miscellaneous_is_secondary'] = True
        miscellaneous = df[[ 'family_type','state','place','year','analysis_type']]
        if 'broadband_and_cell_phone' in df.columns:
            miscellaneous = pd.concat([miscellaneous, df['broadband_and_cell_phone']],axis=1)
        if 'other_necessities' in df.columns:
            miscellaneous = pd.concat([miscellaneous, df['other_necessities']],axis=1)
    else:
        df['miscellaneous_is_secondary'] = False

    health_care = pd.DataFrame()
    if ('health_care' or 'premium' or 'out_of_pocket') in df.columns:
        df['health_care_is_secondary'] = True
        health_care = df[[ 'family_type','state','place','year','analysis_type']]
        if 'out_of_pocket' in df.columns:
            health_care = pd.concat([health_care, df['out_of_pocket']],axis=1)
        if 'premium' in df.columns:
            health_care = pd.concat([health_care, df['premium']],axis=1)
    else:
        df['health_care_is_secondary'] = False
    
    """
    arpa, is analysis_type is not full or partial, 
    create analysis_is_secondary columns

    """
    # these are the columns found exclusively in the arpa file
    arpa_columns = ['federal_income_taxes', 'payroll_taxes', 'state_sales_taxes', 
                'state_income_taxes', 'federal_child_tax_credit', 
                'federal_and_oregon_eitc', 'federal_cdctc', 
                'oregon_wfhdc', 'total_annual_resources']
    arpa = pd.DataFrame()
    # we check whether these arpa columns are found in a file
    if  set(arpa_columns).issubset(list(df.columns)):
        # updates anaylisis_type if arpa columns found
        df['analysis_type'] = 'ARPA'
        arpa = df[[ 'family_type','state','place','year','analysis_type']] 
        arpa = pd.concat([arpa, df['analysis_type']],axis=1)
    if 'Full' or 'Partial' in df['analysis_type']:
        df['analysis_is_secondary'] = False
    else:
        df['analysis_is_secondary'] = True
        arpa = df[[ 'family_type','state','place','year','analysis_type']] 
        arpa = pd.concat([arpa, df['analysis_type']],axis=1)
        
    return df, miscellaneous, health_care, arpa


def data_folder_to_database(data_folder, db_file=default_db_file):
    """
    Reads path of folder of data, adds data to SQL table

    Here, we are using a file path to loop through a folder of the SSS data.
    We create the pandas.dataframe from the file being read.
    Then we call a previous function to add boolean columns.
    We then create the SQL table.
    The primary keys are family_type, state, place, year and anaylsis_type.
    The primary keys are all strings.
    The SQL table includes the columns adult, infant, preschooler, schoolager
    There are also teenager, weighted_child_count, housing, and childcare as integers
    Additional columns include housing, child_care, transportation, health_care, miscellaneous, taxes,  earned_income_tax_credit, child_care_tax_credit, child_tax_credit, hourly_self_sufficiency_wage, monthly_self_sufficiency_wage, annual_self_sufficiency_wage, and  emergency_savings as floats
    Fianlly, we have two boolean columns miscellaneous_is_secondary and health_care_is_secondary

    Parameters
    ----------
    data_folder: str
        path name of the folder or file that we want to read into the database

    Returns
    -------
    pandas.datafranme
        the returned dataframe has columns similar to that of the primary table 

    """
    if os.path.isfile(data_folder):
        data_files = [data_folder]
    elif os.path.isdir(data_folder):
        data_files = glob.glob(os.path.join(data_folder, "*.xls*"))
    else:
        raise ValueError("data_folder must be a file or a folder on this system")

    db = AutomappedDB(db_file)
    session = db.sessionmaker()

    for i in data_files:
        # read file and conduct pre-processing
        df, file = read_file(i)

        #clarify from cheng what will be defined as miscellaneous, and health_care

        df, miscellaneous, health_care, arpa = check_extra_columns(df)
        # need to have more precise solution for this specific problem
        # df['infant'] = pd.to_numeric(df['infant'],errors='coerce')
        # df['emergency_savings'] = pd.to_numeric(
        #                           df['emergency_savings'],errors='coerce')

        # Create a 'weighted_child_count' column from a*c* values
        #   this will take the infant count and move to this column
        df['weighted_child_count'] = df['infant']
        df.loc[df.loc[:, 'family_type'].isin(
            [i for i in df['family_type']
                if 'c' not in i]),
                'weighted_child_count'] = np.nan

        # removing duplicate rows, want to move this
        df = df.drop_duplicates(subset=['analysis_type', 'family_type',
                                        'state', 'year', 'place'])
        df.reset_index(inplace=True, drop=True)

        print(file.split('/')[-1])

        df_dic = df.to_dict(orient="records")
        #TODO: bulk insert with the other classes (miscellaneous, healthcare)
        session.bulk_insert_mappings(SSS, df_dic)
        session.commit()
    session.close()

# TODO: Handle different type of values
