#%%
### Initialization Script
script_path = '../000_init.py'

with open(script_path, 'r') as f:
    script_code = f.read()

exec(script_code)

# %%

# #to upload a file
# fl = st.file_uploader(":file_folder: Upload a file",type=(["csv","txt","xlsx","xls"]))
# if fl is not None:
#     filename = fl.name
#     st.write(filename)
#     df = combine_excel_sheets(filename)
# else:
#     os.chdir(r"C:\Users\AndrewJ.Johnson\OneDrive - NV5\Documents\GitHub\Streamlit")
df = combine_measure_sheets("PR_Measures.xlsx")


# %%
#clean headers
df_clean = df.rename(columns=clean_headers)
df_clean
# %%
