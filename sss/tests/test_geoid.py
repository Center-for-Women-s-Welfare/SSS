import os

from sss.data import DATA_PATH
from sss.geoid import GeoID
from sss.geoid import geoid_to_db


def test_geoid_todb(setup_and_teardown_package):
    """ Test to see if geoid tabsle was created"""
    db, db_file = setup_and_teardown_package
    session = db.sessionmaker()
    geoid_to_db(
        os.path.join(
            DATA_PATH,
            "geoid_data",
            "SSScounty-place-list_20220720.xlsx"),
        os.path.join(
            DATA_PATH,
            "geoid_data",
            "StateAbbreviation_Regions_07192022_AKu.xlsx"),
        db_file=db_file
    )

    result = session.query(GeoID).all()
    assert len(result) == 9

    result = session.query(GeoID).filter(GeoID.cpi_region == "South").all()
    assert len(result) == 2
