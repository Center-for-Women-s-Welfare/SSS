import os

from sss import sss_table
from sss.data import DATA_PATH
import sss

def test_read_file(setup_and_teardown_package):
    """ Test reading file """
    df, file = sss_table.read_file(os.path.join(DATA_PATH, 'AR2022_SSS_Full.xlsx'))

    expected_cols = ["family_type", "analysis_type"]

    for col in expected_cols:
        assert col in df.columns

    assert len(df.columns) == 27
    assert len(df) == 4

    #session = setup_and_teardown_package.sessionmaker()

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

# def test_check_extra_columns():
#     sss_table.check_extra_columns(df)

# def test_data_folder_to_database():
#     sss_table.data_folder_to_database(data_folder)
