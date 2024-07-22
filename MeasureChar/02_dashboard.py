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
    os.chdir(r"C:\Users\AndrewJ.Johnson\OneDrive - NV5\Documents\GitHub\Potential-Study-Tool\MeasureChar")
    df = combine_measure_sheets_test(filename)
    os.chdir(r"C:\Users\AndrewJ.Johnson\OneDrive - NV5\Documents\GitHub\Potential-Study-Tool")
else:
    os.chdir(r"C:\Users\AndrewJ.Johnson\OneDrive - NV5\Documents\GitHub\Potential-Study-Tool")
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
## Create for Sector
sector = st.sidebar.multiselect("Pick your Sector", df_clean["sector"].unique())
if not sector:
    df2 = df_clean.copy()
else:
    df2 = df_clean[df_clean["sector"].isin(sector)]
# # # # Create for primary_fuel
# # Create for primary_fuel_end_use
# # Create for links_with
primary_fuel = st.sidebar.multiselect("Pick your Primary Fuel", df_clean["primary_fuel"].unique())
if not primary_fuel:
    df2 = df_clean.copy()
else:
    df2 = df_clean[df_clean["primary_fuel"].isin(primary_fuel)]


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