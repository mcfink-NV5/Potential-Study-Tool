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


### Build Web app
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

# Optional: Add padding to the top of the block container
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

#TODO make this so we can append file and not overwrite
#to upload a file
fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = combine_measure_sheets(filename)
else:
    os.chdir(r"C:\Users\AndrewJ.Johnson\OneDrive - NV5\Documents\GitHub\Potential-Study-Tool")
    df = combine_measure_sheets("MeasureChar/Input Sheet Template.xlsx")

# ========================
### Cleaning 
# TODO move cleaning to backend?
# ========================
#Clean Output
df_clean = df.rename(columns=clean_headers)
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


st.subheader('Scatter Plot')
#make chart from the final of the filters above
scatterchart = df2
# pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()

fig2 = px.scatter(scatterchart, x = "measure_name", y="incremental_cost_per_kwh__mmbtu_saved" ,height=500, width = 1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)

with st.expander("View Data of ScatterPlot:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data = csv, file_name = "ScatterPlot.csv", mime ='text/csv')

# with st.expander("Measure Sheet:"):
#     st.write(linechart.T.style.background_gradient(cmap="Blues"))
#     csv = linechart.to_csv(index=False).encode("utf-8")
#     st.download_button('Download Data', data = csv, file_name = "ScatterPlot.csv", mime ='text/csv')