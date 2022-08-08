# Self-Sufficiency Standard Database

## Background
[The Self-Sufficiency Standard](https://selfsufficiencystandard.org/)(SSS) was created by the Center of Women's Welfare (CWW) at the University of Washington as an alterantive to the Official Poverty Measure (OPM). The Self-Sufficiency Standard data is spread across the CWW website and this repository creates a database to hold the Self-Sufficiency Standard data. 

## Setting Up Computer
It's important to set up your machine these [instructions](https://neurohackademy.org/setup/).

## Cloning the Repository
With your machine set up, we recommend working with your terminal to clone the repository. All the following instructions will be ran exclusively in the terminal. 

First, you would want to choose the directory that is hosting the code. You can use `ls` to list the folders in the current directory and then use `cd [directory_path]` to enter the directory you want to host the repository.

Next, you would clone the repository using the following command `git clone https://github.com/Center-for-Women-s-Welfare/SSS.git`. 

## Creating the Conda Environment
Now that you are in the repository folder, you would want to create your conda environment using the sss.yml file. To do so, you would use `conda env create -f sss.yml`.

If you want to add or remove a package, add it to the yaml file and then run: `conda env update -f <path_to_yaml_file> --prune`. 

If you have a problem and need to start fresh, you can delete the environment using: `conda remove --name <env_name> --all` (then you can re-make it with the first command). 

After we have created the environment, you will type `conda activate sss` to ensure we working in the conda environment that contains all the dependencies that were included in the sss.yml file.

## Install Packages
From there, you want to install the repository as a package, using the command `pip install .`

## Creating the database
It is important to understand that **this is meant to be done once**. To create the database we would call `./scripts/create_database.py` in our terminal. For our database, **our primary keys are the family_type, state, place, year, and analysis_type**. 

## Inserting data into an already exisiting database
To insert data into the database, you would do so with the following `./scripts/data_to_primary.py [path name]`. It is important to note that you are passing a path name that points to a folder that witholds the Self-Sufficiency Standard data. To have the full data (as of August 2022), it must be a folder containing 144 files of the SSS data from 2017-2022, excluding the following files NYC2018_SSS_Full.xlsx, NYC2021_SSS_Full.xlsx, OR2021_SSS_Full.xlsx_. These files are exlcuded becasue they contain repeat information and they do not have unique IDs. It is also important to note that data being inserted into the database must be a new XLSB or XLSX file containing the Self-Sufficiency Standard (SSS). New data is referring to the fact that we are not inserting a file that do not contain repeated primary keys.  
