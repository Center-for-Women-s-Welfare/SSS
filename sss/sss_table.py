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
from .base import Base, AutomappedDB
from .base import default_db_file


# create class
class SSS(Base):
    """

    Attributes
    ----------
    __tablename__  : String Column
        Name of our table in the database.
    family_type : String Column
        One of our primary keys, the family type as seen in the standard SSS.
    state : String Column
        One of our primary keys, which what state this data is taken from.
    place : String Column
        One of our primary keys, either the town or county.
    year : String Column
        One of our primary keys, the year the data is from.
    analysis_type : String Column
        One of our primary keys, whether the file is either a town or county.
    adult : Integer Column
        Number of adults in the household.
    infant : Integer Column
        Number of infants in the household.
    preschooler : Integer Column
        Number of preschoolers in the household.
    schoolager : Integer Column
        Number of schoolagers in the household.
    teenager : Integer Column
        Number of teenagers in the househould.
    weighted_child_count : Integer Column
        Number of total children in the household.
        A value is only present when the family type is a*c*.
    housing : Float Column
        Cost of housing.
    child_care : Float Column
        Cost of child care.
    transportation : Float Column
        Cost of transportation.
    health_care : Float Column
        Cost of health care.
    miscellaneous : Float Column
        Cost of miscellaneous costs.
    taxes : Float Column
        Cost of taxes paid.
    earned_income_tax_credit : Float Column
        Amount of tax credit earned through work.
    child_care_tax_credit : Float Column
        Amount of tax credit earned through child care cost.
    child_tax_credit : Float Column
        Amount of tax credit earned through number of children.
    hourly_self_sufficiency_wage : Float Column
        The hourly wage needed to reach self-sufficiency.
    monthly_self_sufficiency_wage : Float Column
        The monthly wage needed to reach self-sufficiency.
    annual_self_sufficiency_wage : Float Column
        The annual wage needed reach self-sufficiency.
    emergency_savings : Float Column
        The amount needed to cover random expenses.
    miscellaneous_is_secondary : Boolean Column
        Value represents whether there is a table breakdown of miscellaneous.
    health_care_is_secondary : Boolean Column
        Value represents whether there is a table breakdown of health care.
    analysis_is_secondary : Boolean Column
       Value represents whether there is a table breakdown of ARPA.
    """
    __tablename__ = 'self_sufficiency_standard'
    family_type = Column('family_type', String, primary_key=True)
    state = Column('state', String, primary_key=True)
    place = Column('place', String, primary_key=True)
    year = Column('year', Integer, primary_key=True)
    analysis_type = Column('analysis_type', String, primary_key=True)
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
    earned_income_tax_credit = Column('earned_income_tax_credit', Float)
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


class ARPA(Base):
    """
    Attributes
    ----------
    state : str column
        One of our primary keys, which what state this data is taken from.
    place : str
        One of our primary keys, the town or county.
    year : int column
        One of our primary keys, the year the data is from.
    analysis_type : str column
        One of our primary keys, whether the file is either a town or county.
    federal_state_eitc : float column
        Amount of the "refundable" tax credit based on loss of income.
    federal_cdctc : float column
        Amount of Child and Dependent Care Tax Credit.
    federal_income_taxes : float column
        Amount of federal income taxes paid.
    payroll_taxes : float column
        Amount of payroll taxes paid.
    state_sales_taxes : float column
        Amount of state sales taxes paid.
    total_annual_resources : float column
        An adjusted annual wage to reach self-sufficiency.
    """
    __tablename__ = 'arpa'
    family_type = Column('family_type', String, primary_key=True)
    state = Column('state', String, primary_key=True)
    place = Column('place', String, primary_key=True)
    year = Column('year', Integer, primary_key=True)
    analysis_type = Column('analysis_type', String, primary_key=True)
    federal_and_oregon_eitc = Column('federal_and_oregon_eitc', Float)
    federal_cdctc = Column('federal_cdctc', Float)
    federal_income_taxes = Column('federal_income_taxes', Float)
    payroll_taxes = Column('payroll_taxes', Float)
    state_income_taxes = Column('state_income_taxes', Float)
    state_sales_taxes = Column('state_sales_taxes', Float)
    total_annual_resources = Column('total_annual_resources', Float)


