#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for creating the tables
"""

import argparse
from sss.city import city_to_db
from sss.base import default_db_file

# creating parser object 
parser = argparse.ArgumentParser(description = "Creating the CITY database")

# defining arguements for the parser object
parser.add_argument("data_path", type = str,
                    help = "Enter path name of the city data excelsheet, so the data can be entered into the city table")

parser.add_argument("year", type = int,
                    help = "Enter the year the population data was collected, so the data can be entered into the city table")

parser.add_argument("-d","--db_file", type = str,
                    help = "Enter the database file that the data should be put in",
                    default=default_db_file)

args = parser.parse_args()

# call the function with arguments
city_to_db(args.data_path, args.year, db_file=args.db_file)

