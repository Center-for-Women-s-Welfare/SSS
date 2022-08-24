#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for creating the tables
"""

import argparse
from sss.geoid import geoid_to_db
from sss.base import default_db_file

# creating parser object 
parser = argparse.ArgumentParser(description = "Creating the Geo indentifier database")

# defining arguements for the parser object
parser.add_argument("county_table", type = str,
                    help = "Enter path name of the county table including FIPS code")

parser.add_argument("cpi_table", type = str,
                    help = "Enter path the cpi region table")

parser.add_argument("-d","--db_file", type = str,
                    help = "Enter the database file that the data should be put in",
                    default=default_db_file)

args = parser.parse_args()

# call the function with arguments
geoid_to_db(args.county_table, args.cpi_table, db_file=args.db_file)