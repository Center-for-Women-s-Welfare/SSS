
import pytest
from sss import base
from sss.tests import test_db_url

@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown_package():
    
    sss_declare = base.DeclarativeDB(test_db_url)
    # then we call the create table function 
    sss_declare.create_tables()

    yield sss_declare
    
    sss_declare.drop_tables()