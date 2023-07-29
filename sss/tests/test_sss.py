"""Test the functions that create the SSS table."""

import os
import re

import pandas as pd
import pytest
from sqlalchemy import update

from sss import sss_table
from sss.data import DATA_PATH
from sss import SSS, ARPA, Miscellaneous, HealthCare
from sss.sss_table import remove_state_year, data_folder_to_database


def test_read_file(capsys):
    """Test reading files."""
    # regular file, with multiple sheets
    df, _ = sss_table.read_file(
        os.path.join(DATA_PATH, "sss_data", "AR2022_SSS_Full.xlsx")
    )

    expected_cols = ["family_type", "analysis_type"]

    for col in expected_cols:
        assert col in df.columns

    assert len(df.columns) == 27
    assert len(df) == 4

    # read a file with just two sheets
    df_two_sheets, _ = sss_table.read_file(
        os.path.join(DATA_PATH, "sss_data", "FL2021_SSS_Full.xlsb")
    )
    assert len(df_two_sheets.columns) == 25
    assert len(df_two_sheets) == 4

    # test print statement comes out when file cannot be read
    sss_table.read_file(os.path.join(DATA_PATH, "poverty_th.csv"))

    out, _ = capsys.readouterr()
    assert "This file cannot be read:" in out
    assert "poverty_th.csv" in out


def test_check_extra_columns():
    """Test checking the extra columns: miscellaneous, health_care, analysis."""
    df, file = sss_table.read_file(
        os.path.join(DATA_PATH, "sss_data", "OR2021_SSS_ARPA_Full.xlsx")
    )
    df, arpa, health_care, miscellaneous = sss_table.check_extra_columns(df)

    columns_to_check = [
        "miscellaneous_is_secondary",
        "health_care_is_secondary",
        "analysis_is_secondary",
    ]

    for col in columns_to_check:
        assert col in df.columns

    assert not df.empty
    assert not arpa.empty


def test_check_extra_columns_error():
    """Test occurency of the error in checking the etxra column."""
    with pytest.raises(ValueError, match="df should be a pandas dataframe."):
        sss_table.check_extra_columns(
            os.path.join(DATA_PATH, "sss_data", "AR2022_SSS_Full.xlsx")
        )


def test_data_folder_to_database(setup_and_teardown_package):
    """Test data folder to database."""
    db = setup_and_teardown_package
    session = db.sessionmaker()
    result = session.query(SSS).filter(SSS.state == "FL").all()
    assert len(result) == 4
    result = session.query(SSS).filter(SSS.state == "AZ", SSS.year == 2018).all()
    assert len(result) == 4
    session.close()


def test_columns_and_values_to_match(setup_and_teardown_package):
    """Test columns and values to match."""
    db = setup_and_teardown_package
    session = db.sessionmaker()
    query = session.query(SSS).filter(SSS.state == "AL")
    with session.get_bind().connect() as connection:
        df = pd.read_sql(query.statement, connection)

    cols_to_check_for_val = ["housing"]

    for col in cols_to_check_for_val:
        assert col in df.columns


def test_remove_rows(setup_and_teardown_package):
    """Test remove rows."""
    db = setup_and_teardown_package
    session = db.sessionmaker()
    result = session.query(SSS).filter(SSS.state == "AR").all()
    assert len(result) == 4

    remove_state_year("AR", 2022, testing=True)
    result = session.query(SSS).filter(SSS.state == "AR").all()
    assert len(result) == 0

    data_folder_to_database(
        os.path.join(DATA_PATH, "sss_data", "AR2022_SSS_Full.xlsx"), testing=True
    )
    result = session.query(SSS).filter(SSS.state == "AR").all()
    assert len(result) == 4

    with pytest.raises(ValueError, match="State must be a string"):
        remove_state_year(2022, 2022, testing=True)

    with pytest.raises(ValueError, match="Year must be a integer"):
        remove_state_year("AR", "2022", testing=True)


@pytest.mark.parametrize(
    "columns",
    [
        "food",
        ["food"],
        ["food", "transportation"],
        ["food", "payroll_taxes", "premium", "broadband_and_cell_phone"],
    ],
)
def test_add_column(setup_and_teardown_package, columns):
    """Test column was added."""
    db = setup_and_teardown_package
    session = db.sessionmaker()

    if isinstance(columns, str):
        columns_list = [columns]
    else:
        columns_list = columns

    table_dict = {
        "sss": {
            "object": SSS,
        },
        "arpa": {
            "object": ARPA,
        },
        "health_care": {
            "object": HealthCare,
        },
        "misc": {
            "object": Miscellaneous,
        },
    }

    for _, meta_dict in table_dict.items():
        meta_dict["obj_list"] = session.query(meta_dict["object"]).all()

        meta_dict["col_list"] = []
        for col in columns_list:
            if hasattr(meta_dict["obj_list"][0], col):
                meta_dict["col_list"].append(col)

        if len(meta_dict["col_list"]) > 0:
            for obj in meta_dict["obj_list"]:
                for col in meta_dict["col_list"]:
                    assert getattr(obj, col) is not None

            for col in meta_dict["col_list"]:
                update_dict = {col: None}
                statement = update(meta_dict["object"]).values(update_dict)
                session.execute(statement)
                session.commit()

            result = session.query(meta_dict["object"]).all()
            for obj in result:
                for col in meta_dict["col_list"]:
                    assert getattr(obj, col) is None

    # update the columns
    sss_table.update_columns(os.path.join(DATA_PATH, "sss_data"), columns, testing=True)

    # this commit should not be necessary since it's being done in the function,
    # but it seems to be required.
    session.commit()

    # check that the food column has good data in it again
    for _, meta_dict in table_dict.items():
        if len(meta_dict["col_list"]) > 0:
            result = session.query(meta_dict["object"]).all()
            for obj in result:
                for col in meta_dict["col_list"]:
                    assert getattr(obj, col) is not None


def test_add_column_errors(setup_and_teardown_package):
    """Test errors with new column."""
    with pytest.raises(
        ValueError, match="data_path must be a file or folder on this system"
    ):
        sss_table.update_columns("foo", "food", testing=True)

    with pytest.raises(
        ValueError, match=re.escape(f"No data files identified in {DATA_PATH}")
    ):
        sss_table.update_columns(DATA_PATH, "food", testing=True)

    with pytest.raises(ValueError, match="Cannot update a primary key column."):
        sss_table.update_columns(
            os.path.join(DATA_PATH, "sss_data"), "state", testing=True
        )
