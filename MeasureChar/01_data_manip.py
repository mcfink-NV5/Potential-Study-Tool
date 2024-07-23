#%%
### Initialization Script
script_path = '../000_init.py'

with open(script_path, 'r') as f:
    script_code = f.read()

exec(script_code)

# %%
df_measure = combine_measure_sheets_test("Test_Measures.xlsx")

# %%
#Clean Output
df_clean = df_measure.rename(columns=clean_headers)
df_clean = df_clean.dropna(how='all')
#there is bad raw data I am guessing


# #remove these odd rows
mask = df_clean == '-'
# Count the number of '-' in each row
count_dashes = mask.sum(axis=1)
# Remove rows where the count of '-' is more than 1
df_clean = df_clean[count_dashes <= 1]


# %%
