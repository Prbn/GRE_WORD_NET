#functions

from IPython.display import display
import pandas as pd
import os
import numpy as np
import re

# Preview Data frame
def preview_df(df_data: pd.DataFrame, n_row:int = 5):
    print('------------------')
    print('Top {} rows:'.format(n_row))
    display(df_data.head(n_row))
    print('Columns: '+ str(len(list(df_data.columns))) + '\n' + (', '.join(df_data.columns)) + '\n')
    print('#Rows: ' + str(df_data.shape[0]))
    print('------------------ \n')

# concat N number of dataframes, using common columns
def concat_df(df_list: list, noDup: bool = True):
    col_set = set([str(y) for x in df_list for y in x.columns])
    col_list = list(col_set)
    new_list = list()
    for df in df_list:
        new_col_list = list(col_set.difference(set(df.columns)))
        df[new_col_list] = np.nan
        df = df[col_list]
        new_list.append(df)
    print('Columns:')
    print(list(col_set))
    if noDup == True:
        return pd.concat(new_list).drop_duplicates()
    else:
        return pd.concat(new_list)

# analyse common and uncommon columns in N number of dataframes
def col_analysis_df(df_dict: dict):
    all_col_set = set([str(y) for x in df_dict.values() for y in x.columns])
    common_col_set = set.intersection(*[set(x.columns) for x in df_dict.values()])
    print('------------------')
    print('All Columns:')
    print(list(all_col_set))

    print('\nCommon Columns:')
    print(list(common_col_set))
    print('------------------ \n')

    for key in df_dict:
        col_set = set([str(y) for y in df_dict[key].columns])
        extra_col_set = col_set.difference(common_col_set)
        missing_col_set = all_col_set.difference(col_set)
        print('------------------')
        print('Table: {}'.format(key))
        print('Columns in this table:')
        print(list(col_set))
        print('\nExtra columns in this table:')
        print(list(extra_col_set))
        print('\nMissing columns in this table:')
        print(list(missing_col_set))
        print('------------------ \n')

        
# Check granularity of a dataframe
def unique_check_df(df_data: pd.DataFrame, df_col: list):
    Temp_df = df_data.groupby(df_col).size()
    Temp_df = pd.DataFrame({'VAR': list(Temp_df.index), 'VAL': Temp_df.values})
    Temp_df = Temp_df[Temp_df['VAL'] > 1]
    
    if Temp_df.shape[0] == 0:
        print('The data frame is unique at '+', '.join(df_col))
    else:
        print('The data frame is not unique at ' + ', '.join(df_col))
        print('Duplicate values:')
        display(Temp_df)
        

# Check granularity of a dataframe
def duplicate_check_df(df_data: pd.DataFrame, df_col: list):
    Temp_df = df_data.groupby(df_col).nunique()
    Temp_df = Temp_df[Temp_df.gt(1).any(axis=1)]
    
    if Temp_df.shape[0] == 0:
        print('The data frame is unique at '+', '.join(df_col))
    else:
        print('The data frame is not unique at ' + ', '.join(df_col))
        display(Temp_df)  
        
        
# Get First, Middle, and Last names from Full name    Temp_df
Name_RE = re.compile(r"(?P<First>\S+)\s(?:(?P<Middle>\S*)\s)?(?P<Last>\S+)$")

def get_names(Demo_df, col_FN = 'HCP Full Name'):
    names = Name_RE.match(str(Demo_df[col_FN]))
    if names is not None:
        return pd.Series(names.groupdict())
    else:
        return None
    


def data_transform_1(flag_detail_dict: dict):
    new_list = list()
    for temp_key in flag_detail_dict:

        brand_name = flag_detail_dict[temp_key][0]
        data_df = flag_detail_dict[temp_key][1]
        index_col = flag_detail_dict[temp_key][2]
        col_dict = flag_detail_dict[temp_key][3]

        for indication in col_dict:
            temp_df = pd.DataFrame(columns={'HCP_AZ_CUST_ID':pd.Series(dtype='str')
                                            , 'Brand':pd.Series(dtype='str')
                                            , 'Indication':pd.Series(dtype='str')
                                            , 'Priority':pd.Series(dtype='str')})
            temp_df[['HCP_AZ_CUST_ID', 'Priority']] = data_df[[index_col, col_dict[indication]]].drop_duplicates()
            temp_df['Brand'] = brand_name
            temp_df['Indication'] = indication
            new_list.append(temp_df[['HCP_AZ_CUST_ID', 'Brand', 'Indication', 'Priority']])

    return pd.concat(new_list).drop_duplicates().sort_values(by=['HCP_AZ_CUST_ID', 'Brand', 'Indication'])






# LIST OF Functions

# 1)  preview_df: preview_df(<Dataframe>, <no. of rows (5 by default)>)
    # - To preview the data frame
    # - Displays head of the data frame
    # - Displays column count and lists all the columns
    # - Displays the row count
    
# 2)  concat_df: concat_df(<List of Dataframes>)
    # - Concats a list of Dataframe
    # - common columns are appended together
    # - column that is not present in a dataframe is nulled.

# 3)  col_analysis_df: col_analysis_df(<List of Dataframes>)
    # - List out all columns in the list of Dataframes
    # - List out all the common column
    # - list out all the missing columns in a Dataframe

# 4)  unique_check_df: unique_check_df(<Dataframe>, <List of column Names>)
    # - Checks if the column/column combination is unique to the table
    # - used to check the granularity of a data set
    
# 5)  duplicate_check_df: duplicate_check_df(<Dataframe>, <List of column Names>)
    # - Checks if the column/column combination is unique to the table
    # - Displays a table to show the reason of duplicate values

# 6)  get_names:
    # - Breaks full name into First, Middle, and Last Name

# 7) data_transform_1:
    # - custom function to transpose data
    # df_tools.data_transform_1(data_dictionary)
    # Where data_dictionary = {'<List_Name>': [<(1) Brand Name: str>, <(2) Flag_data: Dataframe>, <(3) HCP ID Column Name: str>, {<(4.1.1)Indication Name: str>: <(4.1.2)Priority column Name in data: str>, <(4.2.1)Indication Name: str>: <(4.2.2)Priority column Name in data: str>}, <(4.~.1)Indication Name: str>: <(4.~.2)Priority column Name in data: str>}],

    
    