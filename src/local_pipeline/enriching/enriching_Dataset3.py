# ENRICHING DATASET 3

# IMPORT NECESSARY LIBRARIES
import pandas as pd
import numpy as np
import os

# Load Cleaned Dataset

# Get the directory of the current script
CWD = os.getcwd()

# Construct the relative path to the input dataset
input_file_path = os.path.join(CWD, 'assets', 'data', 'raw', 'cleaned_dataset3.csv')

# Load the dataset
print("Loading cleaned dataset...")
df = pd.read_csv(input_file_path)
print(f"Dataset loaded. Shape: {df.shape}")

# DROP SPECIFIED COLUMNS
columns_to_drop = ['ID', 'KIDSDRIV', 'BIRTH', 'HOMEKIDS', 'YOJ', 'INCOME', 'PARENT1', 'HOME_VAL', 
                   'MSTATUS', 'GENDER', 'OCCUPATION', 'TRAVTIME', 'CAR_USE', 'BLUEBOOK', 'TIF', 
                   'CAR_TYPE', 'RED_CAR', 'OLDCLAIM', 'CLM_FREQ', 'MVR_PTS', 'CLAIM_FLAG', 'URBANICITY']

# Drop the columns
df = df.drop(columns=columns_to_drop)
print(f"Columns dropped. Remaining columns: {df.columns.tolist()}")

# RENAME COLUMNS
print("Renaming columns...")
df.rename(columns={
    'AGE': 'driverAge',
    'EDUCATION': 'educationLevel',
    'CLM_AMT': 'totalClaimAmount',
    'CAR_AGE': 'vehicleAge',
    'REVOKED': 'fraud'
}, inplace=True)

# Convert fraud column to 0 (No) and 1 (Yes)
df['fraud'] = df['fraud'].map({'No': 0, 'Yes': 1})

# Create New Columns

# Assuming 'driverAge' represents the driver's age
print("Generating 'driverExperience' column...")
np.random.seed(0)  # For reproducibility
df['driverExperience'] = df['driverAge'] - 16 - np.random.randint(0, 7, size=len(df))

# Create 'licenceType' column based on 'driverExperience'
print("Generating 'licenceType' column...")
conditions = [
    (df['driverExperience'] < 1),
    (df['driverExperience'] >= 1) & (df['driverExperience'] < 3),
    (df['driverExperience'] >= 3) & (df['driverExperience'] < 5),
    (df['driverExperience'] >= 5)
]
choices = ['Ls', 'P1', 'P2', 'Full']
df['licenceType'] = np.select(conditions, choices, default='')

# Convert Remaining Numeric Columns to Whole Numbers

print("Converting numeric columns to whole numbers...")
numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
df[numeric_cols] = df[numeric_cols].round(0).astype(int)

# REARRANGE COLUMNS
column_order = [
    'timeAsCustomer', 'driverAge', 'insuranceAccess', 'insurancePremium', 'driverGender', 'educationLevel',
    'accidentType', 'incidentSeverity', 'authoritiesInvolved', 'incidentTime', 'numVehiclesInvolved',
    'numBodilyInjuries', 'policeReportBool', 'totalClaimAmount', 'fraud', 'vehicleAge',
    'driverExperience', 'licenceType'
]

# Only keep columns that exist in the current dataframe
column_order = [col for col in column_order if col in df.columns]

df = df[column_order]

# Save the Enriched Dataset

# Construct the relative path to the output dataset
output_file_path = os.path.join(CWD, 'enriched_dataset3.csv')

# Ensure the output directory exists
output_dir = os.path.dirname(output_file_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Save enriched dataset
df.to_csv(output_file_path, index=False)
print(f"Enriched dataset saved to {output_file_path}.")
