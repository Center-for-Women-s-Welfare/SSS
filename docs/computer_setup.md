# Computer Setup
How to set up your system, environment, and upload file(s) into the database

## Setting up operating system
Make sure you have an up-to-date web browser. Follow the directions
[here](https://docs.microsoft.com/en-us/windows/wsl/install) to set up a bash shell,
git, and python 3. (add miniconda)
- Run as administrator 
	-  If using cmd, right-click on the program and click “Run as Administrator”
- Skip distribution

Here is some basic info about each of the programs: 
- Bash shell
	The bash shell is an interface between the user (you) and the operating system.
	It is a command line interface extensively used in Linux and MacOSX operating
	systems. Bash (and other command line interfaces) are used when users want to
	control their computer programmatically. Command line interfaces are a much older
	way to interact with computers and most people are much more familiar with the newer
	graphical user interfaces (GUIs), which allow users to control their computer by
	using menus, options, and windows. GUIs are a fantastic way for users to interact
	with computers, but they do not work very well when we want to start automatting
	complex tasks. If you want to do the same (complicated) thing to dozens or hundreds
	of files it becomes slow, tedious and error prone to do that using a GUI. For those
	kinds of tasks, a command line interface is much more appropriate. Command line
	interfaces are interacted with exclusively via a keyboard (they were invented
	before mice existed!):
	
	- Here are some commonly used commands in the Bash terminal:
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

- Git
	Git is a version control system that lets you track who made changes to what files
	and at what time. A folder of code that is tracked together by git is called a
	repository. Git runs locally on your computer and keeps track of the changes you
	make and allows you to see all the past changes you and others have made. It also
	makes collaboration easier by making it easy to coordinate changes by multiple
	people. You can access the git via command line (terminal) or a desktop app that
	has a GUI, such as GitKraken (strongly recommended!). 

- GitHub
	- Github is a website that provides hosting of git repositories and adds some very
	helpful collaboration tools as well. It provides a centrally located, always online,
	access point for git repositories.
	
- Python 
	- Python is a high-level, general-purpose, interpreted computer programming
	language. It is widely applied in many fields and it is a relatively easy
	programming language to learn. Python is particularly good at making it easy to
	leverage code libraries written by other programmers and there is a very large,
	robust python open source community.

## Opening up a terminal 
- **On Mac:**
Click the Launchpad icon in the Dock, type Terminal in the search field, then click
Terminal. In the Finder, open the /Applications/Utilities folder, then double-click
Terminal.

- **On Windows:**
Press the Start taskbar button. Select All apps on the Start menu. Scroll down the
Start menu to the Windows Terminal app or Command Prompt app (Windows Terminal is a
little nicer if you have it but not required) shown directly below. Then click Windows
Terminal or Command Prompt there to open it.

## Setting up environment 
- Download miniconda from [here](https://docs.conda.io/en/latest/miniconda.html)
	- If using Windows Subsystem for Linux on Windows, use the Linux installer
	(the first Linux link).
- Install miniconda
	- Change directories to the folder where you downloaded miniconda
	- run `bash`
	- run `cd /Downloads`
	- run `ls` to see whether Miniconda is in the working directory, and exactly how
	the folder name is spelled (including capitalization)
	- run `bash [miniconda file name]` (e.g., Miniconda3) 
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
	correct conda environment. Anytime you restart your terminal you will need to
	re-activate the conda environment using the command above.
- Install the sss package
	- run `pip install .` (including the dot!)
	- The dot means install the current directory package. This will only work if you
	are inside the `SSS` directory (which contais the `setup.py` file)

## Creating the database
- Initialize the database (this creates an empty database)
	- run `python ./scripts/create_database.py`
	- In normal use, once you create the database, you will not need to do this again.
	When testing, however, you may need to remove it and run it again.
- To confirm the script ran successfully:
	- rum `ls`
	- If the file "sss.sqlite" is present, the create_database.py script did its job
- To delete the file
	- run `rm sss.sqlite`

## Running the script:

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
	`ls` to step folder by folder until we find the files you want. **NOTE:** if you
	spaces in names of your folders (which is common in Windows), we need to tell the
	terminal that those spaces are part of the folder name, not marking a new parameter
	to pass to `ls`. We can do that either by putting the entire path in quotation marks
	or by "delimiting" the space by placing a backslash (`\`) directly before the space.
	The terminal will actually add this delimiter for you if you use tab complete, so
	you can start typing the name of the folder you want and once you have enough
	characters to make it so that only one folder can match what you are typing, you can
	hit tab and it will put the full folder name in for you. If you hit tab and nothing
	happens, it probably means there are more than one option that matches so you need
	to type some more characters (or it could mean there are no matches if you
	misspelled something).
	- Once you have found the file you want, the path you are passing to `ls` is the
	path name you will pass to the command in the next step.

- Call to insert data from a file or folder of interest, into an already existing
database (this cannot be done unless the database has already been initialized). If you
pass a file name here, the data from that file will be inserted into the database. If
you pass a folder, **all** the files from that folder will be inserted (this could take
awhile if there are a lot of files):
	- Type `python ./scripts/data_to_primary.py [path name]`
	- **Note:** we typically omit NYC2018_SSS_Full.xlsx and NYC2021_SSS_Full.xlsx from
	the data folder used to fill the database because they have repeating information
	that is already in other files.
