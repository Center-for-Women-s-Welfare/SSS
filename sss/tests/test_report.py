# TODO: test_add_one_entry_reportdb()
# TODO: test_delete_one_entry_reportdb()

import os
import datetime

import numpy as np
import pandas as pd

from sss.data import DATA_PATH
from sss.report import Report
from sss.report import add_report, report_to_db


def test_add_report():
    """ Tests to see if reading report file works"""
    report_df = add_report(
        os.path.join(
            DATA_PATH,
            "report_data",
            "Year_Type_SSS_CPI month year_20220715_DBu.xlsx"))
    assert len(report_df.index) == 7

    nc_row = report_df.loc[report_df['state'] == "NC"]
    nc_row = nc_row.reset_index(inplace=True)

    nc_expected = [{
        "year": 2022,
        "state": "NC",
        "analysis_type": "Partial",
        "cpi_month": "January",
        "cpi_year": 2022,
        "update_date": "2022-06-22",
        "update_person": "Ama"
    }]
    nc_test_df = pd.DataFrame.from_dict(nc_expected)
    nc_test_df = nc_test_df.reset_index(inplace=True)

    assert nc_row == nc_test_df


def test_report_to_db(setup_and_teardown_package):
    """ Test to see if report table was created"""
    db, db_file = setup_and_teardown_package
    session = db.sessionmaker()
    report_to_db(
        os.path.join(
            DATA_PATH,
            "report_data",
            "Year_Type_SSS_CPI month year_20220715_DBu.xlsx"),
        db_file=db_file
    )

    result = session.query(Report).all()
    assert len(result) == 7

    result = session.query(Report).all()
    expected = {}
    report_df = pd.read_excel(
        os.path.join(
            DATA_PATH,
            "report_data",
            "Year_Type_SSS_CPI month year_20220715_DBu.xlsx"))
    report_df.columns = report_df.columns.str.lower().str.replace(' ', '_')
    report_df["year"] = report_df['year'].astype(int)
    report_df["update_person"] = report_df[
        'upload_status'].str.split(' ').str[0]
    report_df.update_person.replace({np.nan: None}, inplace=True)
    report_df["update_date"] = report_df[
        'upload_status'].str.split(' ').str[1]
    print(report_df["update_date"])
    report_df["update_date"] = pd.to_datetime(
        report_df["update_date"], format="mixed", dayfirst=False)
    report_df["update_date"] = report_df[
        'update_date'].map(lambda x: datetime.datetime.date(x))

    for i in range(len(report_df)):
        expected[report_df.loc[i, "state"]] = Report(
            year=report_df.loc[i, "year"].item(),
            state=report_df.loc[i, "state"],
            analysis_type=report_df.loc[i, "type"],
            cpi_month=report_df.loc[i, "cpi_month"],
            cpi_year=int(report_df.loc[i, "cpi_year"]),
            update_date=report_df.loc[i, "update_date"],
            update_person=report_df.loc[i, "update_person"]
        )

    for obj in result:
        assert obj.isclose(expected[obj.state])

    # want to read the report file
    # iterate through each row, for each state, create Report class
