# Computer Setup
How to set up your system, environment, and upload file(s) into the database

## Introduction

To use this package, you will need to use some programs and ways of interacting with
your computer that are unfamiliar to most people. Below we describe a few of the
programs you will be using and interacting with.

- **Bash shell:**
	The bash shell is an interface between the user (you) and the operating system.
	It is a text-based interface, known as a command line, extensively used in Linux
	and MacOSX operating systems. Bash (and other command line interfaces) are used
	when users want to control their computer programmatically. Command line interfaces
	are a much older way to interact with computers and most people are much more
	familiar with the newer graphical user interfaces (GUIs), which allow users to
	control their computer by using menus, options, and windows. GUIs are a fantastic 
	way for users to interact with computers, but they do not work very well when we
	want to start automatting complex tasks. If you want to do the same (complicated)
	thing to dozens or hundreds of files it becomes slow, tedious and error prone to do
	that using a GUI. For those kinds of tasks, a command line interface is much more
	appropriate. Command line interfaces are interacted with exclusively via a keyboard
	(they were invented before mice existed!). 
	
	Note that we will use "bash", "shell", "command line" and "terminal" more or less
	interchangeably in this documentation. There are subtle distinctions but they do
	not matter here.

	When working in a command line interface, it is important to understand the concept
	of the "working directory". When you start the terminal, you are placed into a
	folder (or directory). Typically on a Linux or Mac computer, you start out in your
	"home" directory. Using WSL on Windows, what folder you start out in depends a bit
	on the way you start the terminal. Also, the folder that WSL considers to be your
	"home" directory is a folder made by WSL when you initialize it, not a folder that
	you are familiar with from the Windows side.
	
	The folder you are in at any moment is called your "current directory" or your
	"working directory".  To figure out what directory you are in, you can run `pwd`
	(short for "print working directory") to print out the full path to your working
	directory. To navigate the filesystem, you can call commands to change your
	directory (see `cd` below) or, if you just want to see what is in other folders you
	can print the folders and files they contain without changing your working directory
	(see `ls` below). You can always quickly return to your home directory by calling
	`cd` by itself (with no arguments).

	Commands in bash often take arguments (also called parameters) that control what
	they do. For example, to change directories to a particular folder you would run
	`cd <path_name>` where you would replace `<path_name>` with the full path to the
	folder you'd like to move to. This is often called "passing" an argument to a
	command. These arguments are always separated from the command you are calling
	(and from other arguments -- some commands can take several arguments) with a
	space. Some bash commands can also take optional arguments or "flags" that are
	specified using either one or two dashes before the argument name. For example,
	you can run `ls -l` to have the `ls` command provide more detail (owner, size,
	modification date) about the files and folders it is listing. One dash is used if
	the argument name is a single letter, two dashes are used for longer argument
	names. You can also pass multiple single-letter arguments using one dash, so
	`ls -l -h` can also be written `ls -lh` (the `h` argument makes the file size be
	reported in more human readable units). You will see several examples in the
	instructions below where bash commands are called with arguments.

	Here are some commonly used commands in the Bash terminal:
	- `ls`: list directory contents. The `ls` command allows you to quickly view all
	files within your current working directory (just run `ls`) or any specified
	directory (run `ls <path_name>` by replacing `<path_name>` with the path you are
	interested in).
	- `pwd`: print working directory. This prints the full path to the current
	directory you are working in. 
	- `cd`: change directory. If you run this by itself, it will move you to your "home"
	directory. If you pass either a relative or full path to it (`cd <path_name>`) you
	will move to that path. You can confirm that you moved by running `pwd` and you can
	see what is inside the folder you are currently in by running `ls`.

- **Git:**
	Git is a version control system that lets you track who made changes to what files
	and at what time. A folder of code that is tracked together by git is called a
	repository. Git runs locally on your computer and keeps track of the changes you
	make and allows you to see all the past changes you and others have made. It also
	makes collaboration easier by making it easy to coordinate changes by multiple
	people. You can access the git via command line (terminal) or a desktop app that
	has a GUI, such as GitKraken (strongly recommended!). 

- **GitHub:**
	Github is a website that provides hosting of git repositories, the way that Google
	Drive provides hosting of documents, and adds some very helpful collaboration tools
	as well. It provides a centrally located, always online, access point for git
	repositories.
	
