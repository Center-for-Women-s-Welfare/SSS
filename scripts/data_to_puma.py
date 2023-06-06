#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Script for entering data into the puma table."""

import argparse
from sss.puma import puma_to_db

# creating parser object
parser = argparse.ArgumentParser(description="Creating the PUMA database")

# defining arguements for the parser object
parser.add_argument("puma_folder", type=str,
                    help="Enter file or folder name that contains the PUMA data so "
                    "the data can be entered into the PUMA table")

parser.add_argument("year", type=int,
                    help="Enter the year the PUMA data was collected"
                    "so the data can be entered into the PUMA table")

parser.add_argument("nyc_wa_path", type=str,
                    help="Enter path name of the file with the place breakdown for NYC and WA,"
                    "so the data can be entered into the PUMA table")

args = parser.parse_args()

# call the function with arguments, may need to add quotation marks for arguments
puma_to_db(args.puma_folder, args.year, args.nyc_wa_path)
