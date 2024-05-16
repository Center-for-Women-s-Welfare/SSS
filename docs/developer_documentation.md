# Developer documentation

## Modifying the code or documentation

This is for changes that do not include schema changes. For schema changes see [below](#updating-the-database-schema).

Be sure to do all your work on a git branch off of main.

1. First, make sure you are in the SSS folder. If the SSS folder is in your home
directory, you can get there by running `cd` to get to your home directory followed by
`cd SSS`.
2. run `git pull` to get the latest code onto your machine
3. Make your changes.
4. Run `pip install .` to reinstall the package (unless you did a developer install
using the `-e` flag to `pip install` in which case the installation always includes
your latest changes).
5. Run `pytest` to check that all the tests pass. Fix any tests that fail. Reinstall
the package as needed to use the new code (see step 4 above).
6. Add new tests as required to cover your changes and run them using `pytest`.
See the test files in the `tests` folder for examples. Reinstall the package as needed
to use the new code (see step 4 above).
7. Make sure that you have `pre-commit` installed (run `pre-commit install` in the
top level `sss` directory) to prevent committing code that does not follow our style.
8. Add and commit your changes to git. Push your commits to github.
9. Create a pull request on github to run all the continuous integration checks and to
ask for a code review. Fix any errors in the continuous integration checks. When all the
checks pass and you get an approving review, your changes can be integrated into main
via the pull request.


## Updating the database schema

Be sure to do all your work on a git branch off of main.

### Adding or changing columns in an existing table

1. Update the table definition in the python file. Table definitions are class
definitions that detail the columns (names, types, primary keys etc.).
2. Update any methods and/or scripts that interact with the table to account for your
changes.
3. Run `alembic revision --autogenerate -m '<version description>'`, replacing
`<version description>` with a few words describing the change you're making. This will
create a new alembic revision file under the `alembic` directory in the repository that
will reflect the changes to the database schema you just introduced. Inspect the
resulting file carefully -- alembic's autogeneration is very clever but it's certainly
not perfect. It tends to make more mistakes with table or column alterations than with
table creations.
4. Run `alembic upgrade head` to apply your schema changes and run `pip install .` to
reinstall the package (unless you did a developer install using the `-e` flag to
`pip install` in which case the installation always includes your latest changes).
5. Run `pytest` to check that all the tests pass. Fix any tests that fail. Reinstall
the package as needed to use the new code (see step 4 above).
6. Add new tests as required to cover your changes and run them using `pytest`.
See the test files in the `tests` folder for examples. Reinstall the package as needed
to use the new code (see step 4 above).
7. Make sure that you have `pre-commit` installed (run `pre-commit install` in the
top level `sss` directory) to prevent committing code that does not follow our style.
8. Add and commit your changes to git, including the alembic version files that was
created. Push your commits to github.
9. Create a pull request on github to run all the continuous integration checks and to
ask for a code review. Fix any errors in the continuous integration checks. When all the
checks pass and you get an approving review, your changes can be integrated into main
via the pull request.

### Adding a table

1. If appropriate, create a new python file under the `sss` directory. In rare cases it
may make sense to define the table in an existing python file.
2. Create the table defintion. You can see some example table definitions in
`sss_table.py` or `geoid.py`. Tables are defined as classes and their names should be in
camel case (capital letters for the start of each word, lower case letters for the rest
of the word, no underscores). The `__tablename__` attribute is the name the table will
have in the sql database. It should be all lower case with underscores between words.
2. Add an import of your new table class to the `__init__.py` file similar to the
existing imports in that file.
3. Add methods and scripts as appropriate to interact with the new table. See the
methods in `sss_table.py`, `geoid.py` and `puma.py` for examples. Script examples are
in the `scripts` folders.
4. Run `alembic revision --autogenerate -m '<version description>'`, replacing
`<version description>` with a few words describing the change you're making. This will
create a new alembic revision file under the `alembic` directory in the repository that
will reflect the changes to the database schema you just introduced. Inspect the
resulting file carefully -- alembic's autogeneration is very clever but it's certainly
not perfect. It tends to make more mistakes with table or column alterations than with
table creations.
5. Run `alembic upgrade head` to apply your schema changes and run `pip install .` to
reinstall the package (unless you did a developer install using the `-e` flag to
`pip install` in which case the installation always includes your latest changes).
6. Run `pytest` to check that all the tests pass. Fix any tests that fail. Reinstall
the package as needed to use the new code (see step 5 above).
7. Add new tests as required to cover your changes and run them using `pytest`. If you
created a python file for your changes, create a new test file to contain tests for your
new table. See the test files in the `tests` folder for examples. Reinstall the package
as needed to use the new code (see step 5 above).
8. Make sure that you have `pre-commit` installed (run `pre-commit install` in the
top level `sss` directory) to prevent committing code that does not follow our style.
9. Add and commit your changes to git, including the alembic version files that was
created. Push your commits to github.
10. Create a pull request on github to run all the continuous integration checks and to
ask for a code review. Fix any errors in the continuous integration checks. When all the
checks pass and you get an approving review, your changes can be integrated into main
via the pull request.
