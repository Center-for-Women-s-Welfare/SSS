"""Code to define and interact with tables for SSS data."""

from pathlib import Path

import numpy as np
import pandas as pd
from sqlalchemy import Boolean, Column, Float, Index, Integer, String, delete

from . import preprocess
from .base import AutomappedDB, Base


# create class
class SSS(Base):
    """
    Defines the ``self_sufficiency_standard`` table.

    Attributes
    ----------
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
    food : Float Column
        Cost of food.
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

    __tablename__ = "self_sufficiency_standard"
    family_type = Column("family_type", String, primary_key=True)
    state = Column("state", String, primary_key=True)
    place = Column("place", String, primary_key=True)
    year = Column("year", Integer, primary_key=True)
    analysis_type = Column("analysis_type", String, primary_key=True)
    adult = Column("adult", Integer)
    infant = Column("infant", Integer)
    preschooler = Column("preschooler", Integer)
    schoolager = Column("schoolager", Integer)
    teenager = Column("teenager", Integer)
    weighted_child_count = Column("weighted_child_count", Integer)
    housing = Column("housing", Float)
    child_care = Column("child_care", Float)
    food = Column("food", Float)
    transportation = Column("transportation", Float)
    health_care = Column("health_care", Float)
    miscellaneous = Column("miscellaneous", Float)
    taxes = Column("taxes", Float)
    earned_income_tax_credit = Column("earned_income_tax_credit", Float)
    child_care_tax_credit = Column("child_care_tax_credit", Float)
    child_tax_credit = Column("child_tax_credit", Float)
    hourly_self_sufficiency_wage = Column("hourly_self_sufficiency_wage", Float)
    monthly_self_sufficiency_wage = Column("monthly_self_sufficiency_wage", Float)
    annual_self_sufficiency_wage = Column("annual_self_sufficiency_wage", Float)
    emergency_savings = Column("emergency_savings", Float)
    miscellaneous_is_secondary = Column("miscellaneous_is_secondary", Boolean)
    health_care_is_secondary = Column("health_care_is_secondary", Boolean)
    analysis_is_secondary = Column("analysis_is_secondary", Boolean)

    Index("idx_state", "state")
    Index("idx_year", "year")


class ARPA(Base):
    """
    Define the ``arpa`` table.

    Attributes
    ----------
    state : String Column
        One of our primary keys, which what state this data is taken from.
    place : String Column
        One of our primary keys, the town or county.
    year : Integer Column
        One of our primary keys, the year the data is from.
    analysis_type : String Column
        One of our primary keys, whether the file is either a town or county.
    federal_state_eitc : Float Column
        Amount of the "refundable" tax credit based on loss of income.
    federal_cdctc : Float Column
        Amount of Child and Dependent Care Tax Credit.
    federal_income_taxes : Float Column
        Amount of federal income taxes paid.
    payroll_taxes : Float Column
        Amount of payroll taxes paid.
    state_sales_taxes : Float Column
        Amount of state sales taxes paid.
    total_annual_resources : Float Column
        An adjusted annual wage to reach self-sufficiency.

    """

    __tablename__ = "arpa"
    family_type = Column("family_type", String, primary_key=True)
    state = Column("state", String, primary_key=True)
    place = Column("place", String, primary_key=True)
    year = Column("year", Integer, primary_key=True)
    analysis_type = Column("analysis_type", String, primary_key=True)
    federal_and_oregon_eitc = Column("federal_and_oregon_eitc", Float)
    federal_cdctc = Column("federal_cdctc", Float)
    federal_income_taxes = Column("federal_income_taxes", Float)
    payroll_taxes = Column("payroll_taxes", Float)
    state_income_taxes = Column("state_income_taxes", Float)
    state_sales_taxes = Column("state_sales_taxes", Float)
    total_annual_resources = Column("total_annual_resources", Float)


# declare table columns and data type
class HealthCare(Base):
    """
    Define the ``health_care`` table.

    Attributes
    ----------
    state : String Column
        One of our primary keys, which what state this data is taken from.
    place : String Column
        One of our primary keys, which either the town or county.
    year : Integer Column
        One of our primary keys, the year the data is from.
    analysis_type : String Column
        One of our primary keys, whether the file is either a town or county.
    premium : Float Column
        Price that job covers heatlh_care
    out_of_pocket : Float Column
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
    Define the ``miscellaneous`` table.

    Attributes
    ----------
    state : String Column
        One of our primary keys, which what state this data is taken from.
    place : String Column
        One of our primary keys, which either the town or county.
    year : Integer Column
        One of our primary keys, the year the data is from.
    analysis_type : String Column
        One of our primary keys, whether the file is either a town or county.
    broadband_and_cell_phone : Float Column
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


