# Generating Synthethic Data (method 1) based on merged datset
import pandas as pd
import numpy as np
import os

# Define the base path (working directory)
base_path = os.getcwd()

# Construct the path to the input dataset (relative to the working directory)
input_file_path = os.path.join(base_path, 'ey-azure-fn-pipeline', 'assets', 'data', 'merged', 'merged_Dataset.csv')

# Load your original dataset
df = pd.read_csv(input_file_path)

# Set the number of synthetic rows you want to generate
num_samples = 4000

# Generate synthetic data by sampling from the original data's distribution (excluding the 'fraud' column)
columns_to_sample = df.columns.difference(['fraud'])
synthetic_data = df[columns_to_sample].sample(n=num_samples, replace=True).reset_index(drop=True)

# Add the original 'fraud' column back without modification
synthetic_data['fraud'] = df['fraud'].sample(n=num_samples, replace=True).reset_index(drop=True)

# Optionally, add some noise to numeric columns (excluding 'fraud') and ensure no negatives
for column in synthetic_data.select_dtypes(include=[np.number]).columns.difference(['fraud']):
    noise = np.random.normal(0, 0.01, size=synthetic_data[column].shape)
    synthetic_data[column] += noise
    synthetic_data[column] = synthetic_data[column].round()  # Round to nearest whole number
    synthetic_data[column] = synthetic_data[column].clip(lower=0)  # Ensure no negative values

# Construct the path for saving the output CSV file (relative to the working directory)
output_file_path = os.path.join(base_path, 'ey-azure-fn-pipeline', 'assets', 'data', 'synthesised', 'SynthesisedMethod1.csv')

# Save the synthetic data to the specified path
synthetic_data.to_csv(output_file_path, index=False)

# Print a statement to indicate the process is done
print(f"Synthetic data generation completed and saved to '{output_file_path}'")
