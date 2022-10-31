
import os

import pytest

from sss import base, sss_table
from sss.data import DATA_PATH

@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown_package(tmp_path_factory):
    
    test_db_file = os.path.join(tmp_path_factory.mktemp('test'),'test_sss.sqlite')
    sss_declare = base.DeclarativeDB(db_file=test_db_file)
   
    # then we call the create table function 
    sss_declare.create_tables()
    sss_table.data_folder_to_database(os.path.join(DATA_PATH), db_file=test_db_file)

    yield sss_declare, test_db_file
    
    sss_declare.drop_tables()