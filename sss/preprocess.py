import re
# std_col_names is to standardlize the column names in the columns
def std_col_names(pd_dataframe):
	"""
	This function takes in a pandas df and standardizes the columns

    Specifically, this function cleans up column names by removing
	any characters we do not want. In this case, it is the keys
	of the dictionary that are being replace by the value of the
	dictionary. 

    Parameters
    ----------
    df: pandas.dataframe
        dataframe that we want to to clean column names

    Returns
    -------
    pandas.datafranme
        dataframe that has standardized column names

	"""
	#TODO: Add docstrings
	#if dataframe headers have parentheses and content within , replace with empty
	pd_dataframe.columns = [re.sub('\(.*?\)','',col) for col in pd_dataframe.columns]
	# trim the column name
	pd_dataframe.columns = [col.strip().lower() for col in pd_dataframe.columns]

	replace_dict = {' ':'_', '-':'_', '__': '_', '_costs': '', '1':'', 
						'preshooler': 'preschooler', 'famcode':'family_type',
						'release_year':'year', 'town':'place', 'county':'place', 
						'status': 'analysis_type', '&': 'and'}
	for i in replace_dict:
			pd_dataframe.columns = [col.replace(i, replace_dict[i]) for col in pd_dataframe.columns]	

	return pd_dataframe
	
