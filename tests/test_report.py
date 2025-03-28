"""Test the functions that create the Report table."""

import os
from datetime import datetime

import pandas as pd
import pytest

from sss.data import DATA_PATH
from sss.report import (
    Report,
    add_one_entry_reportdb,
    add_report,
    delete_one_entry_reportdb,
)

# We get this warning in the warnings test where we pass `-W error`, but it
# doesn't produce an error or even a warning under normal testing.
# developers in the pykernel and flask-sqlalchemy ignore it, we will too.
pytestmark = pytest.mark.filterwarnings(
    "ignore:unclosed database in <sqlite3.Connection:ResourceWarning"
)


def test_add_report():
    """Tests to see if reading report file works."""
    report_df = add_report(
        os.path.join(
            DATA_PATH, "report_data", "Year_Type_SSS_CPI month year_20220715_DBu.xlsx"
        )
    )
    assert len(report_df.index) == 8

    nc_row = report_df.loc[report_df["state"] == "NC"]
    nc_row = nc_row.reset_index(inplace=True)

    nc_expected = [
        {
            "year": 2022,
            "state": "NC",
            "analysis_type": "Partial",
            "cpi_month": "January",
            "cpi_year": 2022,
            "update_date": "2022-06-22",
            "update_person": "Ama",
        }
    ]
    nc_test_df = pd.DataFrame.from_dict(nc_expected)
    nc_test_df = nc_test_df.reset_index(inplace=True)

    assert nc_row == nc_test_df


def test_report_to_db(setup_and_teardown_package):
    """Test to see if report table was created."""
    db = setup_and_teardown_package

    with db.sessionmaker() as session:
        result = session.query(Report).all()
        assert len(result) == 8

        result = session.query(Report).all()
    expected = {}
    report_df = pd.read_excel(
        os.path.join(
            DATA_PATH, "report_data", "Year_Type_SSS_CPI month year_20220715_DBu.xlsx"
        )
    )
    report_df.columns = report_df.columns.str.lower().str.replace(" ", "_")
    report_df["year"] = report_df["year"].astype(int)
    report_df["upload_status"] = report_df["upload_status"].where(
        pd.notnull(report_df["upload_status"]), None
    )
    report_df["update_person"] = report_df["upload_status"].str.split(" ").str[0]
    report_df["update_date"] = report_df["upload_status"].str.split(" ").str[1]
    for i in range(len(report_df)):
        try:
            report_df.loc[i, "update_date"] = pd.to_datetime(
                report_df.loc[i, "update_date"], format="%m/%d/%y"
            )
        except ValueError:
            report_df.loc[i, "update_date"] = datetime.strptime(
                report_df.loc[i, "update_date"], "%m/%d/%Y"
            ).strftime("%m/%d/%y")
            report_df.loc[i, "update_date"] = pd.to_datetime(
                report_df.loc[i, "update_date"], format="%m/%d/%y"
            )

    report_df["update_date"] = report_df["update_date"].map(
        lambda x: datetime.date(x), na_action="ignore"
    )

    for i in range(len(report_df)):
        expected[report_df.loc[i, "state"]] = Report(
            year=report_df.loc[i, "year"].item(),
            state=report_df.loc[i, "state"],
            analysis_type=report_df.loc[i, "type"],
            cpi_month=report_df.loc[i, "cpi_month"],
            cpi_year=int(report_df.loc[i, "cpi_year"]),
            update_date=report_df.loc[i, "update_date"],
            update_person=report_df.loc[i, "update_person"],
        )

    for obj in result:
        assert obj.isclose(expected[obj.state])


def test_add_one_entry_reportdb(setup_and_teardown_package):
    """Test to add one report."""
    db = setup_and_teardown_package

    add_one_entry_reportdb(
        2023,
        "NY",
        "Partial",
        "April",
        2022,
        datetime(2023, 4, 14),
        "Hector",
        testing=True,
    )
    with db.sessionmaker() as session:
        result = session.query(Report).all()
    assert len(result) == 9


def test_delete_one_entry_reportdb(setup_and_teardown_package):
    """Test to delete one report."""
    db = setup_and_teardown_package

    delete_one_entry_reportdb(2018, "FL", "Full", testing=True)

    with db.sessionmaker() as session:
        result = session.query(Report).all()

    assert len(result) == 8