- **Python:** 
	Python is a programming language that prioritizes being human-readable, adaptable
	to many kinds of problems, and easy to write quickly without careful study. It is
	widely used in many fields and it is particularly good at making it easy to
	use code written by other programmers (called "libraries"). As a result, there is a
	very large, robust python open source community.
	- We will use conda (packaged as miniconda or anaconda) to manage our python
	environment and to install all the python libraries we need.

## Opening up a terminal (command line interface)
- **On Mac:**
Click the Launchpad icon in the Dock, type Terminal in the search field, then click
Terminal. Or in the Finder, open the /Applications/Utilities folder, then double-click
Terminal.

- **On Windows:**
Press the Start taskbar button and start typing to search for either the 'Terminal' app
or, if it's not installed, the 'Command prompt' app.

## Setting up your environment

### Setting up Windows subsystem for Linx
If you are working on a Windows computer, follow the directions
[here](https://docs.microsoft.com/en-us/windows/wsl/install) to install and set up the
Windows Subsystem for Linux (WSL). Be sure to follow the links in that page for the
"Best practices for setting up a WSL development environment" to install git (you don't
need the other things mentioned on that page, although Windows Terminal is a nicer
terminal than Command Promp and Visual Studio Code is great if you intend to write
python code).
- You may need to run as administrator if you get permissions errors:
	-  When opening the command prompt from the start menu, right-click on the program
	and click "Run as Administrator".
- Skip distribution
- Now if you start the 'Terminal' or 'Command prompt' app, you can get a bash shell by
running `wsl` (`bash` also appears to work but may be less specific, so we encourage
you to use `wsl`).

### Setting up conda 
- Download miniconda from [here](https://docs.conda.io/en/latest/miniconda.html)
	- If using Windows Subsystem for Linux on Windows, use the Linux installer
	(the first Linux link).
- Install miniconda
	- First we need to change directories to the folder where you downloaded miniconda.
	If it is in your normal Downloads folder, WSL probably will find that folder is at
	`/mnt/c/Users/<username>/Downloads` (where `<username>` should be replaced by your
	username). How to get there will depending on what folder you are put into when you
	start your terminal. To find that out:
		- run `wsl` if you haven't already to get into the bash shell.
		- run `pwd` to find out what your current directory is. If it is
		`/mnt/c/Users/<username>`, you can just run `cd Downloads` to get to the
		correct folder. Otherwise, run `cd /mnt/c/Users/[username]/Downloads`. If you're
		not sure what your username is, you can do this in steps. First run
		`cd /mnt/c/Users/`, then run `ls` to see the usernames. Identify the one you
		want and run `cd <username>/Downloads` replacing `<username>` with the one you
		found.
	- run `ls` to see whether Miniconda is in the directory you just navigated to and
	exactly how the files name is spelled (including capitalization)
	- run `source <miniconda file name>` by replacing `<miniconda file name>` with the file
	name you found with `ls` (e.g. `source Miniconda3`)
- Answer yes to all the questions 
	- Tip: press the spacebar to go through the terms and conditions more quickly
- Clone the repository in the terminal: 
	- Change directories to your home directory by running `cd`
	- run `git clone https://github.com/Center-for-Women-s-Welfare/SSS.git` to get the
	repository onto your computer. This will make a folder called "SSS" with the code
	inside of it.
- Change directories into the new folder you created by running `cd SSS`
- Create a conda environment for this work
	- run `conda env create -f sss.yml`
- Activate this environment
	- run `conda activate sss`
	- When you run this, the parentheses at the very beginning of the line will change
	from showing `(base)` to `(sss)`. This is how you know that you are using the
	correct conda environment. **Anytime you restart your terminal you will need to
	re-activate the conda environment using the command above.**
- Install the sss package
	- run `pip install .` (including the dot!)
	- The dot means install the current directory package. This will only work if you
	are inside the `SSS` directory (which contais the `setup.py` file)
	- **This may need to be re-done if changes are made to the code, see
	[below](#getting-code-updates).**

## Creating the database
In normal use, once you create the database, you will not need to do this again.
When testing, however, you may need to delete and it re-make it.

- Initialize the database (this creates an empty database)
	- run `python ./scripts/create_database.py -d <database_path>` by replacing
	`<database_path>` with a full path to where you want to save the database. The path
	should end with a filename with the `.sqlite` extension. This same path will used
	when you add data to the database. If you do not include the `-d <database_path>`
	the script will create a file called `sss.sqlite` in your working directory.
- To confirm the script ran successfully:
	- run `ls`
	- If the file "sss.sqlite" is present, the create_database.py script did its job
- To delete the file
	- run `rm sss.sqlite` (`rm` is short for "remove")

## Running scripts to add data to the database:

- First, we have to find the correct path name. This is not totally obvious on Windows
using WSL because you can't just use the path to the SSS data files that you find from
your Explorer file browser. Instead we need to find where the SSS files are on your
machine according to the WSL terminal.
	- The way we examine what files are inside a folder in the terminal is using the
	`ls` command. If you run `ls` by itself it will print out all the files that are in
	your current working directory. If you add a path after `ls` it will print the
	files that are inside that path.
	- It seems that the devices and drives under "This PC" in Explorer are placed under
	"/mnt" in the WSL terminal. So start by running `ls /mnt`. That will print out a
	list of folders that will include "c" which is your normal "C://" drive, "wsl" which
	contains system files related to WSL (you don't need to look at anything in here).
	If you have a google drive, it will also be listed in here, we have seen it called
	either "g" or "h".
	- Now we can start digging into these drives to find the SSS files. If the files are
	on google drive, start by running `ls /mnt/g` or `ls /mnt/h` depending on the name
	of the drive you saw in the last step (if instead they are in the C drive, just
	replace the "g" or "h" with "c"). That will list all the folders in your google
	drive.
	- We need to drill down into whichever listed folder contains the SSS data, so
	we will keep appending the next folder name to the end of the path that we pass to
	`ls` to step folder by folder until we find the files you want.
		- **NOTE:** if you have spaces in names of your folders (which is common in
		Windows), we need to tell the terminal that those spaces are part of the folder
		name, not marking a new argument to pass to `ls`. We can do that either by
		putting the entire path in quotation marks or by "delimiting" the space by
		placing a backslash (`\`) directly before the space.
		- **Tab completion**: This is a major time-saver when working in the terminal.
		If you start typing the name of a folder or file, once you have typed enough
		characters to make it so that only one folder or file can match what you have
		typed, you can hit tab and it will put the full folder or file name in for you.
		This is particularly helpful when you have spaces in file names because the
		terminal will add the backslash delimiter for you. If you hit tab and nothing
		happens, it probably means there are more than one option that matches what you
		have types, so you need to type some more characters (or it could mean there
		are no matches if you misspelled something).
	- Once you have found the file you want, the path you are passing to `ls` is the
	path name you will pass to the command in the next step.

- Run the following command to insert data from a file or folder of interest, into an
already existing database (this cannot be done unless the database has already been
initialized). If you pass a file name here, the data from that file will be inserted
into the database. If you pass a folder, **all** the files from that folder will be
inserted (this could take awhile if there are a lot of files):
	- Type `python ./scripts/data_to_primary.py <path_name> -d <database_path>` by
	replacing `<path_name>` with the full path to the file you found above and 
	`<database_path>` with a full path to the database files. The database path will be
	the one you used when you created the database. If you do not include the
	`-d <database_path>` the script will try to add data to a database file called
	`sss.sqlite` in your working directory.

	- **Note:** we typically omit NYC2018_SSS_Full.xlsx and NYC2021_SSS_Full.xlsx from
	the data folder used to fill the database because they have repeating information
	that is already in other files.

- There are similar scripts to insert data into the `geoid`, `puma`, `city` and `report`
tables. All those scripts require you to pass at least one file or folder and accept the
`-d` option to pass the database path. You can find out what the script requires as
input if you call the script with the `-h` (for help) flag 
(e.g. `python ./scripts/data_to_puma.py -h`). More details about these scripts are in
the README in the "Inserting Data" section.

## Getting code updates

If the code has changed and you need to get the latest version, follow these steps.
- First, make sure you are in the SSS folder
	- you can get there by running `cd` to get to your home directory followed by
	`cd SSS`
- run `git pull` to get the latest code onto your machine
- run `pip install .` to reinstall the package.
- If the structure of the database has changed since you made it, you may need to
delete it and re-make it using the commands [above](#creating-the-database)