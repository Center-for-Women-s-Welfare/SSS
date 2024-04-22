# library for reading Excel files
import openpyxl
import SSSnippet
import easygui


# path to excel data file
INPUT_XLSX_PATH = easygui.fileopenbox("Choose the Excel data file", "Excel Data", "", ["*.xlsx"])

# create path/filename for indesign snippet
id_filename = easygui.filesavebox("Choose the ID snippet file", "InDesign Table File", "output.idms")

TABLE_1_COLS = ["a", "app", "aii", "aps", "aps"]   # data columns to pull for first table
TABLE_2_COLS = ["ast", "aips", "2ip", "2ps", "2ps"]  # data columns to pull for second table

# create helper object to do the real work
id_outfile = SSSnippet.Snippet4ID(id_filename)
# tell the help which columns to use
id_outfile.table1_columns = TABLE_1_COLS
id_outfile.table2_columns = TABLE_2_COLS

# open the Excel file
xlwb = openpyxl.load_workbook(INPUT_XLSX_PATH, True, keep_vba=False)
# find the county data sheet
county_sheet = xlwb["By County"]

# keep adding tables until "append_table" returns false
county_number = 1
while county_number < 2000 and id_outfile.append_table(county_sheet):
    county_number += 1

# close out the files, etc.
id_outfile.finish()
