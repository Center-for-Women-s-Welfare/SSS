# User Documentation

## Creating the database
In normal use, once you create the database, you will not need to do this again.
When testing, however, you may need to delete and it re-make it.

- Initialize the database (this creates an empty database)
	- run `python ./scripts/create_database.py`. This will will create a new
	database file in the location specified in your `~/.sss/sss_config.json` file.
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
	- Type `python ./scripts/data_to_primary.py <path_name>` by
	replacing `<path_name>` with the full path to the file you found above.

	-**Troubleshooting note:** ValueError: data_folder must be a file or folder on this system.
	Solution 1: Insert a \ in front of every space in a file pathway. Shared drives becomes Shared\ drives
	Solution 2: If uploading several files in succession and tabbing up to get the same file path, make sure that the file type is the same.
	If a file is saved as .xlsx and you're uploading .xlsb, you will be thwarted.

	- **Note:** we typically omit NYC2018_SSS_Full.xlsx and NYC2021_SSS_Full.xlsx from
	the data folder used to fill the database because they have repeating information
	that is already in other files.

- There are similar scripts to insert data into the `geoid`, `puma`, `city` and `report`
tables. All those scripts require you to pass at least one file or folder. You can find
out what the script requires as input if you call the script with the `-h` (for help)
flag  (e.g. `python ./scripts/data_to_puma.py -h`). More details about these scripts
are in the README in the "Inserting Data" section.

## Getting code updates

If the code has changed and you need to get the latest version, follow these steps.
- First, make sure you are in the SSS folder
	- you can get there by running `cd` to get to your home directory followed by
	`cd SSS`
- run `git pull` to get the latest code onto your machine
- run `pip install .` to reinstall the package.
- If the structure of the database has changed since you made it, you may need to
delete it and re-make it using the commands [above](#creating-the-database)
