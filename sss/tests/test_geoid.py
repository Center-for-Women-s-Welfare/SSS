"""Code tests the functions that create GeoID table."""

import os

import pandas as pd
import pytest

from sss.data import DATA_PATH
from sss.geoid import GeoID, geo_identifier_creator


@pytest.mark.filterwarnings("ignore:Unknown extension is not supported and will be")
def testgeo_identifier_creator():
    """Test to see if county_table and cpi_table are joined together."""
    geoid_df = geo_identifier_creator(
        os.path.join(DATA_PATH, "geoid_data", "SSScounty-place-list_20220720.xlsx"),
        os.path.join(
            DATA_PATH, "geoid_data", "StateAbbreviation_Regions_07192022_AKu.xlsx"
        ),
    )
    expected_cols = [
        "FIPS",
        "fips2010",
        "state",
        "areaname",
        "countyname",
        "county_town_name",
        "place",
        "state_fips",
        "county_fips",
        "place_fips",
        "State Name",
        "USPS Abbreviation",
        "cpi_region",
    ]
    assert geoid_df.columns.tolist() == expected_cols

    expected_fips = {
        "05027": "AR",
        "17133": "IL",
        "31061": "NE",
        "34009": "NJ",
        "35019": "NM",
        "45013": "SC",
        "46129": "SD",
        "53033": "WA",
        "55091": "WI",
    }

    for fips in expected_fips:
        assert (
            geoid_df.loc[geoid_df["FIPS"] == fips, "state"].to_string(index=False)
            == expected_fips[fips]
        )


@pytest.mark.filterwarnings("ignore:Unknown extension is not supported and will be")
def test_geoid_to_db(setup_and_teardown_package):
    """Test to see if geoid tabsle was created."""
    db = setup_and_teardown_package
    session = db.sessionmaker()

    result = session.query(GeoID).all()
    assert len(result) == 9

    result = session.query(GeoID).filter(GeoID.cpi_region == "South").all()
    assert len(result) == 2

    result = session.query(GeoID).all()
    county_df = pd.read_excel(
        os.path.join(DATA_PATH, "geoid_data", "SSScounty-place-list_20220720.xlsx"),
        dtype=str,
    )
    # add county_df columns
    county_df["state_fips"] = county_df["fips2010"].str[:2]
    county_df["county_fips"] = county_df["fips2010"].str[2:5]
    county_df["place_fips"] = county_df["fips2010"].str[5:]
    cpi_df = pd.read_excel(
        os.path.join(
            DATA_PATH, "geoid_data", "StateAbbreviation_Regions_07192022_AKu.xlsx"
        )
    )

    expected = {}
    for i in range(len(county_df)):
        expected[county_df.loc[i, "SSS_Place"]] = GeoID(
            state=county_df.loc[i, "state_alpha"],
            place=county_df.loc[i, "SSS_Place"],
            state_fips=county_df.loc[i, "state_fips"],
            county_fips=county_df.loc[i, "county_fips"],
            place_fips=county_df.loc[i, "place_fips"],
            cpi_region=cpi_df.loc[
                cpi_df["USPS Abbreviation"] == county_df.loc[i, "state_alpha"],
                "CPI Region",
            ].to_string(index=False),
        )

    for obj in result:
        assert obj.isclose(expected[obj.place])