# declare table columns and data type
class HealthCare(Base):
    """
    Attributes
    ----------
    state : str column
        One of our primary keys, which what state this data is taken from.
    place : str column
        One of our primary keys, which either the town or county.
    year : int column
        One of our primary keys, the year the data is from.
    analysis_type : str column
        One of our primary keys, whether the file is either a town or county.
    premium : float column
        Price that job covers heatlh_care
    out_of_pocket : float column
        Price that family pays for health care
    """
    __tablename__ = "health_care"
    family_type = Column("family_type", String, primary_key=True)
    state = Column("state", String, primary_key=True)
    place = Column("place", String, primary_key=True)
    year = Column("year", Integer, primary_key=True)
    analysis_type = Column("analysis_type", String, primary_key=True)
    premium = Column("premium", Float)
    out_of_pocket = Column("out_of_pocket", Float)


# declare table columns and data type
class Miscellaneous(Base):
    """
    Attributes
    ----------
    state : str column
        One of our primary keys, which what state this data is taken from.
    place : str
        One of our primary keys, which either the town or county.
    year : int column
        One of our primary keys, the year the data is from.
    analysis_type : str column
        One of our primary keys, whether the file is either a town or county.
    broadband_and_cell_phone : float column
        Cost families spend on broadband and cell phone per month.
    """
    __tablename__ = "miscellaneous"
    family_type = Column("family_type", String, primary_key=True)
    place = Column("place", String, primary_key=True)
    state = Column("state", String, primary_key=True)
    year = Column("year", String, primary_key=True)
    analysis_type = Column("analysis_type", String, primary_key=True)
    broadband_and_cell_phone = Column("broadband_and_cell_phone", Float)
    other_necessities = Column("other_necessities", Float)


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

    except Exception:
        print('This file cannot be read' + ' ' + file.split('/')[-1])
    return df, file


