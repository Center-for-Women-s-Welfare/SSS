#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scipt for creating the primary table

"""

import argparse

from sss.sss_table import data_folder_to_database
from sss.base import db_url

# creating parser object 
parser = argparse.ArgumentParser(description = "Creating the SSS database")

#defining arguements for the parser object
parser.add_argument("data_folder", type = str,
                    help = "Enter path name that contains the SSS data, so it can be entered into table")

parser.add_argument("-d","--db_url", type = str,
                    help = "Enter the database url that the data should be put in",
                    default=db_url)

args = parser.parse_args()
data_folder_to_database(args.data_folder, db_url=args.db_url)
    


