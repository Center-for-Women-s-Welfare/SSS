from abc import ABCMeta
from datetime import date

import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import (
    create_engine,
    MetaData
)

default_db_file = 'sss.sqlite'


class Base():
    """Base table object."""

    def __repr__(self):
        """Define standard representation."""
        columns = self.__table__.columns.keys()
        rep_str = "<" + self.__class__.__name__ + "("
        for c in columns:
            rep_str += str(getattr(self, c)) + ", "
        rep_str = rep_str[0:-2]
        rep_str += ")>"
        return rep_str

    def isclose(self, other):
        """Test if two objects are nearly equal."""
        if not isinstance(other, self.__class__):
            print("not the same class")
            return False

        self_columns = self.__table__.columns
        other_columns = other.__table__.columns
        # the following is structured as an assert because I cannot make it fail but
        # think it should be checked.
        assert {col.name for col in self_columns} == {
            col.name for col in other_columns
        }, (
            "Set of columns are not the same. This should not happen, please make an "
            "issue in our repo."
        )
        for col in self_columns:
            self_col = getattr(self, col.name)
            other_col = getattr(other, col.name)
            if not isinstance(other_col, type(self_col)):
                print(
                    f"column {col} has different types, left is {type(self_col)}, "
                    f"right is {type(other_col)}."
                )
                return False
            if isinstance(self_col, int):
                if self_col != other_col:
                    print(f"column {col} is int, values are not equal")
                    return False
            elif isinstance(self_col, str):
                if self_col != other_col:
                    print(f"column {col} is str, values are not equal")
                    return False
            elif isinstance(self_col, date):
                if self_col != other_col:
                    print(f"column {col} is a datetime, values are not equal")
                    return False
            elif self_col is None:
                pass  # nullable columns, both null (otherwise caught as different types)
            else:
                if hasattr(self, "tols") and col.name in self.tols.keys():
                    atol = self.tols[col.name]["atol"]
                    rtol = self.tols[col.name]["rtol"]
                else:
                    # use numpy defaults
                    atol = 1e-08
                    rtol = 1e-05
                if isinstance(self_col, (np.ndarray, list)):
                    if not np.allclose(self_col, other_col, atol=atol, rtol=rtol):
                        print(
                            f"column {col} is float-like or a float-like array, "
                            "values are not equal"
                        )
                        return False
                else:
                    if not np.isclose(self_col, other_col, atol=atol, rtol=rtol):
                        print(
                            f"column {col} is float-like or a float-like array, "
                            "values are not equal"
                        )
                        return False
        return True


Base = declarative_base(cls=Base)


class DB(object, metaclass=ABCMeta):
    """
    Abstract base class for SSS database object.

    This ABC is only instantiated through the AutomappedDB or DeclarativeDB
    subclasses.

    Parameters
    ----------
    db_file : str
        Database file name, ends with '.sqlite'.

    """

    engine = None
    sessionmaker = sessionmaker()
    sqlalchemy_base = None

    def __init__(self, sqlalchemy_base, db_file=default_db_file):  # noqa
        db_url = 'sqlite:///' + db_file
        self.sqlalchemy_base = Base
        self.engine = create_engine(db_url)
        self.sessionmaker.configure(bind=self.engine)


class DeclarativeDB(DB):
    """
    Declarative database object -- to create database tables.

    Parameters
    ----------
    db_file : str
        database file name, ends with '.sqlite'.

    """

    def __init__(self, db_file=default_db_file):
        super(DeclarativeDB, self).__init__(Base, db_file)

    def create_tables(self):
        """Create all tables."""
        self.sqlalchemy_base.metadata.create_all(self.engine)

    def drop_tables(self):
        """Drop all tables."""
        self.sqlalchemy_base.metadata.bind = self.engine
        self.sqlalchemy_base.metadata.drop_all(self.engine)


class AutomappedDB(DB):
    """Automapped database object -- attaches to an existing database.

    This is intended for use with the production database. __init__()
    raises an exception if the existing database does not match the schema
    defined in the SQLAlchemy initialization magic.

    Parameters
    ----------
    db_file : str
        database file name, ends with '.sqlite'.

    """

    def __init__(self, db_file=default_db_file):
        super(AutomappedDB, self).__init__(automap_base(), db_file)

        from .db_check import is_valid_database

        with self.sessionmaker() as session:
            if not is_valid_database(Base, session):
                raise RuntimeError(
                    "database {0} does not match expected schema".format(db_file)
                )
