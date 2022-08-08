import os

import pytest

from sss import sss_table
from sss.data import DATA_PATH
import sss
from sss.base import AutomappedDB
from sss.tests import test_db_url

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

    assert 'miscellaneous_is_secondary' and 'health_care_is_secondary' and 'analysis_is_secondary' in df.columns

def test_check_extra_columns_error(setup_and_teardown_package):
    with pytest.raises(ValueError, match="df should be a pandas dataframe."):
        df, miscellaneous, health_care, arpa = sss_table.check_extra_columns((os.path.join(DATA_PATH)), 'AR2022_SSS_Full.xlsx')

def test_data_folder_to_database(setup_and_teardown_package):
    db = AutomappedDB(test_db_url)
    session = db.sessionmaker()
    sss_table.data_folder_to_database(os.path.join(DATA_PATH, db_url=test_db_url))
    result = session.query('SSS').filter('SSS'.State == 'CA').all()
    assert len(result) == 4
    session.close()
# def test_create_database():
#     """  Test creating a database """
#     sss_table.data_folder_to_database(DATA_PATH)

# def test_read_file():
#     sss_table.read_file(file)

# def test_check_connection():
#     sss.db_check.check_connection(session)

# def test_is_valid_database():
#     sss.db_check.is_valid_database(base, session)

# def test_geoidentifier_creator():
#     sss.geo_id.geogeoidentifier_creator(county_table, cpi_table)

# def test_std_col_names():
#     sss.preprocess.std_col_names(pd_dataframe)

# def test_pre_check():
#     sss_table.pre_check(df)

# def test_data_folder_to_database():
#     sss_table.data_folder_to_database(data_folder)
