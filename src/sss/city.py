"""Code to define and interact with the City table."""

import pandas as pd
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)

from .base import Base, AutomappedDB


# declare CITY data columns and data type
class City(Base):
    """
    Define the ``city`` table.

    This table links the SSS places to cities and
    provides population to allow for choosing similar
    sized cities to compare.

    Attributes
    ----------
    state : String Column
        name of the state, e.g. WA
    place : String Column
        SSS place name
    city : String Column
        sss_city, some cities of sss place
    census_name : String Column
        the census name of the city
    population : Integer Column
        number of the population of the city
    public_transit : Boolean Column
        whether the city is public transit or not

    """

    __tablename__ = "city"
    state = Column("state", String, primary_key=True)
    place = Column("place", String, primary_key=True)
    sss_city = Column("sss_city", String, primary_key=True)
    census_name = Column("census_name", String)
    population = Column("population", Integer)
    public_transit = Column("public_transit", Boolean)


def add_city(path, year):
    """
    Read city data into data frame and prepare for database table.

    Parameters
    ----------
    path: str
        path name of city excel file
    year: int
        year of the population data collected

    Returns
    -------
    pandas.datafranme
        the returned dataframe has population size by city

    Raises
    ------
    ValueError
        If the state cannot be extracted from SSS_city.

    """
    df = pd.read_excel(path)
    us_state_to_abbrev = {
        "Alabama": "AL",
        "Alaska": "AK",
        "Arizona": "AZ",
        "Arkansas": "AR",
        "California": "CA",
        "Colorado": "CO",
        "Connecticut": "CT",
        "Delaware": "DE",
        "Florida": "FL",
        "Georgia": "GA",
        "Hawaii": "HI",
        "Idaho": "ID",
        "Illinois": "IL",
        "Indiana": "IN",
        "Iowa": "IA",
        "Kansas": "KS",
        "Kentucky": "KY",
        "Louisiana": "LA",
        "Maine": "ME",
        "Maryland": "MD",
        "Massachusetts": "MA",
        "Michigan": "MI",
        "Minnesota": "MN",
        "Mississippi": "MS",
        "Missouri": "MO",
        "Montana": "MT",
        "Nebraska": "NE",
        "Nevada": "NV",
        "New Hampshire": "NH",
        "New Jersey": "NJ",
        "New Mexico": "NM",
        "New York": "NY",
        "North Carolina": "NC",
        "North Dakota": "ND",
        "Ohio": "OH",
        "Oklahoma": "OK",
        "Oregon": "OR",
        "Pennsylvania": "PA",
        "Rhode Island": "RI",
        "South Carolina": "SC",
        "South Dakota": "SD",
        "Tennessee": "TN",
        "Texas": "TX",
        "Utah": "UT",
        "Vermont": "VT",
        "Virginia": "VA",
        "Washington": "WA",
        "West Virginia": "WV",
        "Wisconsin": "WI",
        "Wyoming": "WY",
        "District of Columbia": "DC",
        "American Samoa": "AS",
        "Guam": "GU",
        "Northern Mariana Islands": "MP",
        "Puerto Rico": "PR",
        "United States Minor Outlying Islands": "UM",
        "U.S. Virgin Islands": "VI",
    }
    df["state"] = df["State"].map(us_state_to_abbrev)
    if df.state.isna().sum() > 0:
        raise ValueError(
            "could not find state in State value %s" % (df[df.state.isna()]["State"])
        )
    df["PublicTransit"] = df["PublicTransit"].astype("bool")
    df = df[
        [
            "state",
            "SSS_Place",
            "SSS_City",
            "Census_Name",
            "POPESTIMATE2021",
            "PublicTransit",
        ]
    ]
    df.columns = [
        "state",
        "place",
        "sss_city",
        "census_name",
        "population",
        "public_transit",
    ]
    df["year"] = year
    # drop the duplicates if the city infor is all the same
    df = df.drop_duplicates()
    df.reset_index(inplace=True, drop=True)
    return df


def city_to_db(data_path, year, testing=False):
    """
    Read city data as data frame and insert it to database.

    The data file needed is called "2020_PopulationDatabyCity_20220804_Ama.xlsx"

    Parameters
    ----------
    path: str
        path name of city excel file
    year: int
        year of the population data collected
    testing : bool
        If true, use the testing database rather than the default database

    """
    db = AutomappedDB(testing=testing)
    df_city = add_city(data_path, year)
    with db.sessionmaker() as session:
        session.bulk_insert_mappings(City, df_city.to_dict(orient="records"))
        session.commit()
