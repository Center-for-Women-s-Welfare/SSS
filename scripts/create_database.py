#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for creating the tables

"""

import argparse
from sss import base

parser = argparse.ArgumentParser(description = "Creating the SSS database")

parser.add_argument("-d","--db_file", type = str,
                    help = "Enter the database file that the data should be put in",
                    default=base.db_file)

args = parser.parse_args()


sss_declare = base.DeclarativeDB(args.db_file)
# then we call the create table function 
sss_declare.create_tables()
