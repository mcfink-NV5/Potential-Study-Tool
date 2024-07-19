import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
from PIL import Image
warnings.filterwarnings('ignore')

def combine_excel_sheets(file_path):
    # Load the Excel file
    excel_file = pd.ExcelFile(file_path)
    
    # Initialize an empty list to hold dataframes
    df_list = []
    
    # Iterate over each sheet in the Excel file
    for sheet_name in excel_file.sheet_names:
        # Read the sheet into a dataframe
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        # Add a column for the sheet name
        df['SheetName'] = sheet_name
        # Append the dataframe to the list
        df_list.append(df)
    
    # Concatenate all dataframes in the list into a single dataframe
    combined_df = pd.concat(df_list, ignore_index=True)
    
    return combined_df

#For matplot lib
#%pylab inline