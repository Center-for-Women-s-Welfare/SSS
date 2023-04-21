![](https://github.com/Center-for-Women-s-Welfare/SSS/actions/workflows/tests.yml/badge.svg)
[![codecov](https://codecov.io/gh/Center-for-Women-s-Welfare/SSS/branch/main/graph/badge.svg?token=ZRL342TOLY)](https://codecov.io/gh/Center-for-Women-s-Welfare/SSS)

# Self-Sufficiency Standard Database

## Background
[The Self-Sufficiency Standard](https://selfsufficiencystandard.org/)(SSS) was created
by the Center of Women's Welfare (CWW) at the University of Washington as an alternative
to the Official Poverty Measure (OPM). The Self-Sufficiency Standard data is spread
across the CWW website and this repository creates a database to hold the
Self-Sufficiency Standard data. 

## Computer setup
See directions [here](docs/computer_setup.md) for detailed instructions for users who
are not familiar with working with bash, git and python. These instructions also cover
installation, creating the database and adding data to the database in more detail than
the brief sections below.

## Installation
Clone this repository using
```git clone https://github.com/Center-for-Women-s-Welfare/SSS.git```, change
directories into the newly created `SSS` folder and install the package using
```pip install .``` (including the dot). Note that this will attempt to automatically
install any missing dependencies. If you use conda you might prefer to first install
the dependencies as described in [Dependencies](#dependencies).

To install without dependencies, run `pip install --no-deps`

### Dependencies
If you are using `conda` to manage your environment, you may wish to install the
following packages before installing `sss`:

Required:

* numpy>=1.21
* openpyxl>=3.1.0,!=3.1.1
* pandas>=1.5.0
* pyxlsb>=1.0.8
* setuptools_scm>=7.0.3
* sqlalchemy>=1.4.16

If you want to do development on sss, in addition to the other dependencies
you will need the following packages:

* pytest
* pytest-cov
* coverage
* sphinx
* pypandoc

One way to ensure you have all the needed packages is to use the included
`sss.yaml` file to create a new environment that will
contain all the optional dependencies along with dependencies required for
testing and development (```conda env create -f sss.yml```).
Alternatively, you can specify `dev` when installing sss
(as in `pip install .[dev]`) to install the packages needed for testing
and documentation development.

## Tests
Uses the `pytest` package to execute test suite.
From the source sss directory run ```pytest``` or ```python -m pytest```.

## Creating the Database
In normal use, once you create the database, you will not need to do this again.
When testing, however, you may need to delete it (just delete the sqlite file, with a
file browser or with `rm` in a terminal) and re-make it.

To create the database, use  the `create_database.py` script.
The script takes the optional `-d` parameter for the full path where the database file
should be created. Currently the default is to create a file called `sss.sqlite` in the
working directory.

## Inserting Data
To insert data into the database, use the `data_to_primary.py`, `data_to_city.py` and
`data_to_puma.py` scripts. These scripts take a file or folder containing the data to
upload as an argument and also take the optional `-d` parameter for the full path to
the database file (the default is a file called `sss.sqlite` in the working directory).

- The `data_to_primary.py` script will insert Self-Sufficiency
data into the database. It takes either an excel file or folder as an argument, if a
folder is passed it will read in all the excel files in that folder.
    - To have the full data (as of August 2022), it must be a folder containing 144
    file of the SSS data from 2017-2022, excluding the following files
    NYC2018_SSS_Full.xlsx and NYC2021_SSS_Full.xlsx. These files are exlcuded because
    they contain duplicated information.
- The `data_to_report.py` script will insert data about the SSS reports into the report
table. It takes a single excel file in a specific format as input.
- The `data_to_geoid.py` script will insert data linking the SSS places to FIPS codes
from the census and the CPI regions. It takes two excel files (one for the FIPS info
and one for the CPI region info) in specific formats as input.
- The `data_to_puma.py` script will insert Public Use Microdata Area files from the
census into the database. It can take a file or folder containing the puma files for
multiple states as input. It also requires a single excel file containing the Washington
state and New York City SSS place to census place mappings.
- The `data_to_city.py` script will insert data linking cities to SSS places with
population into the database. It takes a single excel file in a specific format as input.