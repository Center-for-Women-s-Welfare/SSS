#! /usr/bin/env python
"""Script for entering data into geoid table."""

import argparse

from sss.geoid import geoid_to_db

# creating parser object
parser = argparse.ArgumentParser(description="Creating the Geo indentifier database")

# defining arguements for the parser object
parser.add_argument(
    "county_table",
    type=str,
    help="Enter path name of the county table including FIPS code",
)

parser.add_argument("cpi_table", type=str, help="Enter path the cpi region table")

args = parser.parse_args()

# call the function with arguments
geoid_to_db(args.county_table, args.cpi_table)