def read_file(file: str):
    """
    Read SSS data file into a Pandas dataframe.

    Read the sheet of interest (family_type) and standardize the column names.

    Parameters
    ----------
    file : str
        file is the path of the file you want to add to the database

    Returns
    -------
    df : pandas.datafranme
        the returned dataframe has columns similar to that of the primary table
    file : str
        file name that was read into the dataframe

    """
    try:
        with pd.ExcelFile(file) as xl:
            # gets the number of spreadsheets
            n_sheets = len(xl.sheet_names)

            if n_sheets == 1:
                df = pd.read_excel(file, sheet_name=0)

            # if there are two sheets, we read the sheetname that is not the notes
            if n_sheets == 2:
                state_frame = [
                    y
                    for y in range(len(xl.sheet_names))
                    if "note" not in xl.sheet_names[y].lower()
                ]
                df = pd.read_excel(file, sheet_name=state_frame[0])

            if n_sheets > 2:
                family_frame = [sheet for sheet in xl.sheet_names if "Fam" in sheet]
                df = pd.read_excel(file, sheet_name=family_frame[0])

        # call the packages from preprocess
        df = preprocess.std_col_names(df)

    except Exception:
        print("This file cannot be read:" + " " + Path(file).parts[-1])
        df = None
    return df, file


def check_extra_columns(df: pd.DataFrame):
    """
    Add three boolean columns to dataframe to indicate special cost breakdowns.

    Specifically, this function checks if the sss dataframe contains
    additional cost breakdown for arpa, health care, and
    miscellaneous costs. If these additional breakdowns are
    present in the dataframe, we fill each of the breakdown
    dataframe. If these breakdowns are not present, the
    new dataframes will be empty. We then update the boolean column to
    represent whether these breakdowns occur in other helper tables.

    Parameters
    ----------
    df : pandas.dataframe
        this is the dataframe


    Returns
    -------
    df : pandas.datafranme
        the returned dataframe has additional columns
        these columns indicate whether there are any secondary tables
    arpa : pandas.dataframe
       this dataframe contains the additional breakdown of arpa
    health_care : pandas.dataframe
        this dataframe contains the additional breakdown of health care
    miscellaneous : pandas.dataframe
        this dataframe contains the additional breakdown of miscellaneous

    """
    if not isinstance(df, pd.DataFrame):
        raise ValueError("df should be a pandas dataframe.")

    # these are the columns found exclusively in the arpa file
    arpa_columns = [
        "federal_income_taxes",
        "payroll_taxes",
        "state_sales_taxes",
        "state_income_taxes",
        "federal_child_tax_credit",
        "federal_and_oregon_eitc",
        "federal_cdctc",
        "oregon_wfhdc",
        "total_annual_resources",
    ]

    # columns for health_care secondary table
    health_care_columns = ["premium", "out_of_pocket"]

    # columns for miscellaneous secondary table
    miscellaneous_columns = ["other_necessities", "broadband_and_cell_phone"]

    secondary_tables = {
        "arpa": {
            "df": pd.DataFrame(),
            "cols": arpa_columns,
            "main_col": "analysis_is_secondary",
        },
        "health_care": {
            "df": pd.DataFrame(),
            "cols": health_care_columns,
            "main_col": "health_care_is_secondary",
        },
        "miscellaneous": {
            "df": pd.DataFrame(),
            "cols": miscellaneous_columns,
            "main_col": "miscellaneous_is_secondary",
        },
    }

    for table, tbl_dict in secondary_tables.items():
        if set(tbl_dict["cols"]).issubset(list(df.columns)):
            # update the table if cols are found
            if table == "arpa":
                df["analysis_type"] = "ARPA"
            tbl_dict["df"] = df[
                ["family_type", "state", "place", "year", "analysis_type"]
            ]
            for col in tbl_dict["cols"]:
                tbl_dict["df"] = pd.concat([tbl_dict["df"], df[col]], axis=1)
                df = df.drop(columns=col)
            df[tbl_dict["main_col"]] = True
        else:
            df[tbl_dict["main_col"]] = False

    return (
        df,
        secondary_tables["arpa"]["df"],
        secondary_tables["health_care"]["df"],
        secondary_tables["miscellaneous"]["df"],
    )


