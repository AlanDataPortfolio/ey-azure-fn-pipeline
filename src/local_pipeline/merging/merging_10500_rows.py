# Merging to 10500


import os
import pandas as pd

# Define the base path (working directory)
CWD = os.getcwd()

# Load dataset 1 (cleanedEnriched_Dataset1)
df1 = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'enriched', 'enriched_dataset1.csv'), na_values=[], keep_default_na=False)

# Load dataset 2 (cleanedEnriched_Dataset2)
df2 = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'enriched', 'enriched_dataset2.csv'), na_values=[], keep_default_na=False)

# Load synthesized data method 1 (synthesized_Method1)
df3 = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'synthesised', 'synthesised_method1.csv'), na_values=[], keep_default_na=False)

# Load synthesized data method 2 (synthesized_Method2)
df4 = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'synthesised', 'synthesised_method2.csv'), na_values=[], keep_default_na=False)

# Drop the 'driverGender' and 'index' columns from all datasets (if they exist)
columns_to_drop = ['driverGender', 'index']

df1 = df1.drop(columns=columns_to_drop, errors='ignore')
df2 = df2.drop(columns=columns_to_drop, errors='ignore')
df3 = df3.drop(columns=columns_to_drop, errors='ignore')
df4 = df4.drop(columns=columns_to_drop, errors='ignore')

# Combine the datasets using the concat function
df_concat = pd.concat([df1, df2, df3, df4])

# Set the index to start from 1 and not reset
df_concat.index = range(1, len(df_concat) + 1)

# Set index name to 'index'
df_concat.index.name = 'index'

# Output file path for the merged dataset
output_file_path = os.path.join(CWD, 'assets', 'data', 'merged', 'merged_10500_rows.csv')

# Ensure the output directory exists
output_dir = os.path.dirname(output_file_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Save the combined dataframe to CSV
df_concat.to_csv(output_file_path, index=True)

# Print a statement to indicate the process is done
print(f"Data merging completed and saved to '{output_file_path}'.")
