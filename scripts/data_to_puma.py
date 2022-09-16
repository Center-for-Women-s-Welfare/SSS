#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for creating the tables
"""

import argparse
from sss.puma import puma_to_db
from sss.base import default_db_file

# creating parser object 
parser = argparse.ArgumentParser(description = "Creating the PUMA database")

# defining arguements for the parser object
parser.add_argument("puma_folder", type = str,
                    help = "Enter file or folder name that contains the PUMA data so "
                    "the data can be entered into the PUMA table")

parser.add_argument("nyc_wa_path", type = str,
                    help = "Enter path name of the file with the place breakdown for NYC and WA, so the data can be entered into the PUMA table")

parser.add_argument("year", type = int,
                    help = "Enter the year the PUMA data was collected so the data can be entered into the PUMA table")

parser.add_argument("-d","--db_file", type = str,
                    help = "Enter the database file that the data should be put in",
                    default=default_db_file)

args = parser.parse_args()

# call the function with arguments, may need to add quotation marks for arguments
puma_to_db(args.puma_folder, args.nyc_wa_path, args.year, db_file=args.db_file)
