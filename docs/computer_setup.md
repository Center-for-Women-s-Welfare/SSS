# Computer Setup
How to set up your system, environment, and upload file(s) into the database

## Setting up operating system
Make sure you have an up-to-date web browser. Follow the directions [here] (https://docs.microsoft.com/en-us/windows/wsl/install) to set up a bash shell, git, and python 3 (please set up all three). (add miniconda)
* Run as administrator 
	*  If using cmd, right-click on the program and click “Run as Administrator”
* Skip distribution

Here is some basic info about each of the programs: 
* Bash shell
	The bash shell is the interface between the user (you) and the operating system. It is a command line interface shell program extensively used in Linux and macOs operating systems. Bash is used when users want to control their computer without having to navigate menus, options, and windows while interacting in your computer. For example, if you want to quickly create, edit, or delete multiple files, it’s easier to use Bash instead of finding each file by pointing and clicking on multiple directories.
	
	Basic command lines to interact with bash:
	* ls: list directory contents. The ls command allows you to quickly view all files within a specified directory.
	* pwd: print working directory you are in. If you want to know the exact directory you are working within, then pwd will tell you. 
	* cd: change directory you are in.
	* exit: exit out of the directory. This command will close a terminal window, and end the execution of a shell script. 

* Git
	Git is a version control system that lets you track who made changes to what and when on github.com. It also makes collaboration easier, allowing changes by multiple people to all be merged into one source. You can access the git via command line (terminal) or a desktop app that has a GUI, such as GitKraken. 

* GitHub
	* Github is a software that runs locally on your computer and your files and their history are stored on your computer. Having a centrally located place to upload files and make changes and download changes from others enables you to collaborate more easily with other developers. 

	
* Python 
	* Python is a high-level, general-purpose, interpreted computer programming language. It is widely applied in many fields to build solutions for web applications, software development, data analysis and conducting AI techniques. Python has two major versions: 2x was released in 2000 and the latest version 3x was released in 2008. It’s recommended to use the latest version 3 in projects.

## Opening up a terminal 
*For Mac devices:*
Click the Launchpad icon in the Dock, type Terminal in the search field, then click Terminal. In the Finder, open the /Applications/Utilities folder, then double-click Terminal.

*For Windows devices:*
Press the Start taskbar button. Select All apps on the Start menu. Scroll down the Start menu to the Windows Terminal app or Command Prompt app (Windows Terminal is a little nicer if you have it but not required) shown directly below. Then click Windows Terminal or Command Prompt there to open it.


## Setting up environment 
* Download miniconda from [here](https://docs.conda.io/en/latest/miniconda.html) (click the first Linux link)
	* If using Windows Subsystem for Linux on Windows, use the Linux installer
* Install miniconda
	* Change directories to the folder where you downloaded miniconda
	* Type `bash`
	* Type `cd /Downloads` (type ls to see whether the Miniconda is in the working directory, and how to type that folder name)
	* Type `bash [miniconda file name]` (e.g., Miniconda3) 
* Answer yes to all the questions 
	* Tip: press the spacebar to go through the terms and conditions more quickly
* Clone the repository in the terminal: 
	* Change directories to your home directory
		* Type `cd`
	* Type `git clone https://github.com/Center-for-Women-s-Welfare/SSS.git`
	* The default directory when you open a terminal is usually under the user, so use cd to find the working directory you are in 
	* Type `cd ..` to navigate back to the previous working directory in the last terminal session 
* Change directories into the new folder you created
	* Type `cd SSS`
* Create a conda environment for this work
	* Type `conda env create -f sss.yml`
* Activate this environment
	* Type `conda activate sss`
	* To confirm you are in the sss environment, the parentheses at the very beginning of the line should say (sss)
* Install the sss package
	* Type `pip install .`
	* *Dot means install the current directory package. So, it’s important that you are in the sss directory*

## Changing your directory to sss
Change the directory into the working directory that contains the repository you just cloned:
* Type `cd SSS`

## Creating the database
* Initialize the database (this creates an empty database)
	* Type `python ./scripts/create_database.py`
	* *Once you create the database, you will not need to do this again. When testing, however, you may need to remove it and run it again.*
* To confirm the script ran successfully:
	* Type `ls`
	* *If the file “sss.sqlite” is present, the create_database.py script did its job
* To delete the file
	* Type `rm sss.sqlite`

## Running the script:
* Call to insert data from a file or folder of interest, into an already existing primary_table database (this cannot be done unless the database has already been initialized):
	* Type `python ./scripts/data_to_primary.py [path name]`
* To find the path name (add)
	* *NYC2018_SSS_Full.xlsx and NYC2021_SSS_Full.xlsx are omitted from the data folder that creates the primary table because they have repeating information that is already in the database*
