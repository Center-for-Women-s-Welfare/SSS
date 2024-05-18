"""
Read lines from an Excel file and copy the proper cells into an InDesign snippet.

Primarily the help clas Snippet4ID is used to iterate through the Excel file.
It will build an InDesign snippet file (XML format) that will represent
a sequence of tables -- one for each county.
There is a tight correspondence between this code and
the format of the Excel tables and the InDesign snippets.
"""

# library for reading/writing xml files
import lxml

# library for regular expressions (complex find)
import re

NUM_COLUMNS_READ = 250  # columns of data (family types)


def copy_numbers(rowdata, prevcell, columns: list, keep_cents: bool):
    """
    Copy the numeric values from Excel into the cells in the XML snippet.

    :param rowdata the Excel row with all the data
    :param prevcell the table cell in the XML tree to the left of our target
    :param columns: the list of column indices to insert
    :param keep_cents: False = round to integers, else use 2 digits after decimal
    """
    for colidx in columns:
        colvalue = rowdata[colidx]  # value in the Excel file in the right column
        if type(colvalue) is str:  # if it's a string, make it a number
            colvalue = float(colvalue)
        if colvalue < 0.0:
            colvalue = "(${:,.0f})".format(-colvalue)
        elif keep_cents:
            colvalue = "${:,.2f}".format(colvalue)
        else:
            colvalue = "${:,.0f}".format(colvalue)
        # move to the correct cell & replace content
        prevcell = prevcell.getnext()
        # 1st paragraph - 2nd character range - Content
        prevcell[0][0][0].text = colvalue


def sum_tax_amounts(rowdata: list, columns: list, amount_dict):
    """
    For the cells that are being calculated (taxes), track the sums.

    :param rowdata the Excel row with all the data
    :param columns the list of column indices to sum up
    :param amount_dict store the sums here - key=column index, value=sum
    """
    for colidx in columns:
        colvalue = rowdata[colidx]  # value in the Excel file in the right column
        if type(colvalue) is str:  # if it's a string, make it a number
            colvalue = float(colvalue)
        if colidx in amount_dict:
            amount_dict[colidx] += colvalue
        else:
            amount_dict[colidx] = colvalue


def row_label_match(rowhead: str, root):
    """Return the XML element that matches the row description in the Excel.

    For example, the Excel row starts with "Housing", so we look for "Housing"
    in the XML content. There are minor differences between the Excel and the ID rows
    :param rowhead the row title from the Excel file (e.g. 'Housing')
    :param root the root of the XML tree representing one InDesign table snippet
    :return the corresponding row in the snippet that matches
    """
    xpath = "Cell//Content[.='" + rowhead + "']"
    cell = root.xpath(xpath)
    # newline in row header, just match first line
    if len(cell) == 0 and rowhead.find("\n") >= 0:
        rowhead = rowhead.split("\n")[0]
        xpath = "Cell//Content[.='" + rowhead + "']"
        cell = root.xpath(xpath)
    if len(cell) == 0:  # more complex matching for different wording
        xpath = "Cell//Content[starts-with(text(), '" + rowhead + "')]"  # up to Cell
        cell = root.xpath(xpath)
    assert len(cell) == 1, "can't find proper row in InDesign for " + rowhead
    cell = cell[0].getparent().getparent().getparent()
    return cell


