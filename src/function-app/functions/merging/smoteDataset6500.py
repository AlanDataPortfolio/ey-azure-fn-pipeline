import pandas as pd
import os
from imblearn.over_sampling import SMOTE

# Define the global path for the input file
input_file_path = r'C:\Users\Nooru\Documents\PACE\ey-azure-fn-pipeline\assets\data\merged\merged6500.csv'

# Load the merged dataset
df = pd.read_csv(input_file_path)

# Check the count of fraud (1) and non-fraud (0) rows
fraud_count = df['fraud'].value_counts()
print(f"Fraud count (0 = non-fraud, 1 = fraud):\n{fraud_count}")

# Separate features and target ('fraud')
X = df.drop(columns=['fraud'])  # All columns except 'fraud'
y = df['fraud']  # 'fraud' column (target)

# Apply SMOTE to balance fraud and non-fraud classes
smote = SMOTE(sampling_strategy='auto', random_state=42)  # 'auto' makes both classes equal
X_resampled, y_resampled = smote.fit_resample(X, y)

# Combine resampled features and target into a new DataFrame
df_resampled = pd.DataFrame(X_resampled, columns=X.columns)
df_resampled['fraud'] = y_resampled  # Add the target column back

# Set the index to start from 1
df_resampled.index = range(1, len(df_resampled) + 1)

# Set index name to 'index'
df_resampled.index.name = 'index'

# Define the global path for the output file
output_file_path = r'C:\Users\Nooru\Documents\PACE\ey-azure-fn-pipeline\assets\data\merged\smote6500dataset.csv'

# Save the resampled dataset to the specified path
df_resampled.to_csv(output_file_path, index=True)

# Print a statement to indicate the process is done
print(f"Balanced dataset saved to '{output_file_path}'")
