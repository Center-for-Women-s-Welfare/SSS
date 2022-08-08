from sss import sss_table
from sss.data import DATA_PATH
import sss


def test_create_database():
    """  Test creating a database """
    sss_table.data_folder_to_database(DATA_PATH)

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