def check_extra_columns(df):
    """
    Adds three boolean columns to dataframe to indicate other cost breakdowns

    Specifically, this function checks if the sss dataframe contains
    additional cost breakdown for arpa, health care, and
    broadband_&_cell_phone. If these additional breakdowns are
    present in the dataframe, we fill each of the breakdown
    dataframe. If these breakdowns are not present, the
    new dataframes will be empty. We then update the boolean column to
    represent whether these breakdowns occur in other helper tables.

    Parameters
    ----------
    df: pandas.dataframe
        this is the dataframe


    Returns
    -------
    df: pandas.datafranme
        the returned dataframe has additional columns
        these columns indicate whether there are any secondary tables

    arpa: pandas.dataframe
       this dataframe contains the additional breakdown of arpa

    health_care: pandas.dataframe
        this dataframe contains the additional breakdown of health care

    miscellaneous: pandas.dataframe
        this dataframe contains the additional breakdown of miscellaneous

    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df should be a pandas dataframe.")

    # these are the columns found exclusively in the arpa file
    arpa_columns = ['federal_income_taxes', 'payroll_taxes',
                    'state_sales_taxes', 'state_income_taxes',
                    'federal_child_tax_credit',
                    'federal_and_oregon_eitc', 'federal_cdctc',
                    'oregon_wfhdc', 'total_annual_resources']
    arpa = pd.DataFrame()
    # we check whether these arpa columns are found in a file
    if set(arpa_columns).issubset(list(df.columns)):
        # updates anaylisis_type if arpa columns found
        df['analysis_type'] = 'ARPA'
        arpa = df[['family_type', 'state', 'place', 'year', 'analysis_type']]
        for i in arpa_columns:
            arpa = pd.concat([arpa, df[i]], axis=1)
        df['analysis_is_secondary'] = True
    else:
        df['analysis_is_secondary'] = False

    health_care = pd.DataFrame()
    if ('premium' or 'out_of_pocket') in df.columns:
        df['health_care_is_secondary'] = True
        health_care = df[['family_type', 'state', 'place', 'year',
                          'analysis_type']]
        if 'out_of_pocket' in df.columns:
            health_care = pd.concat([health_care, df['out_of_pocket']], axis=1)
        if 'premium' in df.columns:
            health_care = pd.concat([health_care, df['premium']], axis=1)
    else:
        df['health_care_is_secondary'] = False
    miscellaneous = pd.DataFrame()
    if ('other_necessities' or 'broadband_and_cell_phone') in df.columns:
        df['miscellaneous_is_secondary'] = True
        miscellaneous = df[['family_type', 'state', 'place', 'year',
                            'analysis_type']]
        if 'broadband_and_cell_phone' in df.columns:
            miscellaneous = pd.concat([miscellaneous,
                                      df['broadband_and_cell_phone']], axis=1)
        if 'other_necessities' in df.columns:
            miscellaneous = pd.concat([miscellaneous, df['other_necessities']],
                                      axis=1)
    else:
        df['miscellaneous_is_secondary'] = False

    return df, arpa, health_care, miscellaneous


def prepare_for_database(df):
    """
    This function takes in a pandas df and prepares it for database

    Specifically, this function takes in the dataframe containing
    data for the primary table. The dataframe is prepared by
    updating certain columns, adding a new weighted children column,
    and by dropping all duplicates. This functions is meant
    to update the dataframe so there are no issues transferring
    data into the database.


    Parameters
    ----------
    df: pandas.dataframe
        this is the sss dataframe


    Returns
    -------
    pandas.datafranme
        the returned dataframe does not contain duplicates

    """
    # handling some issues with certain columns
    #   (i.e., NJ 2019 has column values of "#NA")
    df['infant'] = pd.to_numeric(df['infant'], errors='coerce')
    df['emergency_savings'] = pd.to_numeric(
                                df['emergency_savings'], errors='coerce')

    # Create a 'weighted_child_count' column from a*c* values
    #   this will take the infant count and move to this column
    df['weighted_child_count'] = df['infant']
    df.loc[df.loc[:, 'family_type'].isin(
        [i for i in df['family_type']
            if 'c' not in i]),
            'weighted_child_count'] = np.nan
    df.loc[df.loc[:, 'family_type'].isin(
        [i for i in df['family_type']
            if 'c' not in i]),
            'infant'] = 0

    # removing duplicate rows
    df = df.drop_duplicates(subset=['analysis_type', 'family_type',
                                    'state', 'year', 'place'])
    df.reset_index(inplace=True, drop=True)
    return df

def data_folder_to_database(data_path, db_file=default_db_file):
    """
    Reads path of the data, adds data to SQL table

    Here, we are using a path that holds the data to loop through the SSS data.
    We create the pandas.dataframe from the file being read.
    Then we call a previous function to add boolean columns.
    We then create the SQL table.


    Parameters
    ----------
    data_folder: str
        path name of the folder or file that we want to read into the database

    db_file : str
        database file name, ends with '.sqlite'.

    Returns
    -------
    pandas.datafranme
        the returned dataframe has columns similar to that of the primary table

    """
    if os.path.isfile(data_path):
        data_files = [data_path]
    elif os.path.isdir(data_path):
        data_files = glob.glob(os.path.join(data_path, "*.xls*"))
    else:
        raise ValueError("data_folder must be a file or folder on this system")

    db = AutomappedDB(db_file)
    session = db.sessionmaker()

    for i in data_files:
        # read file and conduct pre-processing
        df, file = read_file(i)

        # store dataframes created
        df, arpa, health_care,  miscellaneous = check_extra_columns(df)

        # update the primary table df
        df = prepare_for_database(df)

        # prints what file we are reading
        print("We are processing:", file.split('/')[-1])

        # we are taking the primary table df and making it into a dictionary
        df_dic = df.to_dict(orient="records")

        # we insert dataframe
        session.bulk_insert_mappings(SSS, df_dic)

        if not arpa.empty:
            arpa_dict = arpa.to_dict(orient="records")
            session.bulk_insert_mappings(ARPA, arpa_dict)
        if not health_care.empty:
            health_dict = health_care.to_dict(orient="records")
            session.bulk_insert_mappings(HealthCare, health_dict)
        if not miscellaneous.empty:
            miscellaneous_dict = miscellaneous.to_dict(orient="records")
            session.bulk_insert_mappings(Miscellaneous, miscellaneous_dict)

        # prints out the name of the file that has been entered to db
        print(file.split('/')[-1], "has been entered into the database")

        session.commit()
    session.close()
