import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
from PIL import Image

warnings.filterwarnings('ignore')

def clean_headers(val):
    if isinstance(val, str):
        # remove special chars (but skip emtpy spaces and all)
        val = "".join(char for char in val if char.isalnum() or char in (" ", "_"))
        # convert to snake case
        val = val.strip().lower().replace(" ", "_")
        return val
    else:
        return val

#PR_Measures
def combine_measure_sheets_test(file_path):
    # Load the Excel file
    excel_file = pd.ExcelFile(file_path)
    
    # Initialize an empty list to hold dataframes
    df_list = []
    
    # Iterate over each sheet in the Excel file
    for sheet_name in excel_file.sheet_names:
        # Read the sheet into a dataframe
        df_measure          = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=31, nrows=18)
        # Generate column headers, e.g., A, B, C, ...
        num_columns = df_measure.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)]  # 65 is ASCII code for 'A'
        # Assign the new headers to the DataFrame
        df_measure.columns = column_headers

        df_measchars        = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=52, nrows=17)
        num_columns = df_measchars.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_measchars.columns = column_headers
        
        df_sec_end_use_fuel = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=70, nrows=2)
        num_columns = df_sec_end_use_fuel.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_sec_end_use_fuel.columns = column_headers

        df_om               = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=81, nrows=5)
        num_columns = df_om.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_om.columns = column_headers

        df_early_retirement = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=74, nrows=5)
        num_columns = df_early_retirement.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_early_retirement.columns = column_headers

        df_alt              = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=89, nrows=12)
        num_columns = df_alt.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_alt.columns = column_headers
    
        df_water            = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=102, nrows=2)
        num_columns = df_water.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_water.columns = column_headers
        # Concatenate the dataframes along rows (axis=0)
        df = pd.concat([df_measure, df_measchars, df_sec_end_use_fuel, df_om, df_early_retirement, df_alt, df_water], axis=0, ignore_index=True)
    
    #     # Drop the first column if it's not needed
        df = df.drop(columns=[df.columns[0]])
        df_transposed = df.T
        df_transposed.columns = df_transposed.iloc[0]
        df_transposed = df_transposed[1:]
        df_transposed.reset_index(drop=True, inplace=True)
        # Drop rows that are completely blank
        df_transposed.dropna(how='all', inplace=True)
        # Drop columns that are completely blank
        #df_transposed.dropna(axis=1, how='all', inplace=True)
         # Drop columns where the name is NaN
        df_transposed = df_transposed.loc[:, ~df_transposed.columns.isna()]
       
    #    #Logging
    #    total_items = len(items)
    #         for i, item in enumerate(items):
    #     # Process the item
    #             print(f"Processing item {i + 1} of {total_items}")
        # Append the dataframe to the list
        df_list.append(df_transposed)
    
    # Concatenate all dataframes in the list into a single dataframe
    combined_df = pd.concat(df_list, ignore_index=True)
    
    return combined_df


