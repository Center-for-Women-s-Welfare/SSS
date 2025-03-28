"""Code to tests the functions used to create City table."""

import os

import pandas as pd
import pytest

from sss.city import City, add_city
from sss.data import DATA_PATH

# We get this warning in the warnings test where we pass `-W error`, but it
# doesn't produce an error or even a warning under normal testing.
# developers in the pykernel and flask-sqlalchemy ignore it, we will too.
pytestmark = pytest.mark.filterwarnings(
    "ignore:unclosed database in <sqlite3.Connection:ResourceWarning"
)


def test_add_city():
    """Test if the city file is being read and formatted correctly."""
    test_df = add_city(
        os.path.join(
            DATA_PATH, "city_data", "2020_PopulationDatabyCity_20220804_Ama.xlsx"
        ),
        2021,
    )

    assert len(test_df.index) == 4

    assert list(test_df["state"]) == ["AZ", "KS", "OR", "PA"]

    with pytest.raises(ValueError, match="could not find state in State value"):
        add_city(
            os.path.join(
                DATA_PATH,
                "city_data",
                "2020_PopulationDatabyCity_20220804_Ama_incorrect_state_name.xlsx",
            ),
            2021,
        )


def test_city_to_db(setup_and_teardown_package):
    """Test to see if city table was created."""
    db = setup_and_teardown_package

    with db.sessionmaker() as session:
        result = session.query(City).all()
        assert len(result) == 4

        result = session.query(City).filter(City.place == "Maricopa County").all()
        assert len(result) == 1

        result = session.query(City).all()
    expected = {}
    df = pd.read_excel(
        os.path.join(
            DATA_PATH, "city_data", "2020_PopulationDatabyCity_20220804_Ama.xlsx"
        )
    )
    state_dict = {"Arizona": "AZ", "Pennsylvania": "PA", "Kansas": "KS", "Oregon": "OR"}
    for i in range(len(df)):
        expected[df.loc[i, "SSS_City"]] = City(
            state=state_dict[df.loc[i, "State"]],
            place=df.loc[i, "SSS_Place"],
            sss_city=df.loc[i, "SSS_City"],
            census_name=df.loc[i, "Census_Name"],
            population=int(df.loc[i, "POPESTIMATE2021"]),
            public_transit=bool(df.loc[i, "PublicTransit"]),
        )

    for obj in result:
        assert obj.isclose(expected[obj.sss_city])
