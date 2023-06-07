"""Clean SSS data files to be used in sss_table.py."""
import glob
import re
import os


# std_col_names is to standardlize the column names in the columns
def std_col_names(pd_dataframe):
    """
    Standardizes the columns of the Pandas dataframe.

    Standardizes the columns of the Pandas dataframe.

    Specifically, this function cleans up column names by removing
    any characters we do not want.

    Parameters
    ----------
    df : pandas.dataframe
        dataframe that we want to clean column names

    Returns
    -------
    pandas.datafranme
        dataframe that has standardized column names

    """
    # if dataframe headers have parentheses and content within , replace with empty
    pd_dataframe.columns = [re.sub(r'\(.*?\)', '', col) for col in pd_dataframe.columns]
    # trim the column name
    pd_dataframe.columns = [col.strip().lower() for col in pd_dataframe.columns]

    # for this dictionary, the keys are the values that are being replaced
    # the keys are being replaced by their value
    replace_dict = {
        " ": "_",
        "-": "_",
        "__": "_",
        "_costs": "",
        "1": "",
        "preshooler": "preschooler",
        "famcode": "family_type",
        "release_year": "year",
        "town": "place",
        "county": "place",
        "status": "analysis_type",
        "&": "and",
    }
    for key in replace_dict:
        pd_dataframe.columns = [
            col.replace(key, replace_dict[key]) for col in pd_dataframe.columns
        ]
    return pd_dataframe


def data_path_to_file_list(data_path, extension_match=None):
    """
    Get a list of files given a data path, which can be a file or folder.

    Parameters
    ----------
    data_path : str
        Path name of the folder or file that we want to read into the database.
        For folders, get all files in that folder with extensions that match
        `extension_match`.
    extension_match : str
        String to use for matching extensions. For excel files, use "xls*".
    """
    if os.path.isfile(data_path):
        data_files = [data_path]
    elif os.path.isdir(data_path):
        data_files = glob.glob(os.path.join(data_path, "*." + extension_match))
    else:
        raise ValueError("data_path must be a file or folder on this system")

    return data_files
