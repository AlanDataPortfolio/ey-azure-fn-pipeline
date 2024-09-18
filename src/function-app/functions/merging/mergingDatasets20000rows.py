import os
import pandas as pd

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative paths to the datasets
base_dir = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data')

# Load dataset 1, ensuring 'none' is not treated as NaN
df1 = pd.read_csv(os.path.join(base_dir, 'enriched', 'cleanedEnriched_Dataset1.csv'), na_values=[], keep_default_na=False)

# Load dataset 2, ensuring 'none' is not treated as NaN
df2 = pd.read_csv(os.path.join(base_dir, 'enriched', 'cleanedEnriched_Dataset2.csv'), na_values=[], keep_default_na=False)

# Load dataset 3, ensuring 'none' is not treated as NaN
df3 = pd.read_csv(os.path.join(base_dir, 'enriched', 'cleanedEnriched_Dataset3.csv'), na_values=[], keep_default_na=False)

# Load synthesized data method 1, ensuring 'none' is not treated as NaN
df4 = pd.read_csv(os.path.join(base_dir, 'synthesised', 'Synthesized_Method1.csv'), na_values=[], keep_default_na=False)

# Load synthesized data method 2, ensuring 'none' is not treated as NaN
df5 = pd.read_csv(os.path.join(base_dir, 'synthesised', 'synthesized_Method2.csv'), na_values=[], keep_default_na=False)

# Drop the index columns in the synthesized datasets 
df4 = df4.drop('index', axis=1, errors='ignore')  # Use errors='ignore' to handle missing index column
df5 = df5.drop('index', axis=1, errors='ignore')

# Combine the datasets using the concat function
df_concat = pd.concat([df1, df2, df3, df4, df5])

# Ensure 'none' values are preserved in all string columns, especially 'authoritiesInvolved'
for col in df_concat.select_dtypes(include=['object']).columns:
    df_concat[col] = df_concat[col].fillna('none')

# Set the index to start from 1 and not reset 
df_concat.index = range(1, len(df_concat) + 1)

# Set index name to 'index'
df_concat.index.name = 'index'

# Output file path for the merged dataset
output_file_path = os.path.join(base_dir, 'merged', 'mergedDataset_20000.csv')

# Ensure the output directory exists
output_dir = os.path.dirname(output_file_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Save the combined dataframe to CSV
df_concat.to_csv(output_file_path, index=True)

print(f"Data merging completed. The merged dataset has been saved to {output_file_path}.")
