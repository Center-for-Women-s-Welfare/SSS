
import os
import warnings

import pytest

from sss import base, sss_table, city, geoid, puma, report
from sss.data import DATA_PATH


@pytest.fixture(autouse=True, scope="session")
def setup_and_teardown_package(tmp_path_factory):

    sss_declare = base.DeclarativeDB(testing=True)

    # then we call the create table function
    sss_declare.create_tables()

    # we fill each table with appropriate data
    sss_table.data_folder_to_database(os.path.join(
        DATA_PATH, "sss_data"), testing=True)

    # fill city table
    city.city_to_db(
        os.path.join(
            DATA_PATH,
            "city_data",
            "2020_PopulationDatabyCity_20220804_Ama.xlsx"),
        2021,
        testing=True)

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "Unknown extension is not supported and will be removed"
        )
        # fill geoid table
        geoid.geoid_to_db(
            os.path.join(
                DATA_PATH,
                "geoid_data",
                "SSScounty-place-list_20220720.xlsx"),
            os.path.join(
                DATA_PATH,
                "geoid_data",
                "StateAbbreviation_Regions_07192022_AKu.xlsx"),
            testing=True
        )

    # fill puma table
    puma.puma_to_db(
        os.path.join(DATA_PATH, "puma_data", "puma_text"),
        2021,
        os.path.join(DATA_PATH, "puma_data", "SSSplaces_NY&WA_PUMAcode.xlsx"),
        testing=True
    )

    # fill report table
    report.report_to_db(
        os.path.join(
            DATA_PATH,
            "report_data",
            "Year_Type_SSS_CPI month year_20220715_DBu.xlsx"),
        testing=True
    )

    yield sss_declare

    sss_declare.drop_tables()