def prepare_for_database(df):
    """
    Prepare pandas dataframe for database.

    Specifically, this function takes in the dataframe containing
    data for the primary table. The dataframe is prepared by
    updating certain columns, adding a new weighted children column,
    and by dropping all duplicates. This functions is meant
    to update the dataframe so there are no issues transferring
    data into the database.

    Parameters
    ----------
    df : pandas.dataframe
        this is the sss dataframe

    Returns
    -------
    df : pandas.datafranme
        the returned dataframe does not contain duplicates

    """
    # handling some issues with certain columns
    #   (i.e., NJ 2019 has column values of "#NA")
    df["infant"] = pd.to_numeric(df["infant"], errors="coerce")
    if "emergency_savings" in df.columns:
        df["emergency_savings"] = pd.to_numeric(
            df["emergency_savings"], errors="coerce"
        )

    # Create a 'weighted_child_count' column from a*c* values initialized to zeros
    df["weighted_child_count"] = 0

    # first set the weighted_child_count to NaN for family types without "c"s
    df.loc[
        df.loc[:, "family_type"].isin([i for i in df["family_type"] if "c" not in i]),
        "weighted_child_count",
    ] = np.nan

    # for the rows with "c" in the family type, extract the value after the c
    # and assign it to the weighted_child_count column
    c_rows = df.loc[:, "family_type"].isin([i for i in df["family_type"] if "c" in i])
    if np.sum(c_rows) > 0:
        # pandas split with the "expand" option returns a dataframe with number
        # of splits + 1 columns. We're asking for one split, so we get two columns
        # the second one has the data we want.
        child_count_df = df.loc[c_rows, "family_type"].str.split(
            pat="c", n=1, expand=True
        )
        df.loc[c_rows, "weighted_child_count"] = child_count_df[1].astype(int)

        # then set the other kid age columns to 0 for family types *with* "c"s
        df.loc[c_rows, ["infant", "preschooler", "schoolager", "teenager"]] = 0

    # removing duplicate rows
    df = df.drop_duplicates()

    # Check for rows with duplicate primary keys and error if any present.
    # These will error when entered into the database anyway and the code doesn't
    # know which one to keep, user should fix this in the data.
    primary_keys = ["analysis_type", "family_type", "state", "year", "place"]
    primary_key_duplicates = df[df.duplicated(subset=primary_keys)]
    if len(primary_key_duplicates) > 0:
        raise ValueError(
            "Some rows have identical primary keys with different data:\n"
            f"{primary_key_duplicates[primary_keys]}"
        )

    df.reset_index(inplace=True, drop=True)
    return df


def data_folder_to_database(data_path, testing=False):
    """
    Read path of the data, add data to SQL table.

    Here, we are using a path that holds the data to loop through the SSS data.
    SSS data is found here: https://selfsufficiencystandard.org/state-data/.
    We create the pandas.dataframe from the file being read.
    Then we call a previous function to add boolean columns.
    We then create the SQL table.

    Parameters
    ----------
    data_folder : str
        path name of the folder or file that we want to read into the database
    testing : bool
        If true, use the testing database rather than the default database

    """
    data_files = preprocess.data_path_to_file_list(data_path, extension_match="xls*")

    db = AutomappedDB(testing=testing)
    with db.sessionmaker() as session:
        for fi in data_files:
            # read file and conduct pre-processing
            df, file = read_file(fi)

            # store dataframes created
            df, arpa, health_care, miscellaneous = check_extra_columns(df)

            # update the primary table df
            df = prepare_for_database(df)

            # prints what file we are reading
            print("Processing:", Path(file).parts[-1])

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
            print(Path(file).parts[-1], "has been entered into the database")

            session.commit()


