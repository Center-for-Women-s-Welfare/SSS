#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Scipt for creating the primary table

"""

import argparse

from sss.sss import data_folder_to_database

# creating parser object 
parser = argparse.ArgumentParser(description = "Creating the SSS database")

#defining arguements for the parser object
parser.add_argument("data_folder", type = str,
                    help = "Enter path name that contains the SSS data, so it can be entered into table")

args = parser.parse_args()
data_folder_to_database(args.data_folder)
    


