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

## Creating the database configuration file
- In the terminal, ensure that you are in your home directory by running `cd`.
- run `mkdir .sss` to make a new folder in your home directory called `.sss`. Since it
  starts with a dot it will not show up when you run `ls`, but you can see that it is
  there by running `ls -a`.
- run `cd .sss` to change directories into the new folder you made.
- run `nano sss_config.json` to create a new file called `sss_config.json` and open it
  in the nano text editor. You can also make and edit this file with any other text
  editor (e.g. vscode) but make sure it is named `sss_config.json` and it is placed in
  the `.sss` folder nested inside your home directory.
- edit the file to look like this, with `<<<path-to-dbfile>>>` replaced with the full
  path (including the file name) on your machine to the database file and
  `<<<path-to-test-dbfile>>>` replaced with the full path (including a file name) on your
  machine to a location where a test database file can be created (one reasonable option
  is a file named `test_sss.sqlite` inside the top-level folder for the sss package):
	```
	{
	"default_db_file": "<<<path-to-dbfile>>>",
	"test_db_file": "<<<path-to-test-dbfile>>>"
	}
	```
- Save the file by hitting `control o` (or maybe `control shift o` if that doesn't work)
then hitting enter to confirm the file name and then  exit the nano editor by hitting `control x` (or maybe `control shift x`).
