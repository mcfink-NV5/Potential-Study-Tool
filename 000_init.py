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


def combine_measure_sheets(file_path):
    # Load the Excel file
    excel_file = pd.ExcelFile(file_path)
    
    # Initialize an empty list to hold dataframes
    df_list = []
    
    # Iterate over each sheet in the Excel file
    for sheet_name in excel_file.sheet_names:
        # Read the sheet into a dataframe
        df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=33, nrows=18)
         # Drop the first column if it's not needed
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
        # Drop rows where all elements are '-'
        df_transposed = df_transposed[~(df_transposed == '-').all(axis=1)]


        # Append the dataframe to the list
        df_list.append(df_transposed)
    
    # Concatenate all dataframes in the list into a single dataframe
    combined_df = pd.concat(df_list, ignore_index=True)
    
    return combined_df

def measure_sheets(file_path):
    # Load the Excel file
    excel_file = pd.ExcelFile(file_path)

        # Read the sheet into a dataframe
    df = pd.read_excel(file_path, skiprows=33, nrows=18)
        # Drop the first column if it's not needed
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
