"""Retrieve database files."""
import json
import os

from sss.base import config_file, get_db_file


def test_get_db_file():
    """Set both the default and testing database files."""
    with open(config_file) as f:
        config_data = json.load(f)

    default_db_file = os.path.expanduser(config_data.get("default_db_file"))
    testing_db_file = os.path.expanduser(config_data.get("test_db_file"))

    assert default_db_file == get_db_file()
    assert testing_db_file == get_db_file(testing=True)