def remove_state_year(state, year, testing=False):
    """
    Remove rows for a specific state and year.

    Parameters
    ----------
    state : str
        The state to remove from live database.
    year : int
        The year to remove from live database.
    testing : bool
        If true, use the testing database rather than the default database

    """
    if not isinstance(state, str):
        raise ValueError("State must be a string")
    if not isinstance(year, int):
        raise ValueError("Year must be a integer")

    db = AutomappedDB(testing=testing)
    statement_sss = delete(SSS).where(SSS.year == year, SSS.state == state)
    statement_arpa = delete(ARPA).where(ARPA.year == year, ARPA.state == state)
    statement_misc = delete(Miscellaneous).where(
        Miscellaneous.year == year, Miscellaneous.state == state
    )
    statement_hc = delete(HealthCare).where(
        HealthCare.year == year, HealthCare.state == state
    )
    with db.sessionmaker() as session:
        for statement in [statement_sss, statement_arpa, statement_misc, statement_hc]:
            session.execute(statement)
        session.commit()


def update_columns(data_path, columns=None, testing=False):
    """
    Update the specified columns using data in the data_path.

    Read in the data from the data_path and update only the specified columns.
    Assumes that the rows for this data already exist in the database.

    Parameters
    ----------
    data_path : str
        path name of the folder or file that we want to read into the database
    columns : list of str
        List of column names to update
    testing : bool
        If true, use the testing database rather than the default database

    """
    data_files = preprocess.data_path_to_file_list(data_path, extension_match="xls*")

    if len(data_files) == 0:
        raise ValueError(f"No data files identified in {data_path}")

    pk_cols = ["family_type", "state", "place", "year", "analysis_type"]

    if isinstance(columns, str):
        columns = [columns]

    for col in columns:
        if col in pk_cols:
            raise ValueError("Cannot update a primary key column.")

    db = AutomappedDB(testing=testing)
    with db.sessionmaker() as session:
        for file in data_files:
            print("Processing:", Path(file).parts[-1])

            df, _ = read_file(file)
            df, arpa, health_care, miscellaneous = check_extra_columns(df)
            df = prepare_for_database(df)

            main_columns = []
            arpa_cols = []
            health_care_cols = []
            miscellaneous_cols = []
            for col in columns:
                if col in df.columns:
                    main_columns.append(col)
                elif not arpa.empty and col in arpa.columns:
                    arpa_cols.append(col)
                elif not health_care.empty and col in health_care.columns:
                    health_care_cols.append(col)
                elif not miscellaneous.empty and col in miscellaneous.columns:
                    miscellaneous_cols.append(col)

            if len(main_columns) > 0:
                cols_to_keep = pk_cols + main_columns
                cols_to_drop = [col for col in df.columns if col not in cols_to_keep]
                df.drop(columns=cols_to_drop, inplace=True)

                session.bulk_update_mappings(SSS, df.to_dict("records"))
                session.commit()

            if len(arpa_cols) > 0:
                cols_to_keep = pk_cols + arpa_cols
                cols_to_drop = [col for col in arpa.columns if col not in cols_to_keep]
                arpa.drop(columns=cols_to_drop, inplace=True)

                session.bulk_update_mappings(ARPA, arpa.to_dict("records"))
                session.commit()

            if len(health_care_cols) > 0:
                cols_to_keep = pk_cols + health_care_cols
                cols_to_drop = [
                    col for col in health_care.columns if col not in cols_to_keep
                ]
                health_care.drop(columns=cols_to_drop, inplace=True)

                session.bulk_update_mappings(HealthCare, health_care.to_dict("records"))
                session.commit()

            if len(miscellaneous_cols) > 0:
                cols_to_keep = pk_cols + miscellaneous_cols
                cols_to_drop = [
                    col for col in miscellaneous.columns if col not in cols_to_keep
                ]
                miscellaneous.drop(columns=cols_to_drop, inplace=True)

                session.bulk_update_mappings(
                    Miscellaneous, miscellaneous.to_dict("records")
                )
                session.commit()
