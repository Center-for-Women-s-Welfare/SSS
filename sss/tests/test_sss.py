import os
import pytest
from sss import sss_table
from sss.data import DATA_PATH
from sss import SSS
from sss.sss_table import remove_state_year, data_folder_to_database
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

    df, file = sss_table.read_file(os.path.join(DATA_PATH, 'OR2021_SSS_ARPA_Full.xlsx'))
    df, arpa, health_care, miscellaneous = sss_table.check_extra_columns(df)

    columns_to_check = ['miscellaneous_is_secondary', 'health_care_is_secondary', 'analysis_is_secondary']

    for col in columns_to_check:
        assert col in df.columns

    assert not df.empty
    # assert not miscellaneous.empty
    # assert not health_care.empty
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
    result = session.query(SSS).filter(SSS.state == 'FL').all()
    assert len(result) == 4
    result = session.query(SSS).filter(SSS.state == 'AZ', SSS.year == 2018).all()
    assert len(result) == 4
    session.close()

def test_columns_and_values_to_match(setup_and_teardown_package):
    """ Test columns and values to match"""
    db = setup_and_teardown_package
    session = db.sessionmaker()
    query = session.query(SSS).filter(SSS.state == 'AL')
    df = pd.read_sql(query.statement, db.engine)
    
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
    data_folder_to_database(os.path.join(DATA_PATH, 'AR2022_SSS_Full.xlsx'),  db_file = db_file)
    result = session.query(SSS).filter(SSS.state == 'AR').all()
    assert len(result) == 4