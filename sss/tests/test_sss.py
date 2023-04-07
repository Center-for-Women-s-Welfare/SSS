import os
import glob

import pandas as pd
import pytest
from sqlalchemy import update, bindparam

from sss import sss_table
from sss.data import DATA_PATH
from sss import SSS
from sss.sss_table import remove_state_year, data_folder_to_database


def test_read_file():
    """ Test reading file """
    df, file = sss_table.read_file(
        os.path.join(
            DATA_PATH,
            "sss_data",
            'AR2022_SSS_Full.xlsx'))

    expected_cols = ["family_type", "analysis_type"]

    for col in expected_cols:
        assert col in df.columns

    assert len(df.columns) == 27
    assert len(df) == 4


def test_check_extra_columns():
    """Test checking the extra columns: miscellaneous, health_care, analysis"""

    df, file = sss_table.read_file(
        os.path.join(
            DATA_PATH,
            "sss_data",
            'OR2021_SSS_ARPA_Full.xlsx'))
    df, arpa, health_care, miscellaneous = sss_table.check_extra_columns(df)

    columns_to_check = [
        'miscellaneous_is_secondary',
        'health_care_is_secondary',
        'analysis_is_secondary']

    for col in columns_to_check:
        assert col in df.columns

    assert not df.empty
    assert not arpa.empty


def test_check_extra_columns_error():
    """ Test occurency of the error in checking the etxra column """
    with pytest.raises(ValueError, match="df should be a pandas dataframe."):
        sss_table.check_extra_columns(
            os.path.join(
                DATA_PATH,
                "sss_data",
                'AR2022_SSS_Full.xlsx'))


def test_data_folder_to_database(setup_and_teardown_package):
    """ Test data folder to database """
    db, _ = setup_and_teardown_package
    session = db.sessionmaker()
    result = session.query(SSS).filter(SSS.state == 'FL').all()
    assert len(result) == 4
    result = session.query(SSS).filter(
        SSS.state == 'AZ', SSS.year == 2018).all()
    assert len(result) == 4
    session.close()


def test_columns_and_values_to_match(setup_and_teardown_package):
    """ Test columns and values to match"""
    db, _ = setup_and_teardown_package
    session = db.sessionmaker()
    query = session.query(SSS).filter(SSS.state == 'AL')
    with session.get_bind().connect() as connection:
        df = pd.read_sql(query.statement, connection)

    cols_to_check_for_val = ["housing"]

    for col in cols_to_check_for_val:
        assert col in df.columns


def test_remove_rows(setup_and_teardown_package):
    """ Test remove rows """
    db, db_file = setup_and_teardown_package
    session = db.sessionmaker()
    result = session.query(SSS).filter(SSS.state == 'AR').all()
    assert len(result) == 4

    remove_state_year("AR", 2022, db_file=db_file)
    result = session.query(SSS).filter(SSS.state == 'AR').all()
    assert len(result) == 0

    data_folder_to_database(
        os.path.join(
            DATA_PATH,
            "sss_data",
            'AR2022_SSS_Full.xlsx'),
        db_file=db_file
    )
    result = session.query(SSS).filter(SSS.state == 'AR').all()
    assert len(result) == 4


def test_add_food_col(setup_and_teardown_package):
    db, db_file = setup_and_teardown_package
    session = db.sessionmaker()

    # first check that the food column has good data in it.
    result_init = session.query(SSS).all()
    for obj in result_init:
        assert obj.food is not None

    # fill the food column with Nones
    statement = (update(SSS).values(food=None))
    session.execute(statement)
    session.commit()
    result = session.query(SSS).all()
    for obj in result:
        assert obj.food is None

    # update the food column
    data_files = glob.glob(os.path.join(DATA_PATH, "*.xls*"))
    for file in data_files:
        df, _ = sss_table.read_file(file)
        df, _, _, _ = sss_table.check_extra_columns(df)
        df = sss_table.prepare_for_database(df)
        pk_cols = ["family_type", "state", "place", "year", "analysis_type"]

        cols_to_keep = pk_cols + ["food"]
        cols_to_drop = [col for col in df.columns if col not in cols_to_keep]
        df.drop(columns=cols_to_drop, inplace=True)

        session.bulk_update_mappings(SSS, df.to_dict('records'))
        session.commit()

    # check that the food column has good data in it again
    result = session.query(SSS).all()
    for index, obj in enumerate(result):
        assert obj.food is not None
        # Add the following once the branch that adds the `isclose` method is merged in
        # assert obj.isclose(result_init[index])
