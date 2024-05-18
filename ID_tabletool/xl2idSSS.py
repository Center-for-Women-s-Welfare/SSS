"""
Create an InDesign snippet file containing formatted tables from Excel data.

1) Asks for an 2024 format Excel file (.xlsx) of self sustainability data.
2) Asks for a filename for the InDesign snippet file (XML format).
3) Creates an InDesign snippet file that contains a table
   for each county in the Excel file.

Primarily the helper class Snippet4ID is used to iterate through the Excel file.
There is a tight correspondence between this code and
the format of the Excel tables and the InDesign snippets.
"""

# library for reading Excel files
import openpyxl
import SSSnippet
import easygui


# path to excel data file
INPUT_XLSX_PATH = easygui.fileopenbox(
    "Choose the Excel data file", "Excel Data", "", ["*.xlsx"]
)

# create path/filename for indesign snippet
id_filename = easygui.filesavebox(
    "Choose the ID snippet file", "InDesign Table File", "output.idms"
)

# create helper object to do the real work
id_outfile = SSSnippet.Snippet4ID(id_filename)

TABLE_COLS = [
    "a",
    "ap",
    "aip",
    "aps",
    "ast",
    "2ip",
    "2ps",
]  # data columns to pull for first table
id_outfile.table1_columns = TABLE_COLS

# open the Excel file
xlwb = openpyxl.load_workbook(INPUT_XLSX_PATH, True, keep_vba=False)
# find the county data sheet
county_sheet = xlwb["By County"]

# keep adding tables until "append_table" returns false
county_number = 1
while county_number < 8 and id_outfile.append_table(county_sheet):
    county_number += 1

# close out the files, etc.
id_outfile.finish()