#PR_Measures
def combine_measure_sheets_PR(file_path):
    # Load the Excel file
    excel_file = pd.ExcelFile(file_path)
    
    # Initialize an empty list to hold dataframes
    df_list = []
    
    # Iterate over each sheet in the Excel file
    for sheet_name in excel_file.sheet_names:
        # Read the sheet into a dataframe
        df_measure          = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=31, nrows=18)
        # Generate column headers, e.g., A, B, C, ...
        num_columns = df_measure.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)]  # 65 is ASCII code for 'A'
        # Assign the new headers to the DataFrame
        df_measure.columns = column_headers

        df_measchars        = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=52, nrows=17)
        num_columns = df_measchars.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_measchars.columns = column_headers
        
        df_sec_end_use_fuel = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=70, nrows=2)
        num_columns = df_sec_end_use_fuel.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_sec_end_use_fuel.columns = column_headers

        df_om               = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=81, nrows=5)
        num_columns = df_om.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_om.columns = column_headers

        df_early_retirement = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=74, nrows=5)
        num_columns = df_early_retirement.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_early_retirement.columns = column_headers

        df_alt              = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=89, nrows=12)
        num_columns = df_alt.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_alt.columns = column_headers
    
        df_water            = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=102, nrows=2)
        num_columns = df_water.shape[1]
        column_headers = [chr(65 + i) for i in range(num_columns)] 
        df_water.columns = column_headers
        # Concatenate the dataframes along rows (axis=0)
        df = pd.concat([df_measure, df_measchars, df_sec_end_use_fuel, df_om, df_early_retirement, df_alt, df_water], axis=0, ignore_index=True)
    
    #     # Drop the first column if it's not needed
        df = df.drop(columns=[df.columns[0]])
        df_transposed = df.T
        df_transposed.columns = df_transposed.iloc[0]
        df_transposed = df_transposed[1:]
        df_transposed.reset_index(drop=True, inplace=True)
        # Drop rows that are completely blank
        df_transposed.dropna(how='all', inplace=True)
        # Drop columns that are completely blank
        #df_transposed.dropna(axis=1, how='all', inplace=True)
         # Drop columns where the name is NaN
        df_transposed = df_transposed.loc[:, ~df_transposed.columns.isna()]
       
    #    #Logging
    #    total_items = len(items)
    #         for i, item in enumerate(items):
    #     # Process the item
    #             print(f"Processing item {i + 1} of {total_items}")
        # Append the dataframe to the list
        df_list.append(df_transposed)
    
    # Concatenate all dataframes in the list into a single dataframe
    combined_df = pd.concat(df_list, ignore_index=True)
    
    return combined_df

def measure_sheets(file_path):
    # Load the Excel file
    excel_file = pd.ExcelFile(file_path)

        # Read the sheet into a dataframe
    df_measure          = pd.read_excel(file_path, skiprows=31, nrows=18)
        # Generate column headers, e.g., A, B, C, ...
    num_columns = df_measure.shape[1]
    column_headers = [chr(65 + i) for i in range(num_columns)]  # 65 is ASCII code for 'A'
# Assign the new headers to the DataFrame
    df_measure.columns = column_headers

    df_measchars        = pd.read_excel(file_path, skiprows=52, nrows=17)
    num_columns = df_measchars.shape[1]
    column_headers = [chr(65 + i) for i in range(num_columns)] 
    df_measchars.columns = column_headers
    
    df_sec_end_use_fuel = pd.read_excel(file_path, skiprows=70, nrows=2)
    num_columns = df_sec_end_use_fuel.shape[1]
    column_headers = [chr(65 + i) for i in range(num_columns)] 
    df_sec_end_use_fuel.columns = column_headers

    df_om               = pd.read_excel(file_path, skiprows=81, nrows=5)
    num_columns = df_om.shape[1]
    column_headers = [chr(65 + i) for i in range(num_columns)] 
    df_om.columns = column_headers

    df_early_retirement = pd.read_excel(file_path, skiprows=74, nrows=5)
    num_columns = df_early_retirement.shape[1]
    column_headers = [chr(65 + i) for i in range(num_columns)] 
    df_early_retirement.columns = column_headers

    df_alt              = pd.read_excel(file_path, skiprows=89, nrows=12)
    num_columns = df_alt.shape[1]
    column_headers = [chr(65 + i) for i in range(num_columns)] 
    df_alt.columns = column_headers

    df_water            = pd.read_excel(file_path, skiprows=102, nrows=2)
    num_columns = df_water.shape[1]
    column_headers = [chr(65 + i) for i in range(num_columns)] 
    df_water.columns = column_headers
        # Concatenate the dataframes along rows (axis=0)
    df = pd.concat([df_measure, df_measchars, df_sec_end_use_fuel, df_om, df_early_retirement, df_alt, df_water], axis=0, ignore_index=True)
    
    #     # Drop the first column if it's not needed
    df = df.drop(columns=[df.columns[0]])
    df_transposed = df.T
    df_transposed.columns = df_transposed.iloc[0]
    df_transposed = df_transposed[1:]
    df_transposed.reset_index(drop=True, inplace=True)
    # Drop rows that are completely blank
    df_transposed.dropna(how='all', inplace=True)
    # Drop columns that are completely blank
    #df_transposed.dropna(axis=1, how='all', inplace=True)
     # Drop columns where the name is NaN
    df_transposed = df_transposed.loc[:, ~df_transposed.columns.isna()]
    
    return df_transposed

#For matplot lib
#%pylab inline
