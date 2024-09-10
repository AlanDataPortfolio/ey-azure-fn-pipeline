import pandas as pd
import os
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder

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

# Encode categorical columns (except 'drivergender') using LabelEncoder
label_encoders = {}
for column in non_numeric_columns:
    if column != 'drivergender':  # Skip 'drivergender' for now
        le = LabelEncoder()
        X[column] = le.fit_transform(X[column].astype(str))
        label_encoders[column] = le  # Save the encoder to decode after SMOTE

# Impute 'drivergender' column (fill NaN with mode for SMOTE processing)
X['drivergender'] = X['drivergender'].fillna(X['drivergender'].mode()[0])

# Apply SMOTE to balance the dataset (both numeric and categorical encoded columns)
smote = SMOTE(sampling_strategy='auto', random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Convert the resampled numeric data back to a DataFrame
X_resampled = pd.DataFrame(X_resampled, columns=X.columns)

# Decode categorical columns back to original form
for column, le in label_encoders.items():
    X_resampled[column] = le.inverse_transform(X_resampled[column].astype(int))

# Round numeric values and convert them to integers
X_resampled[numeric_columns] = X_resampled[numeric_columns].round(0).astype(int)

# Ensure 'drivergender' retains its NaN values
X_resampled['drivergender'] = X_resampled['drivergender'].replace(X['drivergender'].mode()[0], pd.NA)

# Combine resampled data with 'fraud' target
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
