#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script for creating the tables

"""

import argparse
from sss import base

parser = argparse.ArgumentParser(description = "Creating the SSS database")

parser.add_argument("-d","--db_url", type = str,
                    help = "Enter the database url that the data should be put in",
                    default=base.db_url)

args = parser.parse_args()


sss_declare = base.DeclarativeDB(args.db_url)
# then we call the create table function 
sss_declare.create_tables()