class Snippet4ID:
    """
    Primary function for building InDesign table snippets from Excel.

    This functions kind of as an iterator, where append_table would be
    called repeatedly appending each table to the same file.
    """

    def __init__(self, idfilename: str):
        """Initialize the snippet with the ID snippet filename to create."""
        self.id_filename = idfilename
        self.id_file = open(self.id_filename, "w", encoding="utf-8")
        # copy the "Pretable snippet" into the InDesign file (just copies, no parsing)
        with open("PretableSnippet.xml", encoding="utf-8") as prefixfile:
            prefix_data = prefixfile.read()
            self.id_file.write(prefix_data)
        # close the InDesign file (causes it to write to disk)
        # we open and close it repeatedly
        self.id_file.close()
        # read & parse the table snippet
        self.snippet1_xml = lxml.etree.parse("TableSnippet.xml")
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
        self.tax_credits = [
            "Earned Income Tax Credit (-)",
            "Child Care Tax Credit (-)",
            "Child Tax Credit (-)",
        ]

    def _new_self_id(self, old_id: str) -> str:
        """
        Generate a new id for one element in the XML tree.

        :param old_id: the original id string in the snippet
        :return: str representing the new unique id
        """
        if old_id.startswith(self.defaultTableID):
            return self.nextTableID + old_id[7:]
        return old_id

    def _renumber(self):
        """
        Create new IDs for the table items in the snippet template.

        Probably not used ?? but we make them unique anyway.
        """
        self.nextTableID = "u" + str(int(self.nextTableID[1:]) + 1)
        for child in self.snippet1_root:
            if "Self" in child.attrib:
                new_id = self._new_self_id(child.attrib["Self"])
                child.attrib["Self"] = new_id

    def _format_head(self, head_cell: str):
        """
        Copy the header data into the table snippet.

        :param str head_cell: the contents of the Excel header cell
        """
        # The Excel file has something like --
        #  'Table 1_x000D_\nThe Self-Sufficiency Standard_
        #           x000D_\nfor_x000D_\nAllegany County, MD, 2023>
        # We break this string into the 4 sections, copying the relevant fields
        if "_x000D_\n" in head_cell:
            lines = head_cell.split("_x000D_\n")
        elif "_x000d_\n" in head_cell:
            lines = head_cell.split("_x000d_\n")
        else:
            raise AssertionError("Can't split head row: " + head_cell)

        # validate expected Excel header string
        assert lines[0].startswith("Table"), "Unrecognized format head: " + head_cell
        assert lines[1].endswith("The Self-Sufficiency Standard"), (
            "Unrecognized format head: " + head_cell
        )
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
        # 1st cell - 1st paragraph - 2nd character range - Content
        x[0][0][1][0].text = county_name
        # 1st cell - 1st paragraph - 3rd character range - Content
        x[0][0][2][0].text = state_etc

    def _build_column_map(self):
        """
        First time, read all column headers to create map between index & header desc.

        We read up to NUM_COLUMNS_READ columns turning the column head (e.g. 'aii')
        into the column index (e.g. 7). We only do this once. These indices are used
        instead of the strings (i.e. using 7 instead of 'aii')
        """
        # if we've already created the map from e.g. 'aii' to column 7
        skip = type(self.table1_columns[0]) is int
        # if skip is True, we still read the 7 rows the column headers use, but we skip them
        # columns will hold 250 key strings while we build them
        # start with 250 empty strings
        columns = ["" for _ in range(NUM_COLUMNS_READ)] if not skip else None
        count = 0
        for row in self.row_iterator:
            count += 1  # we read a row
            if not skip:
                # if we need to generate the table
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
        # for each requested key for table 1,
        #     replace each key (eg 'aiit') with the column index (47)
        for i in range(len(self.table1_columns)):
            key = self.table1_columns[i]
            assert key in xl_column_map, "can't find table 1 column: " + key
            self.table1_columns[i] = xl_column_map[key]

    def append_table(self, county_sheet) -> bool:
        """
        Append the next table from Excel starting at "first_row".

        :param county_sheet: this is the Excel sheet object from openpyxl
        :return: False if the end of the Excel was reached, True if success
        """
        # the first time, we create the row_iterator at the top of the Excel file,
        # after, the row_iterator should already be at the first line of the next county
        if self.row_iterator is None:
            self.row_iterator = county_sheet.iter_rows(
                min_row=1,
                max_row=None,
                min_col=1,
                max_col=NUM_COLUMNS_READ,
                values_only=True,
            )
        try:
            # read the row into a big list
            row = next(self.row_iterator)
        except StopIteration:
            # if we can't read it, then we're done
            return False

        # title cell from Excel
        head_cell = row[0]
        # If there's a blank row at the end of the data, just say we're done
        if not head_cell or len(head_cell) < 10:
            return False

        # prepare new table snippet by renumbering the InDesign elements
        self._renumber()
        # write the correct data from the header cell to the InDesign table
        self._format_head(head_cell)
        # read or skip the column headers
        self._build_column_map()

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
                # sum rows about tax credits into temporary buckets, added in later
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
                break  # after if we read 20 lines, stop.

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
        self.id_file.write(
            b"""<CharacterStyleRange AppliedCharacterStyle="CharacterStyle/$ID/"""
            b"""[No character style]" ParagraphBreakType="NextPage">"""
            b"""<Br /></CharacterStyleRange>\n"""
        )
        self.id_file.close()
        return True

    def finish(self):
        """Finish the file by appending the post table snippet."""
        self.id_file = open(self.id_filename, "a", encoding="utf-8")
        with open("PosttableSnippet.xml", encoding="utf-8") as postfile:
            post_data = postfile.read()
            self.id_file.write(post_data)
        self.id_file.close()
        self.id_file = None
