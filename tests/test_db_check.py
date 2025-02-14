# -*- mode: python; coding: utf-8 -*-
import re

import pytest
import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String, text, create_engine
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declarative_base, declared_attr, relationship, sessionmaker

from sss.db_check import is_valid_database


def gen_test_model():
    Base = declarative_base()

    class ValidTestModel(Base):
        """A sample SQLAlchemy model to demostrate db conflicts."""

        __tablename__ = "validity_check_test"

        #: Running counter used in foreign key references
        id_ = Column(Integer, primary_key=True)
        foo = Column(Integer)

    return Base, ValidTestModel


def gen_relation_models():
    Base = declarative_base()

    class RelationTestModel(Base):
        __tablename__ = "validity_check_test_2"
        id_ = Column(Integer, primary_key=True)

    class RelationTestModel2(Base):
        __tablename__ = "validity_check_test_3"
        id_ = Column(Integer, primary_key=True)

        test_relationship_id = Column(ForeignKey("validity_check_test_2.id_"))
        test_relationship = relationship(
            RelationTestModel, primaryjoin=test_relationship_id == RelationTestModel.id_
        )

    return Base, RelationTestModel, RelationTestModel2


def gen_declarative():
    Base = declarative_base()

    class DeclarativeTestModel(Base):
        __tablename__ = "validity_check_test_4"
        id_ = Column(Integer, primary_key=True)

        @declared_attr
        def _password(self):
            return Column("password", String(256), nullable=False)

        @hybrid_property
        def password(self):
            return self._password

    return Base, DeclarativeTestModel


@pytest.fixture()
def temp_db(tmp_path_factory):
    db_file = tmp_path_factory.mktemp("db") / "sss.sqlite"
    db_url = "sqlite:///" + str(db_file)
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    yield engine, session


def test_validity_pass(temp_db):
    """
    See database validity check completes when tables and columns are created.
    """
    Base, ValidTestModel = gen_test_model()
    engine, session = temp_db
    try:
        Base.metadata.drop_all(engine, tables=[ValidTestModel.__table__])
    except sqlalchemy.exc.NoSuchTableError:
        pass

    base_is_none = is_valid_database(None, session)
    assert base_is_none

    Base.metadata.create_all(engine, tables=[ValidTestModel.__table__])

    try:
        db_valid, _ = is_valid_database(Base, session)
        assert db_valid
    finally:
        Base.metadata.drop_all(engine)


def test_validity_table_missing(temp_db):
    """See check fails when there is a missing table"""
    Base, ValidTestModel = gen_test_model()
    engine, session = temp_db

    try:
        Base.metadata.drop_all(engine, tables=[ValidTestModel.__table__])
    except sqlalchemy.exc.NoSuchTableError:
        pass

    db_valid, valid_msg = is_valid_database(Base, session)
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
        Session = sessionmaker(bind=engine)
        session = Session()
        Base, ValidTestModel = gen_test_model()
        try:
            Base.metadata.drop_all(engine, tables=[ValidTestModel.__table__])
        except sqlalchemy.exc.NoSuchTableError:
            pass
        Base.metadata.create_all(engine, tables=[ValidTestModel.__table__])
        session.close()

        # Delete one of the columns
        conn.execute(text("ALTER TABLE validity_check_test DROP COLUMN foo"))

    # use a new context manager to make sure there are no open transactions
    # without this it hangs
    with engine.begin() as conn:
        Session = sessionmaker(bind=engine)
        session = Session()
        db_valid, valid_msg = is_valid_database(Base, session)
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

    Base, RelationTestModel, RelationTestModel2 = gen_relation_models()
    try:
        Base.metadata.drop_all(
            engine, tables=[RelationTestModel.__table__, RelationTestModel2.__table__]
        )
    except sqlalchemy.exc.NoSuchTableError:
        pass

    Base.metadata.create_all(
        engine, tables=[RelationTestModel.__table__, RelationTestModel2.__table__]
    )

    try:
        db_valid, _ = is_valid_database(Base, session)
        assert db_valid
    finally:
        Base.metadata.drop_all(engine)


def test_validity_pass_declarative(temp_db):
    """
    See database validity check understands about relationships and don't deem
    them as missing column.
    """
    engine, session = temp_db

    Base, DeclarativeTestModel = gen_declarative()
    try:
        Base.metadata.drop_all(engine, tables=[DeclarativeTestModel.__table__])
    except sqlalchemy.exc.NoSuchTableError:
        pass

    Base.metadata.create_all(engine, tables=[DeclarativeTestModel.__table__])

    try:
        db_valid, _ = is_valid_database(Base, session)
        assert db_valid
    finally:
        Base.metadata.drop_all(engine)
