"""Test base."""

import datetime
import json
import os

import numpy as np

import sss
from sss import Report, GeoID, SSS
from sss.base import config_file, get_db_file

default_datetime = datetime.datetime(2023, 4, 14)


def report_obj(year=2022, state="WA", date=default_datetime):
    test_report = Report(
        year=year,
        state=state,
        analysis_type="full",
        cpi_month="June",
        cpi_year=2021,
        update_date=date,
        update_person="foo",
    )

    return test_report


def geoid_obj():
    test_geoid = GeoID(
        state="WA",
        place="King County",
        state_fips="53",
        county_fips="033",
        place_fips="99999",
        cpi_region="West",
    )

    return test_geoid


def sss_obj(misc_bool=True, hourly_wage=11.04):
    test_sss = SSS(
        family_type="a1i0p0s0t0",
        state="WA",
        place="King County",
        analysis_type="full",
        year=2022,
        adult=1,
        infant=0,
        preschooler=0,
        schoolager=0,
        teenager=0,
        weighted_child_count=0,
        housing=527.0,
        child_care=0.0,
        food=279.0,
        transportation=307.0,
        health_care=214.0,
        miscellaneous=315.0,
        taxes=301.0,
        earned_income_tax_credit=0.0,
        child_care_tax_credit=0.0,
        child_tax_credit=0.0,
        hourly_self_sufficiency_wage=hourly_wage,
        monthly_self_sufficiency_wage=1943.0,
        annual_self_sufficiency_wage=23314.0,
        emergency_savings=48.0,
        miscellaneous_is_secondary=misc_bool,
        health_care_is_secondary=False,
        analysis_is_secondary=False,
    )
    return test_sss


def test_get_db_file():
    """Set both the default and testing database files."""
    with open(config_file) as f:
        config_data = json.load(f)

    default_db_file = os.path.expanduser(config_data.get("default_db_file"))
    testing_db_file = os.path.expanduser(config_data.get("test_db_file"))

    assert default_db_file == get_db_file()
    assert testing_db_file == get_db_file(testing=True)


def test_base_repr():
    test_report = report_obj()

    expected_repr = "<Report(2022, WA, full, June, 2021, 2023-04-14 00:00:00, foo)>"
    assert str(test_report) == expected_repr


def test_isclose_class():
    test_report = report_obj()
    test_geoid = geoid_obj()

    assert not test_report.isclose(test_geoid)


def test_isclose_int():
    test_obj1 = report_obj(year=5)
    test_obj2 = report_obj(year=5.0)
    assert not test_obj1.isclose(test_obj2)

    test_obj3 = report_obj(year=5)
    assert test_obj1.isclose(test_obj3)

    test_obj4 = report_obj(year=3)
    assert not test_obj1.isclose(test_obj4)

    test_obj5 = report_obj(year=None)
    assert not test_obj1.isclose(test_obj5)

    test_obj6 = report_obj(year=None)
    assert test_obj5.isclose(test_obj6)


def test_isclose_bool():
    test_obj1 = sss_obj(misc_bool=True)
    test_obj2 = sss_obj(misc_bool=1)
    assert not test_obj1.isclose(test_obj2)

    test_obj3 = sss_obj(misc_bool=True)
    assert test_obj1.isclose(test_obj3)

    test_obj4 = sss_obj(misc_bool=False)

    assert not test_obj1.isclose(test_obj4)


def test_isclose_str(setup_and_teardown_package):
    test_obj1 = report_obj(state="foo")
    test_obj2 = report_obj(state=5.0)
    assert not test_obj1.isclose(test_obj2)

    test_obj3 = report_obj(state="foo")
    assert test_obj1.isclose(test_obj3)

    test_obj4 = report_obj(state="barr")
    assert not test_obj1.isclose(test_obj4)


def test_isclose_date(setup_and_teardown_package):
    test_obj1 = report_obj(date=datetime.datetime(2023, 4, 14))
    test_obj2 = report_obj(date=None)
    assert not test_obj1.isclose(test_obj2)

    test_obj3 = report_obj(date=datetime.datetime(2023, 4, 14))
    assert test_obj1.isclose(test_obj3)

    test_obj4 = report_obj(date=datetime.datetime(2023, 4, 15))
    assert not test_obj1.isclose(test_obj4)


def test_isclose_float():
    test_obj1 = sss_obj(hourly_wage=5.12345)
    test_obj1.tols = {"hourly_self_sufficiency_wage": {"atol": 1e-3, "rtol": 0}}
    test_obj2 = sss_obj(hourly_wage=5.1235)
    assert test_obj1.isclose(test_obj2)

    test_obj3 = sss_obj(hourly_wage=5.12345)
    assert test_obj1.isclose(test_obj3)

    test_obj4 = sss_obj(hourly_wage=5.122)
    assert not test_obj1.isclose(test_obj4)

    test_obj5 = sss_obj(hourly_wage=5.12345)
    test_obj6 = sss_obj(hourly_wage=5.12345)
    assert test_obj5.isclose(test_obj6)

    test_obj7 = sss_obj(hourly_wage=(5.12345 + 9e-9))
    assert test_obj5.isclose(test_obj7)

    test_obj8 = sss_obj(hourly_wage=(5.12345 * (1 + 1e-5) + 1.1e-8))
    assert not test_obj5.isclose(test_obj8)


def test_isclose_float_array():
    test_obj1 = sss_obj(hourly_wage=np.array([5.1, 4.2, 3.3]))
    test_obj1.tols = {"hourly_self_sufficiency_wage": {"atol": 1e-3, "rtol": 0}}

    test_obj2 = sss_obj(hourly_wage=np.array([5.1, 4.2, 3.3]))
    assert test_obj1.isclose(test_obj2)

    test_obj3 = sss_obj(hourly_wage=np.array([5.1001, 4.2, 3.3]))
    assert test_obj1.isclose(test_obj3)

    test_obj4 = sss_obj(hourly_wage=np.array([5.101, 4.2, 3.3]))
    assert not test_obj1.isclose(test_obj4)

    test_obj5 = sss_obj(hourly_wage=[5.1, 4.2, 3.3])
    test_obj5.tols = {"hourly_self_sufficiency_wage": {"atol": 1e-3, "rtol": 0}}
    assert not test_obj1.isclose(test_obj5)

    test_obj6 = sss_obj(hourly_wage=[5.1, 4.2, 3.3])
    assert test_obj5.isclose(test_obj6)

    test_obj7 = sss_obj(hourly_wage=[5.1, 4.2001, 3.3])
    assert test_obj5.isclose(test_obj7)

    test_obj8 = sss_obj(hourly_wage=[5.1, 4.202, 3.3])
    assert not test_obj5.isclose(test_obj8)


def test_version():
    # this just exercises the version code in `__init__.py`

    assert sss.__version__ is not None
