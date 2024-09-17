import os
import pandas as pd 
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer
from sdv.evaluation.single_table import evaluate_quality

# Define the base path (working directory)
base_path = os.getcwd()

# Construct the path to the input dataset (relative to the working directory)
input_file_path = os.path.join(base_path, 'ey-azure-fn-pipeline', 'assets', 'data', 'merged', 'merged_Dataset.csv')

# Load your original dataset
df = pd.read_csv(input_file_path)

# Define the metadeta for the dataset
metadata = SingleTableMetadata()

metadata.detect_from_csv(filepath='/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/Merging/merged_Dataset.csv')

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

# Convert synthetic data to the df
synthetic_df = pd.DataFrame(synthetic_data)

# Reset the index to ensure it starts from 1
synthetic_df.reset_index(drop=True, inplace=True)

# Set the index to range from 1 to 3001
synthetic_df['index'] = synthetic_df.index = range(1, len(synthetic_df) + 1)

quality_report = evaluate_quality(
    real_data=df,
    synthetic_data=synthetic_data,
    metadata=metadata)

# Spit out the file
synthetic_df.to_csv('/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/Synthesizing/synthesized_Method2.csv',index=False)