import pandas as pd
import os

# Define the base path (working directory)
base_path = os.getcwd()

# Load dataset 1 from 'merged_Dataset.csv'
df1 = pd.read_csv(os.path.join(base_path, 'ey-azure-fn-pipeline', 'assets', 'data', 'merged', 'merged_Dataset.csv'))

# Load dataset 2 from 'cleanedEnriched_Dataset2.csv'
df2 = pd.read_csv(os.path.join(base_path, 'ey-azure-fn-pipeline', 'assets', 'data', 'enriched', 'cleanedEnriched_Dataset2.csv'))

# Load synthesized data from 'SynthesisedMethod1.csv'
df3 = pd.read_csv(os.path.join(base_path, 'ey-azure-fn-pipeline', 'assets', 'data', 'synthesised', 'SynthesisedMethod1.csv'))

# Remove any 'index' columns in all datasets before concatenation to avoid duplicates
df1 = df1.drop(columns=['index'], errors='ignore')
df2 = df2.drop(columns=['index'], errors='ignore')
df3 = df3.drop(columns=['index'], errors='ignore')

# Standardize column names to lowercase to avoid duplicate names with different cases
df1.columns = df1.columns.str.lower()
df2.columns = df2.columns.str.lower()
df3.columns = df3.columns.str.lower()

# Combine the three datasets using concat function
df_concat = pd.concat([df1, df2, df3])

# Drop any duplicated columns (that have the same name but contain no data)
df_concat = df_concat.loc[:, ~df_concat.columns.duplicated()]

# Set the index to start from 1 and not reset after 1000
df_concat.index = range(1, len(df_concat) + 1)

# Set index name to 'index'
df_concat.index.name = 'index'

# Define the path for the output file
output_file_path = os.path.join(base_path, 'ey-azure-fn-pipeline', 'assets', 'data', 'merged', 'merged6500.csv')

# Save the combined dataset to the specified path
df_concat.to_csv(output_file_path, index=True)

# Print a statement to indicate the process is done
print(f"Merged data saved to '{output_file_path}'")
