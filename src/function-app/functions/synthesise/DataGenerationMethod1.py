# Generating Synthetic Data (method 1) based on merged dataset
import pandas as pd
import numpy as np
import os

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the relative path to the merged dataset
input_file_path = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'merged', 'merged_Dataset.csv')

# Load your original dataset
df = pd.read_csv(input_file_path)

# Ensure that 'authoritiesInvolved' contains no blanks or NaN values
df['authoritiesInvolved'] = df['authoritiesInvolved'].replace('', 'none').fillna('none')

# **Optional: Verify that there are no missing values in 'authoritiesInvolved'**
print("Unique values in 'authoritiesInvolved' after cleaning:", df['authoritiesInvolved'].unique())
print("Number of missing 'authoritiesInvolved' in df:", df['authoritiesInvolved'].isna().sum())

# Set the number of synthetic rows you want to generate
num_samples = 4000

# Generate synthetic data by sampling from the original data's distribution (excluding the 'fraud' column)
columns_to_sample = df.columns.difference(['fraud'])
synthetic_data = df[columns_to_sample].sample(n=num_samples, replace=True, random_state=0).reset_index(drop=True)

# Add the 'fraud' column back without modification
synthetic_data['fraud'] = df['fraud'].sample(n=num_samples, replace=True, random_state=0).reset_index(drop=True)

# **Ensure 'authoritiesInvolved' in synthetic_data is cleaned in case of any reintroduced missing values**
synthetic_data['authoritiesInvolved'] = synthetic_data['authoritiesInvolved'].replace('', 'none').fillna('none')

# **Optional: Verify that there are no missing values in 'authoritiesInvolved' in synthetic_data**
print("Unique values in 'authoritiesInvolved' in synthetic_data after cleaning:", synthetic_data['authoritiesInvolved'].unique())
print("Number of missing 'authoritiesInvolved' in synthetic_data:", synthetic_data['authoritiesInvolved'].isna().sum())

# Optionally, add some noise to numeric columns (excluding 'fraud') and ensure no negatives
for column in synthetic_data.select_dtypes(include=[np.number]).columns.difference(['fraud']):
    noise = np.random.normal(0, 0.01, size=synthetic_data[column].shape)
    synthetic_data[column] += noise
    synthetic_data[column] = synthetic_data[column].round()  # Round to nearest whole number
    synthetic_data[column] = synthetic_data[column].clip(lower=0)  # Ensure no negative values

# Construct the path for saving the enriched output CSV file
output_file_path = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'synthesised', 'synthesized_Method1.csv')

# Save the synthetic data to the specified path
synthetic_data.to_csv(output_file_path, index=False)

# Print a statement to indicate the process is done
print(f"Synthetic data generation completed and saved to '{output_file_path}'")
