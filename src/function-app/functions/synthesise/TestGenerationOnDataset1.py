import pandas as pd
import numpy as np
import os

# Define the base path (working directory)
base_path = os.getcwd()

# Construct the path to the input dataset (relative to the working directory)
input_file_path = os.path.join(base_path, 'ey-azure-fn-pipeline', 'assets', 'data', 'enriched', 'cleanedEnriched_dataset1.csv')

# Load your original dataset
df = pd.read_csv(input_file_path)

# Set the number of synthetic rows you want to generate
num_samples = 3000

# Generate synthetic data by sampling from the original data's distribution
synthetic_data = df.sample(n=num_samples, replace=True).reset_index(drop=True)

# Optionally, add some noise to numeric columns and ensure no negatives
for column in synthetic_data.select_dtypes(include=[np.number]):
    noise = np.random.normal(0, 0.01, size=synthetic_data[column].shape)
    synthetic_data[column] += noise
    synthetic_data[column] = synthetic_data[column].round()  # Round to nearest whole number
    synthetic_data[column] = synthetic_data[column].clip(lower=0)  # Ensure no negative values

# Construct the path for saving the output CSV file (relative to the working directory)
output_file_path = os.path.join(base_path, 'ey-azure-fn-pipeline', 'assets', 'data', 'synthesised', 'TestSyntheticOnDataset.csv')

# Save the synthetic data to the specified path
synthetic_data.to_csv(output_file_path, index=False)

# Print a statement to indicate the process is done
print(f"Synthetic data generation completed and saved to '{output_file_path}'")
