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

# Drop the 'index' column in the synthesized dataset
df3 = df3.drop('index', axis=1)

# Combine the three datasets using concat function
df_concat = pd.concat([df1, df2, df3])

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
