#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scipt for creating the primary table

"""

import argparse

from sss.sss_table import data_folder_to_database
from sss.base import default_db_file

# creating parser object 
parser = argparse.ArgumentParser(description = "Add file(s) to the SSS database")

#defining arguements for the parser object
parser.add_argument("data_folder", type = str,
                    help = "Enter path name that contains the SSS data, so it can be entered into table")

parser.add_argument("-d","--db_file", type = str,
                    help = "Enter the database file that the data should be put in",
                    default=default_db_file)

args = parser.parse_args()
data_folder_to_database(args.data_folder, db_file=args.db_file)
    


