#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for creating the tables
"""

import argparse
from sss.puma import puma_to_db
from sss.base import db_url

# creating parser object 
parser = argparse.ArgumentParser(description = "Creating the PUMA database")

# defining arguements for the parser object
parser.add_argument("puma_folder", type = str,
                    help = "Enter path name that contains the PUMA data so the data can be entered into the PUMA table")

parser.add_argument("nyc_wa_path", type = str,
                    help = "Enter path name of the file with the place breakdown for NYC and WA, so the data can be entered into the PUMA table")

parser.add_argument("year", type = int,
                    help = "Enter the year the PUMA data was collected so the data can be entered into the PUMA table")

parser.add_argument("-d","--db_url", type = str,
                    help = "Enter the database url that the data should be put in",
                    default=db_url)

args = parser.parse_args()

# call the function with arguments, may need to add quotation marks for arguments
puma_to_db(args.puma_folder, args.nyc_wa_path, args.year, db_url=args.db_url)
