"""Database consistency checking functions."""

from sqlalchemy import inspect
from sqlalchemy.exc import OperationalError


def is_valid_database(base, session):
    """
    Check that the current database matches the models declared in model base.

    Currently we check that all tables exist with all columns.

    What is not checked:

    * Column types are not verified
    * Relationships are not verified

    Parameters
    ----------
    base : Declarative Base
        Instance of SQLAlchemy Declarative Base to check.
    session : SQLAlchemy session
        Session to use, bound to an engine.

    Returns
    -------
    True if all declared models have corresponding tables and columns.

    """
    if base is None:
        from .base import Base

        base = Base

    engine = session.get_bind()
    try:  # This tries thrice with 5sec sleeps in between
        iengine = inspect(engine)
    except OperationalError:  # pragma: no cover
        import time

        time.sleep(5)
        try:
            iengine = inspect(engine)
        except OperationalError:
            time.sleep(5)
            iengine = inspect(engine)

    errors = False
    err_msg = ""

    tables = iengine.get_table_names()

    # Go through all SQLAlchemy models

    for table, klass in base.metadata.tables.items():
        if table in tables:
            # Check all columns are found
            # Looks like [{'default':
            #               "nextval('validity_check_test_id_seq'::regclass)",
            #              'autoincrement': True, 'nullable': False,
            #              'type': INTEGER(), 'name': 'id'}]

            columns = [c["name"] for c in iengine.get_columns(table)]
            mapper = inspect(klass)

            for column in mapper.columns:
                # Assume normal flat column
                if column.key not in columns:
                    err_msg = (
                        f"Model {klass} declares column {column.key} which "
                        f"does not exist in database {engine}"
                    )
                    errors = True
        else:
            err_msg = (
                f"Model {klass} declares table {table} which does not "
                f"exist in database {engine}"
            )
            errors = True

    return not errors, err_msg
