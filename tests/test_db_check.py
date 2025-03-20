import contextlib
import re
import warnings

import pytest
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, create_engine, text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, declared_attr, relationship, sessionmaker

from sss.db_check import is_valid_database

# We get this warning in the warnings test where we pass `-W error`, but it
# doesn't produce an error or even a warning under normal testing.
# developers in the pykernel and flask-sqlalchemy ignore it, we will too.
pytestmark = pytest.mark.filterwarnings(
    "ignore:unclosed database in <sqlite3.Connection:ResourceWarning"
)


def gen_test_model():
    base = declarative_base()

    class ValidTestModel(base):
        """A sample SQLAlchemy model to demostrate db conflicts."""

        __tablename__ = "validity_check_test"

        #: Running counter used in foreign key references
        id_ = Column(Integer, primary_key=True)
        foo = Column(Integer)

    return base, ValidTestModel


def gen_relation_models():
    base = declarative_base()

    class RelationTestModel(base):
        __tablename__ = "validity_check_test_2"
        id_ = Column(Integer, primary_key=True)

    class RelationTestModel2(base):
        __tablename__ = "validity_check_test_3"
        id_ = Column(Integer, primary_key=True)

        test_relationship_id = Column(ForeignKey("validity_check_test_2.id_"))
        test_relationship = relationship(
            RelationTestModel, primaryjoin=test_relationship_id == RelationTestModel.id_
        )

    return base, RelationTestModel, RelationTestModel2


def gen_declarative():
    base = declarative_base()

    class DeclarativeTestModel(base):
        __tablename__ = "validity_check_test_4"
        id_ = Column(Integer, primary_key=True)

        @declared_attr
        def _password(self):
            return Column("password", String(256), nullable=False)

        @hybrid_property
        def password(self):
            return self._password

    return base, DeclarativeTestModel


@pytest.fixture()
def temp_db(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("db") / "sss.sqlite"
    db_url = "sqlite:///" + str(db_file)
    engine = create_engine(db_url)

    with engine.connect() as test_conn, test_conn.begin() as test_trans:
        session = sessionmaker(bind=test_conn)
        with session() as test_session:
            yield engine, test_session

        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        with warnings.catch_warnings():
            # If an error was raised, rollback may have already been called.
            # If so, this will give a warning which we filter out here.
            warnings.filterwarnings(
                "ignore", "transaction already deassociated from connection"
            )
            test_trans.rollback()


def test_validity_pass(temp_db):
    """
    See database validity check completes when tables and columns are created.
    """
    base, valid_test_model = gen_test_model()
    engine, session = temp_db
    with contextlib.suppress(sqlalchemy.exc.NoSuchTableError):
        base.metadata.drop_all(engine, tables=[valid_test_model.__table__])

    base_is_none = is_valid_database(None, session)
    assert base_is_none

    base.metadata.create_all(engine, tables=[valid_test_model.__table__])

    try:
        db_valid, _ = is_valid_database(base, session)
        assert db_valid
    finally:
        base.metadata.drop_all(engine)


def test_validity_table_missing(temp_db):
    """See check fails when there is a missing table"""
    base, valid_test_model = gen_test_model()
    engine, session = temp_db

    with contextlib.suppress(sqlalchemy.exc.NoSuchTableError):
        base.metadata.drop_all(engine, tables=[valid_test_model.__table__])

    db_valid, valid_msg = is_valid_database(base, session)
    assert not db_valid
    expected_msg = (
        "Model validity_check_test declares table validity_check_test which does not "
        "exist in database"
    )

    assert re.compile(expected_msg).search(valid_msg)


def test_validity_column_missing(temp_db):
    """See check fails when there is a missing table"""
    engine, session = temp_db

    with engine.begin() as conn:
        session = sessionmaker(bind=engine)
        with session() as test_session:
            base, valid_test_model = gen_test_model()
            with contextlib.suppress(sqlalchemy.exc.NoSuchTableError):
                base.metadata.drop_all(engine, tables=[valid_test_model.__table__])
            base.metadata.create_all(engine, tables=[valid_test_model.__table__])

        # Delete one of the columns
        conn.execute(text("ALTER TABLE validity_check_test DROP COLUMN foo"))

    # use a new context manager to make sure there are no open transactions
    # without this it hangs
    with engine.begin() as conn:
        session = sessionmaker(bind=engine)
        with session() as test_session:
            db_valid, valid_msg = is_valid_database(base, test_session)
            assert not db_valid
            expected_msg = (
                "Model validity_check_test declares column foo which does not exist in "
                "database"
            )

        assert re.compile(expected_msg).search(valid_msg)


def test_validity_pass_relationship(temp_db):
    """
    See database validity check understands about relationships and don't
    deem them as missing column.
    """
    engine, session = temp_db

    base, relation_test_model, relation_test_model2 = gen_relation_models()
    with contextlib.suppress(sqlalchemy.exc.NoSuchTableError):
        base.metadata.drop_all(
            engine,
            tables=[relation_test_model.__table__, relation_test_model2.__table__],
        )

    base.metadata.create_all(
        engine, tables=[relation_test_model.__table__, relation_test_model2.__table__]
    )

    try:
        db_valid, _ = is_valid_database(base, session)
        assert db_valid
    finally:
        base.metadata.drop_all(engine)


def test_validity_pass_declarative(temp_db):
    """
    See database validity check understands about relationships and don't deem
    them as missing column.
    """
    engine, session = temp_db

    base, declarative_test_model = gen_declarative()
    with contextlib.suppress(sqlalchemy.exc.NoSuchTableError):
        base.metadata.drop_all(engine, tables=[declarative_test_model.__table__])

    base.metadata.create_all(engine, tables=[declarative_test_model.__table__])

    try:
        db_valid, _ = is_valid_database(base, session)
        assert db_valid
    finally:
        base.metadata.drop_all(engine)
