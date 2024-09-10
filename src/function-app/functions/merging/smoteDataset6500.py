import pandas as pd
import os
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer

# Get the current directory of the script (within the Git repo)
script_dir = os.path.dirname(os.path.abspath(__file__))

# Define the relative path for the input file
input_file_path = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'merged', 'merged6500.csv')

# Load the merged dataset
df = pd.read_csv(input_file_path)

# Check the count of fraud (1) and non-fraud (0) rows
fraud_count = df['fraud'].value_counts()
print(f"Fraud count (0 = non-fraud, 1 = fraud):\n{fraud_count}")

# Save the original dataset
original_df = df.copy()

# Separate features and target ('fraud')
X = df.drop(columns=['fraud'])  # Drop only the 'fraud' column before applying SMOTE
y = df['fraud']  # 'fraud' column (target)

# Separate numeric and non-numeric columns
numeric_columns = X.select_dtypes(include=['number']).columns
non_numeric_columns = X.select_dtypes(exclude=['number']).columns

# Impute missing values in numeric columns with the mean
imputer = SimpleImputer(strategy='mean')
X_numeric_imputed = imputer.fit_transform(X[numeric_columns])

# Apply SMOTE only on numeric data
smote = SMOTE(sampling_strategy='auto', random_state=42)
X_numeric_resampled, y_resampled = smote.fit_resample(X_numeric_imputed, y)

# Convert the resampled numeric data back to a DataFrame
X_numeric_resampled = pd.DataFrame(X_numeric_resampled, columns=numeric_columns)

# Round numeric values and convert them to integers
X_numeric_resampled = X_numeric_resampled.round(0).astype(int)

# For non-numeric (categorical) data, replicate the original pattern
X_categorical_resampled = pd.DataFrame()

# Replicate the original pattern for each non-numeric column except 'drivergender'
for column in non_numeric_columns:
    if column != 'drivergender':  # Skip 'drivergender' for now
        X_categorical_resampled[column] = X[column].sample(n=len(X_numeric_resampled), replace=True).reset_index(drop=True)

# For the 'drivergender' column, preserve the original distribution of 0s, 1s, and NaNs
drivergender_resampled = df['drivergender'].sample(
    n=len(X_numeric_resampled), 
    replace=True, 
    weights=df['drivergender'].value_counts(normalize=True, dropna=False)
).reset_index(drop=True)

# Add 'drivergender' to the categorical columns
X_categorical_resampled['drivergender'] = drivergender_resampled

# Combine resampled numeric and categorical data
X_resampled = pd.concat([X_numeric_resampled.reset_index(drop=True), X_categorical_resampled], axis=1)

# Add 'fraud' target back to the resampled data
df_resampled = pd.DataFrame(X_resampled)
df_resampled['fraud'] = y_resampled

# Ensure both datasets have the same columns
df_resampled = df_resampled[original_df.columns]

# Reset the index of both the original and resampled datasets
original_df.reset_index(drop=True, inplace=True)
df_resampled.reset_index(drop=True, inplace=True)

# Combine original dataset and SMOTE-generated dataset
final_df = pd.concat([original_df, df_resampled], ignore_index=True)

# Set the index to start from 1
final_df.index = range(1, len(final_df) + 1)
final_df.index.name = 'index'

# Define the relative path for the output file
output_file_path = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'merged', 'smote6500dataset.csv')

# Save the final dataset (original + SMOTE-generated) to the specified path
final_df.to_csv(output_file_path, index=True)

# Print a statement to indicate the process is done
print(f"Balanced dataset saved to '{output_file_path}'")
