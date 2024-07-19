#%%
### INitialization Script
script_path = '../000_init.py'

with open(script_path, 'r') as f:
    script_code = f.read()

exec(script_code)

# %%
