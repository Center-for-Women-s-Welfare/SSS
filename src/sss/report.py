"""Create the report table and functions to interact with table."""

from datetime import datetime

import pandas as pd
from sqlalchemy import Column, Date, Integer, String

from .base import AutomappedDB, Base


# declare Report data columns and data type
class Report(Base):
    """
    Define the ``report`` table.

    Attributes
    ----------
    year : Integer Column
        year of report
    state : String Column
        name of state
    analysis_type : String Column
        analysis type of sss, e.g. full, partial
    cpi_month : String Column
        cpi month of the report
    cpi_year : Integer Column
        cpi year of the report
    update_date : Date Column
        update date
    update_person : String Column
        person who updated the report

    """

    __tablename__ = "report"
    year = Column("year", Integer, primary_key=True)
    state = Column("state", String, primary_key=True)
    analysis_type = Column("analysis_type", String, primary_key=True)
    cpi_month = Column("cpi_month", String)
    cpi_year = Column("cpi_year", Integer)
    update_date = Column("update_date", Date)
    update_person = Column("update_person", String)


def add_report(path):
    """
    Read report data into data frame and perprare for database report table.

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
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # make nans and other null types be None
    df["upload_status"] = df["upload_status"].where(
        pd.notnull(df["upload_status"]), None
    )

    # split column into meaningful column
    df["update_person"] = df["upload_status"].str.split(" ").str[0]
    df["update_date"] = df["upload_status"].str.split(" ").str[1]
    # this code handles whether there are different date formats in the
    # "update_date" column
    for i in range(len(df)):
        try:
            df.loc[i, "update_date"] = pd.to_datetime(
                df.loc[i, "update_date"], format="%m/%d/%y"
            )
        except ValueError:
            df.loc[i, "update_date"] = datetime.strptime(
                df.loc[i, "update_date"], "%m/%d/%Y"
            ).strftime("%m/%d/%y")
            df.loc[i, "update_date"] = pd.to_datetime(
                df.loc[i, "update_date"], format="%m/%d/%y"
            )
    # convert to datetime that sql can recognize
    df["update_date"] = df["update_date"].map(
        lambda x: datetime.date(x), na_action="ignore"
    )
    df["year"] = df["year"].astype(int)
    df["cpi_year"] = df["cpi_year"].astype(int)
    df.rename(columns={"type": "analysis_type"}, inplace=True)
    # Note: there are some columns has no names (e.g. unnamed: 1)
    df = df[
        [
            "year",
            "state",
            "analysis_type",
            "cpi_month",
            "cpi_year",
            "update_date",
            "update_person",
        ]
    ]
    return df


def report_to_db(path, testing=False):
    """
    Insert report file to the report table.

    The report file is named
    "Year_Type_SSS_CPI month year_20220715_DBu.xlsx"

    Parameters
    ----------
    path: str
        path name of report excel file
    testing : bool
        If true, use the testing database rather than the default database

    """
    db = AutomappedDB(testing=testing)
    df_report = add_report(path)
    with db.sessionmaker() as session:
        session.bulk_insert_mappings(Report, df_report.to_dict(orient="records"))
        session.commit()


def add_one_entry_reportdb(
    year,
    state,
    analysis_type,
    cpi_month,
    cpi_year,
    update_date,
    update_person,
    testing=False,
):
    """
    Insert one record into report table.

    Parameters
    ----------
    year : int
        year of report
    state : str
        name of state
    analysis_type : str
        analysis type of sss, e.g. full, partial
    cpi_month : str
        cpi month of the report, like May
    cpi_year : int
        cpi year of the report
    update_date : date
        update date, the format is date(2021,6,22)
    update_person : str
        who update the report
    testing : bool
        If true, use the testing database rather than the default database

    """
    db = AutomappedDB(testing=testing)
    new_record = Report(
        year=int(year),
        state=str(state),
        analysis_type=str(analysis_type),
        cpi_month=str(cpi_month),
        cpi_year=int(cpi_year),
        update_date=update_date,
        update_person=str(update_person),
    )
    # add to db
    with db.sessionmaker() as session:
        session.add(new_record)
        session.commit()


def delete_one_entry_reportdb(year, state, analysis_type, testing=False):
    """
    Delete one report entry.

    Parameters
    ----------
    year : int
        year of report
    state : str
        name of state
    analysis_type : str
        analysis type of sss, e.g. full, partial
    testing : bool
        If true, use the testing database rather than the default database

    """
    db = AutomappedDB(testing=testing)
    # delete the records that meets criteria
    with db.sessionmaker() as session:
        session.query(Report).filter(
            Report.year == year,
            Report.state == state,
            Report.analysis_type == analysis_type,
        ).delete()
        session.commit()
