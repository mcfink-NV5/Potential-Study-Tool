# ========================
# # Load packages
# # ========================
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
from PIL import Image
warnings.filterwarnings('ignore')

# ========================
### Call Functions
# ========================
script_path = '000_init.py'

with open(script_path, 'r') as f:
    script_code = f.read()

exec(script_code)

# ========================
### Build Web app
# ========================
st.set_page_config(page_title="Measure List Creation", layout="wide")
# Load the image
image = Image.open('NV5.jpg')
# Create columns
col1, col2 = st.columns([0.2, 0.8])
# Place the image in the first column
with col1:
    st.image(image,  width=200)
# Place the title in the second column
with col2:
    st.title("Measure List Creation")
# Add padding to the top of the block container
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# ========================
### Uploader
# ========================
#TODO make this so we can append file and not overwrite
#to upload a file
fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))

#TODO fix this os issue I had some issues with pointing and this works but calling OS is generally not good
if fl is not None:
    filename = fl.name
    st.write(filename)
    #os.chdir(r"C:\Users\AndrewJ.Johnson\OneDrive - NV5\Documents\GitHub\Potential-Study-Tool\MeasureChar")
    os.chdir(os.relpath("MeasureChar"))
    df = combine_measure_sheets_test(filename)
    #os.chdir(r"C:\Users\AndrewJ.Johnson\OneDrive - NV5\Documents\GitHub\Potential-Study-Tool")
    os.chdir(os.relpath(".."))  
else:
    #os.chdir(r"C:\Users\AndrewJ.Johnson\OneDrive - NV5\Documents\GitHub\Potential-Study-Tool")
    df = combine_measure_sheets_test("MeasureChar/Test_Measures.xlsx")

# ========================
### Cleaning 
# TODO move cleaning to backend?
# ========================
#Clean Output
df_clean = df.rename(columns=clean_headers) #Could change this for format the columns but this is an internal tool so I prefer this

df_clean = df_clean.dropna(how='all')
#there is bad raw data I am guessing
# #remove these odd rows
mask = df_clean == '-'
# Count the number of '-' in each row
count_dashes = mask.sum(axis=1)
# Remove rows where the count of '-' is more than 1
df_clean = df_clean[count_dashes <= 1]

# ========================
### Filters
# ========================
st.sidebar.header("Choose your filter: ")
# # Create for primary_fuel_end_use
# # Create for links_with

sector = st.sidebar.multiselect("Pick your Sector", df_clean["sector"].unique())

# Filter the DataFrame by sector
if sector:
    df2 = df_clean[df_clean["sector"].isin(sector)]
else:
    df2 = df_clean.copy()

# Create Primary Fuel filter
primary_fuel = st.sidebar.multiselect("Pick your Primary Fuel", df2["primary_fuel"].unique())

# Filter the DataFrame by primary fuel (on top of the sector filter)
if primary_fuel:
    df2 = df2[df2["primary_fuel"].isin(primary_fuel)]
# ========================
### Make Heat map of completion DF and chart
heatchart = df2

import plotly.graph_objects as go
st.subheader('Data Completion Heat Map')
# ========================

# Create a binary DataFrame where 1 indicates non-NA and 0 indicates NA
binary_df = heatchart.drop(columns=['measure_name']).notna().astype(int)

# Get the measure names for the Y-axis
measure_names = heatchart['measure_name']

# Create a heat map
fig = go.Figure(data=go.Heatmap(
    z=binary_df.values,
    x=binary_df.columns,
    y=measure_names,
    colorscale=[[0, 'red'], [1, 'green']],
    showscale=False
))

# Update layout for better readability
fig.update_layout(
    height=500,
    width=1000,
    xaxis_title="Columns",
    yaxis_title="Measure Names",
    font=dict(
        family="Arial, sans-serif",
        size=14,
        color="Black"
    )
)

# Display the heat map
st.plotly_chart(fig, use_container_width=True)


# ========================
### Make Scatterplot DF and chart
st.subheader('Scatter Plot')
# ========================
scatterchart = df2
# Create a selectbox for the Y-axis
y_axis = st.selectbox("Select the Y-axis", options=scatterchart.columns)

# Create the scatter plot
fig2 = px.scatter(scatterchart, x="measure_name", y=y_axis, height=500, width=1000, template="gridon")


#fig2 = px.scatter(scatterchart, x = "measure_name", y="incremental_cost_per_kwh__mmbtu_saved" ,height=500, width = 1000,template="gridon")
st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Data of ScatterPlot:"):
    st.write(scatterchart.T.style.background_gradient(cmap="Blues"))
    csv = scatterchart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "ScatterPlot.csv", mime ='text/csv')

# ========================
### Create Measure Sheet
# ========================
#Columns needed
#Meas #	
# Sector	
# Measure Name	
# Primary End Use	
# Measure Long Name	
# Parent Measure Name	
# Parent Measure Long Name	
# Description	
# Life	
# Exist. Life	
# Life/Existing Life
#Source
# Life Source #s	
# Pri-mary Fuel	
# 2nd-ary Fuel	
# Primary Fuel End Use	
# 2ndary Fuel End Use	
# Elec Load Shape	
# Fuel Switch	
# Waste Heat Adjust.	
# In Use	
# Depends On	
# Links With

with st.expander("Measure Sheet:"):
    st.write(df.style.background_gradient(cmap="Blues"))
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "measure_sheet.csv", mime ='text/csv')

# ========================
### Create MeasureChar Sheet
# ========================
#Columns needed 
#Meas#	
# Mkt	
# EndUse	
# MeasLongName				
# Status	
# Notes			
# TargetMkts	
# Baseline	
# StartYr	
# EndYr	
# BldgTypeForChar	
# Units	EffKw	
# BaseKw	
# FLH	
# AnnKWh	
# PctSavings	
# FLHSrc	
# SavingsSrc	
# SavingsSrc#	
# EffCost	
# BaseCost	
# IncCost	 
# IncCostPerKwh 	 
# IncCostSrc 	 
# CostsSrc# 	 
# BaseLife 	 
# BaseAge 	 
# BaseCostRet 	 
# BaseCostPerKwh 	
# BaseShift	
# BaseShiftSrc	
# BaseCostRetSrc	
# EffComp1	 
# EffComp1Life 	 
# EffComp1LifeSrc 	
# EffComp1Cost	
# EffComp1CostSrc	
# EffComp1CostPerKwh	
# EffComp2	 
# EffComp2Life 	 
# EffComp2LifeSrc 	
# EffComp2Cost	
# EffComp2CostSrc	
# EffComp2CostPerKwh	
# BaseComp1	 
# BaseComp1Life 	 
# BaseComp1LifeSrc 	
# BaseComp1Cost	
# BaseComp1CostSrc	
# BaseComp1CostPerKwh	
# BaseComp2	 
# BaseComp2Life 	 
# BaseComp2LifeSrc 	
# BaseComp2Cost	
# BaseComp2CostSrc	
# BaseComp2CostPerKwh	
# LevCostOM		
# MeasLife	
# Fuel1Type	
# Fuel1Sav	
# Fuel1SavPerKwh	
# Fuel1SavPerKwhSrc	
# Water	
# WaterPerKwh	
# WaterSrc

with st.expander("MeasureChar Sheet:"):
    st.write(df.style.background_gradient(cmap="Blues"))
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "measurechar_sheet.csv", mime ='text/csv')