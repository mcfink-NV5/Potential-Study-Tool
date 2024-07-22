#%%
### Initialization Script
script_path = '../000_init.py'

with open(script_path, 'r') as f:
    script_code = f.read()

exec(script_code)

# %%
file_path = "PR_Measures.xlsx"

df_measure          = pd.read_excel(file_path, skiprows=31, nrows=18)
    # Generate column headers, e.g., A, B, C, ...
num_columns = df_measure.shape[1]
column_headers = [chr(65 + i) for i in range(num_columns)]  # 65 is ASCII code for 'A'
# Assign the new headers to the DataFrame
df_measure.columns = column_headers

df_measchars        = pd.read_excel(file_path, skiprows=51, nrows=17)
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

df_alt              = pd.read_excel(file_path, skiprows=88, nrows=12)
num_columns = df_alt.shape[1]
column_headers = [chr(65 + i) for i in range(num_columns)] 
df_alt.columns = column_headers
df_water            = pd.read_excel(file_path, skiprows=102, nrows=2)
num_columns = df_water.shape[1]
column_headers = [chr(65 + i) for i in range(num_columns)] 
df_water.columns = column_headers
# %%
