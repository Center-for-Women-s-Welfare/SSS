# library for reading/writing xml files
import lxml
# library for regular expressions (complex find)
import re

NUM_COLUMNS_READ = 250  # columns of data (family types)


# copy the numeric value into the cells in the snippet
# rowdata = the Excel row with all the data
# prevcell = the table cell in the snippet to the left of our target
# columns = the list of column indices to insert
def copy_numbers(rowdata, prevcell, columns: list, keep_cents: bool):
    # for each column index (e.g. 'a', 'ai', 'ap', 'at')
    for colidx in columns:
        colvalue = rowdata[colidx]  # value in the Excel file in the right column
        if type(colvalue) == str:  # if it's a string, make it a number
            colvalue = float(colvalue)
        if colvalue < 0.0:
            colvalue = "(${:,.0f})".format(-colvalue)
        elif keep_cents:
            colvalue = "${:,.2f}".format(colvalue)
        else:
            colvalue = "${:,.0f}".format(colvalue)
        prevcell = prevcell.getnext()  # move to the correct cell & replace content
        prevcell[0][0][0].text = colvalue  # 1st paragraph - 2nd character range - Content


def sum_tax_amounts(rowdata: list, columns: list, amount_dict):
    for colidx in columns:
        colvalue = rowdata[colidx]  # value in the Excel file in the right column
        if type(colvalue) == str:  # if it's a string, make it a number
            colvalue = float(colvalue)
        if colidx in amount_dict:
            amount_dict[colidx] += colvalue
        else:
            amount_dict[colidx] = colvalue


# complicated code to find the cells in the snippet XML to replace
# rowhead = the row title from the Excel file (e.g. 'Housing')
# root = the root of the XML tree representing one InDesign table snippet
# find the corresponding row in the snippet that matches
def row_label_match(rowhead: str, root):
    xpath = "Cell//Content[.='" + rowhead + "']"
    cell = root.xpath(xpath)
    if len(cell) == 0 and rowhead.find("\n") >= 0:  # newline in row header, just match first line
        rowhead = rowhead.split("\n")[0]
        xpath = "Cell//Content[.='" + rowhead + "']"
        cell = root.xpath(xpath)
    if len(cell) == 0:  # more complex matching for different wording
        xpath = "Cell//Content[starts-with(text(), '" + rowhead + "')]"  # up to Cell
        cell = root.xpath(xpath)
    assert len(cell) == 1, "can't find proper row in InDesign for " + rowhead
    cell = cell[0].getparent().getparent().getparent()
    return cell


