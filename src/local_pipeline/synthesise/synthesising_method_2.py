import os
import pandas as pd
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer
from sdv.evaluation.single_table import evaluate_quality

# Get the directory of the current script
CWD = os.getcwd()

# Construct the relative path to the input dataset
input_file_path = os.path.join(CWD, 'assets', 'data', 'merged', 'merged_dataset_1_2.csv')

# Load your original dataset
df = pd.read_csv(input_file_path)

# Define the metadata for the dataset
metadata = SingleTableMetadata()

# Correct the argument passed to detect_from_csv by providing the input file path
metadata.detect_from_csv(filepath=input_file_path)

# Define the synthesizer
synthesizer = CTGANSynthesizer(
    metadata,
    enforce_rounding=False,
    epochs=1800,
    verbose=True
)

# Fit the synthesizer with the dataset
synthesizer.fit(df)

# Generate synthetic data
synthetic_data = synthesizer.sample(num_rows=4000)

# Convert synthetic data to a DataFrame
synthetic_df = pd.DataFrame(synthetic_data)

# Reset the index to ensure it starts from 1
synthetic_df.reset_index(drop=True, inplace=True)

# Set the index to range from 1 to 3001
synthetic_df['index'] = synthetic_df.index = range(1, len(synthetic_df) + 1)

# Evaluate the quality of the synthetic data
quality_report = evaluate_quality(
    real_data=df,
    synthetic_data=synthetic_data,
    metadata=metadata
)

# Construct the path for saving the output CSV file (relative to the working directory)
output_file_path = os.path.join(CWD, 'assets', 'data', 'synthesised', 'synthesised_method2.csv')

# Save the synthetic data to the specified path
synthetic_df.to_csv(output_file_path, index=False)

# Print a statement to indicate the process is done
print(f"Synthetic data generation completed and saved to '{output_file_path}'")
