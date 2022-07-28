import pandas as pd
import re
import preprocess



def geoidentifier_creator(county_table, cpi_table):
    """The function to create geoidentifier
    Parameters
    ----------
    county_table : string
            The path of the county table including FIPS code
    cpi_table : string
            The path of the cpi_table including capi region
    Returns
    -------
    df_combine : dataframe
            Return the merged table from county_table and cpi_table

    Raises
    ------
    ValueError
        Column name may not exist when merging

    """

    xl = pd.ExcelFile(county_table)
    # n_sheets = len(xl.sheet_names)
    df_l = pd.read_excel(county_table, sheet_name = 0, dtype=str)
    print(df_l.head())
    print("Read the first sheet of LEFT table"+' '+ xl.sheet_names[0]+'. \
        Please adjust the sheet order if your tagret table is not the first one')
    df_l['fips_state'] = df_l['fips2010'].str[:2]
    df_l['county_state'] = df_l['fips2010'].str[2:5]
    df_l['place_fips'] = df_l['fips2010'].str[5:]
    

    xl_r = pd.ExcelFile(cpi_table)
    # n_sheets_r = len(xl_r.sheet_names)
    df_r = pd.read_excel(cpi_table, sheet_name = 0)
    print("Read the first sheet of RIGHT table"+' '+ xl_r.sheet_names[0]+'.\
         Please adjust the sheet order if your tagret table is not the first one')

    try:
        df_combine = df_l.merge(df_r,left_on = 'state_alpha', right_on = 'USPS Abbreviation', how='left')
        df_combine = df_combine.rename(columns={"state_alpha": "state", "CPI Region": "cpi_region","CPI SSS_Place":"place"})
        if df_combine.shape[0] != df_l.shape[0]:
            print('Merge sucessfully but new rows were created due to duplicaitons in right(CPI) table')
    except:
        raise ValueError('Cannot merge, please check the two columns are named as "state_alpha" and "USPS Abbreviation"')

    return df_combine



# test = geoidentifier_creator('SSScounty-place-list_20220720.xlsx','StateAbbreviation_Regions_07192022_AKu.xlsx')
# print(test.head())
# print(test.columns)
