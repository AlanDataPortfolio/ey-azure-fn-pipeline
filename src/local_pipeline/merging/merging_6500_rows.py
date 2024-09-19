import pandas as pd
import os

# Define the base path (working directory)
CWD = os.getcwd()

# Load dataset 1 from 'merged_Dataset.csv'
df1 = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'merged', 'merged_dataset_1_2.csv'))

# Load synthesized data from 'SynthesisedMethod1.csv'
df2 = pd.read_csv(os.path.join(CWD, 'assets', 'data', 'synthesised', 'synthesised_method1.csv'))

# Remove any 'index' columns in both datasets before concatenation to avoid duplicates
df1 = df1.drop(columns=['index'], errors='ignore')
df2 = df2.drop(columns=['index'], errors='ignore')

# Standardize column names to lowercase to avoid duplicate names with different cases
df1.columns = df1.columns.str.lower()
df2.columns = df2.columns.str.lower()

# Combine the two datasets using concat function
df_concat = pd.concat([df1, df2])

# Drop any duplicated columns (that have the same name but contain no data)
df_concat = df_concat.loc[:, ~df_concat.columns.duplicated()]

# Set the index to start from 1 and not reset after 1000
df_concat.index = range(1, len(df_concat) + 1)

# Set index name to 'index'
df_concat.index.name = 'index'

# Define the path for the output file
output_file_path = os.path.join(CWD, 'assets', 'data', 'merged', 'merged_6500_rows.csv')

# Save the combined dataset to the specified path
df_concat.to_csv(output_file_path, index=True)

# Print a statement to indicate the process is done
print(f"Merged data saved to '{output_file_path}'")
