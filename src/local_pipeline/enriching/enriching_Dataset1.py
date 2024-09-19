import os
import pandas as pd
import numpy as np

# Get the directory of the current script
CWD = os.getcwd()

# Construct the relative path to the input dataset
input_file_path = os.path.join(CWD, 'assets', 'data', 'raw', 'cleaned_dataset1.csv')

# Load the cleaned dataset, ensuring 'none' is not treated as NaN
df = pd.read_csv(input_file_path, na_values=[], keep_default_na=False)

# Convert 'policeReportBool' column to numerical
df['policeReportBool'] = df['policeReportBool'].map({'YES': 1, 'NO': 0})

# Convert 'driverGender' to numerical
df['driverGender'] = df['driverGender'].map({'MALE': 0, 'FEMALE': 1})

# Convert 'fraud' to numerical
df['fraud'] = df['fraud'].map({'Y': 1, 'N': 0})

# Create 'vehicleAge' column
df['vehicleAge'] = 2015 - df['vehicleYear']

# Drop the 'vehicleYear' column since it is no longer needed
df.drop(columns=['vehicleYear'], inplace=True)

# Create 'driverExperience' column
np.random.seed(0)  # For reproducibility
df['driverExperience'] = df['driverAge'] - 16 - np.random.randint(0, 7, size=len(df))

# Create 'licenceType' column based on 'driverExperience'
conditions = [
    (df['driverExperience'] < 1),
    (df['driverExperience'] >= 1) & (df['driverExperience'] < 3),
    (df['driverExperience'] >= 3) & (df['driverExperience'] < 5),
    (df['driverExperience'] >= 5)
]
choices = ['Ls', 'P1', 'P2', 'Full']
df['licenceType'] = np.select(conditions, choices, default='')

# Convert 'insurancePremium' to whole numbers
df['insurancePremium'] = df['insurancePremium'].round(0).astype(int)

# Ensure 'none' is preserved in 'authoritiesInvolved' column
df['authoritiesInvolved'] = df['authoritiesInvolved'].fillna('none')

# Drop unnecessary columns
columns_to_drop = ['policy_number', 'policy_bind_date', 'policy_state', 'policy_csl', 'umbrella_limit',
                   'insured_zip', 'insured_occupation', 'insured_hobbies', 'insured_relationship',
                   'capital-gains', 'capital-loss', 'incident_date', 'collision_type', 'incident_state',
                   'incident_city', 'incident_location', 'property_damage', 'witnesses', 'injury_claim',
                   'property_claim', 'vehicle_claim', 'auto_make', 'auto_model']
df.drop(columns=columns_to_drop, inplace=True)

# Save the Enriched Dataset

# Construct the relative path to the output dataset
output_file_path = os.path.join(CWD, 'enriched_dataset1.csv')

# Ensure the output directory exists
output_dir = os.path.dirname(output_file_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Save enriched dataset
df.to_csv(output_file_path, index=False)
print(f"Enriched dataset saved to {output_file_path}.")
