"""Code that defines the Capital table."""

from tkinter.filedialog import test
import pandas as pd
from sqlalchemy import Column, String, Integer
from .base import Base, AutomappedDB

# declare Capital data columns and data type
class Capital(Base):
    """
    Defines the `Capital` table

    The data for this table comes from ...

    Attributes
    ----------
    state : String Column
        name of state
    city : String Column
        name of city
    capital : String Column
        name of capital of the city
    population : Integer Column
        numeric value representing population at ...
    """

    __tablename__ = "capital"
    state = Column("state", String, primary_key=True)
    city = Column("city", String, primary_key=True)
    capital = Column("capital", String)
    population = Column("population", Integer)
    year = Column("year", Integer)

def capital_creater(capital_file, year):
    """
    Read in file for capital information

    Parameters
    ----------
    capital_file : string
        The path of the capital data
    """
    df = pd.read_excel(capital_file)
    df["population"] = df["population"].astype("Integer")
    df["year"] = year
    return df

def capital_to_db(path, year, testing=False):
    """
    Puts Capital data into database.

    Parameters
    ----------
    path : str
        path name of the capital file that we want 
    year : int
        year that the population data comes from
    testing : bool
        If true, use the testing database
    """
    capital_df = capital_creater(path, year)
    db = AutomappedDB(testing=testing)
    session = db.sessionmaker()
    session.bulk_insert_mappings(Capital, capital_df.to_dict(orient="records"))
    session.commit()
    session.close()

