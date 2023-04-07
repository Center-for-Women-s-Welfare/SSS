import os

from sss.puma import PUMA
from sss.puma import read_puma, puma_crosswalk, puma_to_db
from sss.data import DATA_PATH

import pandas as pd


def test_read_puma():
    """ Test reading puma text files"""
    year = 2021
    df = read_puma(os.path.join(
        DATA_PATH,
        "puma_data",
        "puma_text",
        "PUMSEQ10_25.txt"), year)
    expected_cols = [
        "summary_level",
        "state_fips",
        "state_national_standards",
        "puma_code",
        "county_fips",
        "county_national_standards",
        "county_sub_fips",
        "county_sub_national_standards",
        "place_fips",
        "place_national_standards",
        "tract_code",
        "population",
        "house_number",
        "area_name",
        "year",
        "state"]
    assert expected_cols == df.columns.tolist()
    assert len(df.state_fips.unique().tolist()) == 1
    assert df.year.unique() == [year]


def test_puma_crosswalk():
    """ Test creating the crosswalk for WA"""
    year = 2015
    crosswalk = puma_crosswalk(
        os.path.join(DATA_PATH, "puma_data", "puma_text", "PUMSEQ10_53.txt"),
        year,
        os.path.join(DATA_PATH, "puma_data", "SSSplaces_NY&WA_PUMAcode.xlsx"))
    expected_cols = [
        "summary_level",
        "state_fips",
        "state",
        "puma_code",
        "county_fips",
        "county",
        "puma_area",
        "population",
        "year",
        "population_max",
        "weight",
        "place"]
    for col in expected_cols:
        assert col in crosswalk.columns.tolist()

    wa_places = [
        "King County (Seattle)",
        "King County (North)",
        "King County (East)",
        "King County (South)"]
    for place in wa_places:
        assert place in crosswalk.place.tolist()


def test_puma_to_db(setup_and_teardown_package):
    """ Tests columns and values to match in the database"""
    db,  db_file = setup_and_teardown_package
    session = db.sessionmaker()
    year = 2021
    puma_to_db(
        os.path.join(DATA_PATH, "puma_data", "puma_text", "PUMSEQ10_36.txt"),
        year,
        os.path.join(DATA_PATH, "puma_data", "SSSplaces_NY&WA_PUMAcode.xlsx"),
        db_file=db_file
    )
    crosswalk = puma_crosswalk(
        os.path.join(DATA_PATH, "puma_data", "puma_text", "PUMSEQ10_36.txt"),
        year,
        os.path.join(DATA_PATH, "puma_data", "SSSplaces_NY&WA_PUMAcode.xlsx")
    )
    # result = session.query(PUMA).filter(PUMA.state == "NY")
    result = session.query(PUMA).all()
    expected = {}
    for i in range(len(crosswalk)):
        key = crosswalk.loc[i, "puma_code"] + "_" + crosswalk.loc[i, "place"]
        expected[key] = PUMA(
            summary_level=crosswalk.loc[i, "summary_level"],
            state_fips=crosswalk.loc[i, "state_fips"],
            state=crosswalk.loc[i, "state"],
            puma_code=crosswalk.loc[i, "puma_code"],
            county_fips=crosswalk.loc[i, "county_fips"],
            county_sub_fips= None,
            county=crosswalk.loc[i, "county"],
            puma_area=crosswalk.loc[i, "puma_area"],
            place=crosswalk.loc[i, "place"],
            population=int(crosswalk.loc[i, "population"]),
            weight=crosswalk.loc[i, "weight"],
            year=int(crosswalk.loc[i, "year"])
        )

    for obj in result:
        key = obj.puma_code + "_" + obj.place
        assert obj.isclose(expected[key])
