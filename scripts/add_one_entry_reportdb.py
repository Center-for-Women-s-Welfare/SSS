#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Script for creating the tables."""

import argparse
from sss.report import add_one_entry_reportdb
from datetime import date

# creating parser object
parser = argparse.ArgumentParser(description="Creating the report database")

# defining arguements for the parser object
parser.add_argument("year", type=int, help="Enter year of the record")

parser.add_argument("state", type=str, help="Enter state name")

parser.add_argument("analysis_type", type=str, help="Enter analysis type")

parser.add_argument("cpi_month", type=str, help="Enter month e.g. May")

parser.add_argument("cpi_year", type=int, help="Enter year of CPI report")

parser.add_argument(
    "update_date", type=date, help="update date, the format is date(2021,6,22)"
)

parser.add_argument("update_person", type=str, help="who update the report")

args = parser.parse_args()

# call the function with arguments
add_one_entry_reportdb(
    args.year,
    args.state,
    args.analysis_type,
    args.cpi_month,
    args.cpi_year,
    args.update_date,
    args.update_person)
