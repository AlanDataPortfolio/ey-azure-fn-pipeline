# Merging 20000

import os
import pandas as pd

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct relative paths to the input datasets
input_file_path1 = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'enriched', 'cleanedEnriched_Dataset1.csv')
input_file_path2 = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'enriched', 'cleanedEnriched_Dataset2.csv')
input_file_path3 = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'enriched', 'cleanedEnriched_Dataset3.csv')
input_file_path4 = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'synthesised', 'SynthesisedMethod1.csv')
input_file_path5 = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'synthesised', 'synthesized_Method2.csv')

# Load the datasets
df1 = pd.read_csv(input_file_path1)
df2 = pd.read_csv(input_file_path2)
df3 = pd.read_csv(input_file_path3)
df4 = pd.read_csv(input_file_path4)
df5 = pd.read_csv(input_file_path5)

# Drop the index columns in the synthesized datasets, if present
df4 = df4.drop('index', axis=1, errors='ignore')
df5 = df5.drop('index', axis=1, errors='ignore')

# Combine the datasets using the concat function
df_concat = pd.concat([df1, df2, df3, df4, df5])

# Set the index to start from 1 and not reset
df_concat.index = range(1, len(df_concat) + 1)

# Set index name to 'index'
df_concat.index.name = 'index'

# Construct the relative path to the output file
output_file_path = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'merged', 'mergedDataset_20000.csv')

# Ensure the output directory exists
output_dir = os.path.dirname(output_file_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Save the merged dataframe to the output CSV file
df_concat.to_csv(output_file_path, index=True)

print(f"Data merging completed. The merged dataset has been saved to {output_file_path}.")
