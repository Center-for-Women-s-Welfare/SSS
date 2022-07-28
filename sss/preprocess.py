import re
# std_col_names is to standardlize the column names in the columns
def std_col_names(pd_dataframe):
	
	#if dataframe headers have parentheses and content within , replace with empty
	pd_dataframe.columns = [re.sub('\(.*?\)','',col) for col in pd_dataframe.columns]
	# trim the column name
	pd_dataframe.columns = [col.strip().lower() for col in pd_dataframe.columns]
	# if dataframe headers have spaces, replace with underscores
	pd_dataframe.columns = [col.replace(' ', '_').lower() for col in pd_dataframe.columns]
	# if dataframe headers have -, replace with underscores
	pd_dataframe.columns = [col.replace('-', '_') for col in pd_dataframe.columns]
	# if dataframe headers have __, replace with underscores
	pd_dataframe.columns = [col.replace('__', '_') for col in pd_dataframe.columns]
	# if dataframe headers have _cost replace with nothing
	pd_dataframe.columns = [col.replace('_costs', '')for col in pd_dataframe.columns]
	# if dataframe headers have 1 replace with nothing
	pd_dataframe.columns = [col.replace('1', '')for col in pd_dataframe.columns]
	# if dataframe headers have preshooler replace with preschooler
	pd_dataframe.columns = [col.replace('preshooler', 'preschooler')for col in pd_dataframe.columns]
	# if dataframe headers have famcode replace with family_type
	pd_dataframe.columns = [col.replace('famcode', 'family_type')for col in pd_dataframe]
	# if dataframe headers have release_year replace with year
	pd_dataframe.columns = [col.replace('release_year', 'year')for col in pd_dataframe]
	# if dataframe headers have release_year replace with place
	pd_dataframe.columns = [col.replace('town', 'place')for col in pd_dataframe]
	# if dataframe headers have county replace with place
	pd_dataframe.columns = [col.replace('county', 'place')for col in pd_dataframe]
	# if dataframe headers have status replace with analysis_type
	pd_dataframe.columns = [col.replace('status', 'analysis_type')for col in pd_dataframe]
	# if dataframe headers have & replace with and
	pd_dataframe.columns = [col.replace('&', 'and')for col in pd_dataframe]
	
	return pd_dataframe
	
