
import os

import pytest

from sss import base, sss_table
from sss.tests import test_db_url
from sss.data import DATA_PATH

@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown_package():
    
    sss_declare = base.DeclarativeDB(test_db_url)
   
    # then we call the create table function 
    sss_declare.create_tables()
    sss_table.data_folder_to_database(os.path.join(DATA_PATH), db_url=test_db_url)

    yield sss_declare
    
    sss_declare.drop_tables()