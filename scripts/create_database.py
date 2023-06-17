#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Script for creating the tables."""

import argparse
from sss import base

parser = argparse.ArgumentParser(description="Create the SSS database")

sss_declare = base.DeclarativeDB()
# then we call the create table function
sss_declare.create_tables()
