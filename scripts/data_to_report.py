#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Script for creating the tables."""

import argparse
from sss.report import report_to_db

# creating parser object
parser = argparse.ArgumentParser(description="Creating the report database")

# defining arguements for the parser object
parser.add_argument("path", type=str, help="Enter path name of the report excel file")

args = parser.parse_args()

# call the function with arguments
report_to_db(args.path)
