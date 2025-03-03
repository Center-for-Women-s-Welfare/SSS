"""Code tests the functions that create GeoID table."""

import os

import pandas as pd
import pytest


from sss.data import DATA_PATH
from sss.geoid import GeoID, geo_identifier_creator

# We get this warning in the warnings test where we pass `-W error`, but it
# doesn't produce an error or even a warning under normal testing.
# developers in the pykernel and flask-sqlalchemy ignore it, we will too.
pytestmark = pytest.mark.filterwarnings(
    "ignore:unclosed database in <sqlite3.Connection:ResourceWarning"
)


@pytest.mark.filterwarnings("ignore:Unknown extension is not supported and will be")
def testgeo_identifier_creator(capsys):
    """Test to see if county_table and cpi_table are joined together."""

    # tests print message is created when we have duplicate rows in CPI table
    geo_identifier_creator(
        os.path.join(DATA_PATH, "geoid_data", "SSScounty-place-list_20220720.xlsx"),
        os.path.join(
            DATA_PATH,
            "geoid_data",
            "StateAbbreviation_Regions_07192022_AKu_duplicate_rows.xlsx",
        ),
    )

    out, _ = capsys.readouterr()
    print(out)
    assert (
        "Merge sucessful, but new rows were created due to"
        " duplications in right(CPI) table" in out
    )

    # test error message
    with pytest.raises(
        ValueError,
        match="Cannot merge, please check the two columns"
        " are named as 'state_alpha' and 'USPS Abbreviation'",
    ):
        geo_identifier_creator(
            os.path.join(
                DATA_PATH,
                "geoid_data",
                "SSScounty-place-list_20220720_misnamed_column.xlsx",
            ),
            os.path.join(
                DATA_PATH, "geoid_data", "StateAbbreviation_Regions_07192022_AKu.xlsx"
            ),
        )

    # test dataframe is correctly created
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

    # test dataframe is correctly created with duplicates across both files
    geoid_df_duplicate = geo_identifier_creator(
        os.path.join(
            DATA_PATH,
            "geoid_data",
            "SSScounty-place-list_20220720_duplicated_rows.xlsx",
        ),
        os.path.join(
            DATA_PATH,
            "geoid_data",
            "StateAbbreviation_Regions_07192022_AKu_duplicate_rows.xlsx",
        ),
    )

    assert geoid_df_duplicate.columns.tolist() == expected_cols

    for fips in expected_fips:
        assert (
            str(
                pd.unique(
                    geoid_df_duplicate.loc[geoid_df_duplicate["FIPS"] == fips, "state"]
                )[0]
            )
            == expected_fips[fips]
        )


@pytest.mark.filterwarnings("ignore:Unknown extension is not supported and will be")
def test_geoid_to_db(setup_and_teardown_package):
    """Test to see if geoid table was created."""
    db = setup_and_teardown_package

    with db.sessionmaker() as session:
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