# this class does the work of replacing content in the InDesign snippet tables
# to reflect the data pulled from the Excel file
class Snippet4ID:
    # initialize the object
    def __init__(self, idfilename: str):
        # the path to use when generating the InDesign file
        self.id_filename = idfilename
        # open a new file at the location
        self.id_file = open(self.id_filename, "w", encoding="utf-8")
        # copy the "Pretable snippet" into the InDesign file (just copies, no parsing)
        with open('PretableSnippet.xml', encoding="utf-8") as prefixfile:
            prefix_data = prefixfile.read()
            self.id_file.write(prefix_data)
        # close the InDesign file (causes it to write to disk)
        # we open and close it repeatedly
        self.id_file.close()
        # read & parse the table snippet
        self.snippet1_xml = lxml.etree.parse('TableSnippet.xml')
        # get the root of the XML tree representation for the table
        self.snippet1_root = self.snippet1_xml.getroot()
        # start with empty columns (filled out later)
        self.table1_columns = []
        # we create unique IDs for each table, not sure if it's necessary...
        self.defaultTableID = "u777777"
        self.nextTableID = "u" + str(int(self.defaultTableID[1:]) + 1)
        # the row_iterator walks through the Excel file (row by row)
        self.row_iterator = None
        # list of columns summed as tax credits
        self.tax_credits = ["Earned Income Tax Credit (-)", "Child Care Tax Credit (-)", "Child Tax Credit (-)"]

    # table snippet has all IDs in the form u777777______ with some suffix,
    # we change them to u 777777x+n _____ (increment the number part)
    # where x is "1" for table 1 and "2" for table 2
    def new_self_id(self, oldID: str, which: str) -> str:
        if oldID.startswith(self.defaultTableID):
            return self.nextTableID + which + oldID[7:]
        return oldID

    # create new IDs for the table items. Probably not used ?? but we make them unique anyway
    def renumber(self):
        self.nextTableID = "u" + str(int(self.nextTableID[1:]) + 1)
        for child in self.snippet1_root:
            if "Self" in child.attrib:
                newid = self.new_self_id(child.attrib["Self"], "1")
                child.attrib["Self"] = newid

    # county / state / date table header -- only in table 1
    # the Excel file has something like:
    # 'Table 1_x000D_\nThe Self-Sufficiency Standard_x000D_\nfor_x000D_\nAllegany County, MD, 2023'
    # we break this string into the 4 sections, pulling out relevant fields
    def format_head(self, head_cell: str):
        if "_x000D_\n" in head_cell:
            lines = head_cell.split("_x000D_\n")
        elif "_x000d_\n" in head_cell:
            lines = head_cell.split("_x000d_\n")
        else:
            assert False, "Can't split head row" + head_cell

        assert lines[0].startswith("Table"), "Unrecognized format head: " + head_cell
        assert lines[1].endswith("The Self-Sufficiency Standard"), "Unrecognized format head: " + head_cell
        assert lines[2] == "for", "Unrecognized format head: " + head_cell
        # regular expression finds the county name and the State, year
        county_match = re.search(r"^(.+)(,.?\w\w, \d\d\d\d)$", lines[3])
        assert county_match is not None, "Unrecognized format head: " + head_cell
        county_name = county_match.group(1)
        state_etc = county_match.group(2)
        # find the table header cell in the snippet
        x = self.snippet1_root.findall("Cell[@Name='0:0']")
        assert len(x) == 1, "should only find 1 header cell"
        # report our progress
        print("Building table for", county_name, state_etc)
        x[0][0][1][0].text = county_name  # 1st cell - 1st paragraph - 2nd character range - Content
        x[0][0][2][0].text = state_etc  # 1st cell - 1st paragraph - 3rd character range - Content

    # read the column header rows from the Excel file. The first time, we
    # parse the cells to create keys for each column. Once we've read it once,
    # then we just skip those rows
    def build_column_map(self):
        # if we've already mapped from e.g. 'aii' to column 7
        skip = type(self.table1_columns[0]) is int
        # columns will hold 250 key strings while we build them
        # start with 250 empty strings
        columns = ["" for _ in range(NUM_COLUMNS_READ)] if not skip else None
        count = 0
        for row in self.row_iterator:
            count += 1  # we read a row
            if not skip:
                # if we need to generate
                for i in range(min(len(columns), len(row))):
                    fam_member = row[i]  # e.g. "infant" or "teenager"
                    # if not a blank cell, add the first character in the word to the column
                    if fam_member and len(fam_member) > 3:
                        columns[i] = columns[i] + fam_member[0].lower()
            if count == 7:
                break  # stop before reading the 7th row
        if skip:
            return  # if we did this already, just return
        # We find the column index for each of the keys that are being asked for
        # First, create a mapping from column key (e.g. 'aiit') to the column index (e.g. 47)
        xl_column_map = {}
        for i in range(len(columns)):
            key = columns[i]
            if len(key) > 0:
                xl_column_map[key] = i
        # for each requested key for table 1, replace each key (eg 'aiit') with the column index (47)
        for i in range(len(self.table1_columns)):
            key = self.table1_columns[i]
            assert key in xl_column_map, "can't find table 1 column: " + key
            self.table1_columns[i] = xl_column_map[key]

    # append the next table entries from excel starting at "first_row"
    # it's split between 2 tables in InDesign
    def append_table(self, county_sheet) -> bool:
        # the first time, we create the row_iterator at the top of the Excel file,
        # but after that, the row_iterator should already be at the top of the next county data
        if self.row_iterator is None:
            self.row_iterator = county_sheet.iter_rows(min_row=1, max_row=None,
                                                       min_col=1, max_col=NUM_COLUMNS_READ,
                                                       values_only=True)
        try:
            # read the row into a big list
            row = next(self.row_iterator)
        except:
            # if we can't read it, then we're done
            return False

        # title cell from Excel
        head_cell = row[0]
        # If there's a blank row at the end of the data, just say we're done
        if not head_cell or len(head_cell) < 10:
            return False

        # renumber the InDesign elements in the table snippets
        self.renumber()
        # write the correct data from the header cell to the first ID table
        self.format_head(head_cell)
        # read or skip the column headers
        self.build_column_map()

        sum_tax_credits = {}
        taxes = {}
        count = 0
        for row in self.row_iterator:
            count += 1
            if not row[0]:  # skip rows with a blank first cell
                continue
            rowhead = row[0].strip()  # e.g. "Housing"
            if len(rowhead) < 4:
                continue
            elif row[1] is None:  # skip empty rows with just a label
                continue

            cell = None
            if rowhead in self.tax_credits:
                # add rows about tax credits into temporary buckets, added in later
                sum_tax_amounts(row, self.table1_columns, sum_tax_credits)
            elif rowhead == "Taxes":
                # add taxes into temp. bucket, too
                sum_tax_amounts(row, self.table1_columns, taxes)
            else:
                # find the matching row in the ID table to copy the data into
                cell = row_label_match(rowhead, self.snippet1_root)

            if cell is not None:
                copy_numbers(row, cell, self.table1_columns, rowhead == "Hourly")

            if count == 20:
                break  # if we read 20 lines, stop.

        # we just filled out the XML tree representing the InDesign table as a snippet
        # fill out the couple of calculated entries: Taxes (Net) and Tax Credits
        for k in taxes:
            taxes[k] += sum_tax_credits[k]
        cell = row_label_match("Taxes (Net)", self.snippet1_root)
        copy_numbers(taxes, cell, self.table1_columns, False)
        cell = row_label_match("Tax Credits", self.snippet1_root)
        copy_numbers(sum_tax_credits, cell, self.table1_columns, False)

        # append it to the end of the file we are building
        self.id_file = open(self.id_filename, "ab")
        self.snippet1_xml.write(self.id_file)

        # add a "force-page-break" after the table
        self.id_file.write(b'''<CharacterStyleRange AppliedCharacterStyle="CharacterStyle/$ID/[No character style]" ParagraphBreakType="NextPage"><Br /></CharacterStyleRange>\n''')
        self.id_file.close()
        return True

    # finish the file by appending the "post table snippet"
    def finish(self):
        self.id_file = open(self.id_filename, "a", encoding="utf-8")
        with open('PosttableSnippet.xml', encoding="utf-8") as postfile:
            post_data = postfile.read()
            self.id_file.write(post_data)
        self.id_file.close()
        self.id_file = None
