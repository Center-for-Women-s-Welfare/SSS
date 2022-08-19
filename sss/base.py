from abc import ABCMeta

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import (
    create_engine,
    MetaData
)

default_db_file = 'sss.sqlite'
Base = declarative_base()

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
