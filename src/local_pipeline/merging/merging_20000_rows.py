import os
import pandas as pd

# Define the base path (working directory)
CWD = os.getcwd()

# Load dataset 1, ensuring 'none' is not treated as NaN
df1 = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'enriched', 'enriched_Dataset1.csv'), na_values=[], keep_default_na=False)

# Load dataset 2, ensuring 'none' is not treated as NaN
df2 = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'enriched', 'enriched_Dataset2.csv'), na_values=[], keep_default_na=False)

# Load dataset 3 (which lacks some columns), ensuring 'none' is not treated as NaN
df3 = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'enriched', 'enriched_Dataset3.csv'), na_values=[], keep_default_na=False)

# Load synthesized data method 1, ensuring 'none' is not treated as NaN
df4 = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'synthesised', 'synthesised_method1.csv'), na_values=[], keep_default_na=False)

# Load synthesized data method 2, ensuring 'none' is not treated as NaN
df5 = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'synthesised', 'synthesised_method2.csv'), na_values=[], keep_default_na=False)

# Drop the index columns in the synthesized datasets 
df4 = df4.drop('index', axis=1, errors='ignore')  # Use errors='ignore' to handle missing index column
df5 = df5.drop('index', axis=1, errors='ignore')

# Combine the datasets using the concat function
df_concat = pd.concat([df1, df2, df3, df4, df5])

# Fill 'none' only for columns that are expected to have 'none' in existing rows,
# but keep other columns where they should remain NaN if not present in the datasets
columns_to_fill_none = ['driverGender', 'accidentType', 'incidentSeverity', 'authoritiesInvolved']

for col in columns_to_fill_none:
    if col in df_concat.columns:
        # Fill only the rows where these columns originally exist, leave the rest as NaN
        df_concat[col] = df_concat[col].where(df_concat[col].notna(), None)

# Set the index to start from 1 and not reset 
df_concat.index = range(1, len(df_concat) + 1)

# Set index name to 'index'
df_concat.index.name = 'index'

# Output file path for the merged dataset
output_file_path = os.path.join(CWD, 'assets', 'data', 'merged', 'merged_20000_rows.csv')

# Ensure the output directory exists
output_dir = os.path.dirname(output_file_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Save the combined dataframe to CSV
df_concat.to_csv(output_file_path, index=True)

print(f"Data merging completed. The merged dataset has been saved to {output_file_path}.")
