import os
import pytest
from sss import sss_table
from sss.data import DATA_PATH
import sss
from sss.base import AutomappedDB
from sss.tests import test_db_url
from sss import SSS
import pandas as pd

def test_read_file(setup_and_teardown_package):
    """ Test reading file """
    df, file = sss_table.read_file(os.path.join(DATA_PATH, 'AR2022_SSS_Full.xlsx'))

    expected_cols = ["family_type", "analysis_type"]

    for col in expected_cols:
        assert col in df.columns

    assert len(df.columns) == 27
    assert len(df) == 4

    #session = setup_and_teardown_package.sessionmaker()

def test_check_extra_columns(setup_and_teardown_package):
    """ Test checking the extra columns: miscellaneous_is_secondary, health_care_is_secondary, analysis_is_secondary """

    df, file = sss_table.read_file(os.path.join(DATA_PATH, 'AR2022_SSS_Full.xlsx'))
    df, miscellaneous, health_care, arpa = sss_table.check_extra_columns(df)

    columns_to_check = ['miscellaneous_is_secondary', 'health_care_is_secondary', 'analysis_is_secondary']

    for col in columns_to_check:
        assert col in df.columns

    assert not df.empty
    assert not miscellaneous.empty
    assert not health_care.empty
    assert not arpa.empty

    # TODO: Actually check values inside of the dataframes. 

def test_check_extra_columns_error(setup_and_teardown_package):
    """ Test occurency of the error in checking the etxra column """
    with pytest.raises(ValueError, match="df should be a pandas dataframe."):
        df, miscellaneous, health_care, arpa = sss_table.check_extra_columns(os.path.join(DATA_PATH, 'AR2022_SSS_Full.xlsx'))

def test_data_folder_to_database(setup_and_teardown_package):
    """ Test data folder to database """
    db = setup_and_teardown_package
    session = db.sessionmaker()
    sss_table.data_folder_to_database(os.path.join(DATA_PATH), db_url=test_db_url)
    result = session.query(SSS).filter(SSS.state == 'FL').all()
    assert len(result) == 4
    session.close()

def test_columns_and_values_to_match(setup_and_teardown_package):
     """ Test columns and values to match"""
     db = setup_and_teardown_package
     session = db.sessionmaker()
     sss_table.data_folder_to_database(os.path.join(DATA_PATH), db_url=test_db_url)
     result = session.query(SSS).filter(SSS.state == 'AL').all()
     df = pd.read_sql(query.statement, db.engine)
     
     cols_to_check_for_val = ["housing"]
     
     for col in cols_to_check_for_val:
        assert col in df.columns
