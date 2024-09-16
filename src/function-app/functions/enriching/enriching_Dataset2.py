import os
import pandas as pd
import numpy as np

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the relative path to the cleaned dataset
input_file_path = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'cleaned', 'cleaned_dataset2.csv')

# Load the cleaned dataset
df_motor = pd.read_csv(input_file_path)

# Multiply the InsurancePremium column by 12
df_motor['insurancePremium'] *= 12

# Round InsurancePremium to whole numbers
df_motor['insurancePremium'] = df_motor['insurancePremium'].round().astype(int)

# Add empty column for DriverGender
df_motor['driverGender'] = np.nan

# Define Distribution of AccidentType
accident_type_distribution = {
    'Multi-vehicle Collision': 0.419,
    'Single Vehicle Collision': 0.403,
    'Vehicle Theft': 0.094,
    'Parked Car': 0.084
}

np.random.seed(0)  # For reproducibility

# Generate AccidentType based on the distribution
df_motor['accidentType'] = np.random.choice(
    list(accident_type_distribution.keys()),
    size=len(df_motor),
    p=list(accident_type_distribution.values())
)

# Define Distribution of NumVehiclesInvolved
def distribution_num_vehicles_involved(accident_type):
    if accident_type == 'Multi-vehicle Collision':
        return np.random.normal(3, 0.38)
    else:
        return 1

# Generate NumVehiclesInvolved based on the distribution
df_motor['numVehiclesInvolved'] = df_motor['accidentType'].apply(lambda x: distribution_num_vehicles_involved(x)).round().astype(int)


# Define Distribution of VehicleAge
vehicle_age_distribution = {
    '0': 0.047,
    '1': 0.044,
    '2': 0.049,
    '3': 0.046,
    '4': 0.053,
    '5': 0.050,
    '6': 0.050,
    '7': 0.045,
    '8': 0.052,
    '9': 0.053,
    '10': 0.054,
    '11': 0.039,
    '12': 0.051,
    '13': 0.049,
    '14': 0.042,
    '15': 0.042,
    '16': 0.055,
    '17': 0.040,
    '18': 0.046,
    '19': 0.037,
    '20': 0.056,
}

# Generate VehicleAge based on the distribution
df_motor['vehicleAge'] = np.random.choice(
    list(vehicle_age_distribution.keys()),
    size=len(df_motor),
    p=list(vehicle_age_distribution.values())
).astype(int)

# Define Distribution of InsuranceAccess
insurance_access_distribution = {
    500: 0.342,
    1000: 0.351,
    2000: 0.307
}

# Generate InsuranceAccess based on the distribution
df_motor['insuranceAccess'] = np.random.choice(
    list(insurance_access_distribution.keys()),
    size=len(df_motor),
    p=list(insurance_access_distribution.values())
)

# Create 'DriverExperience' column
np.random.seed(0)  # For reproducibility
  
df_motor['driverExperience'] = df_motor['driverAge'] - 16 - np.random.randint(0, 7, size=len(df_motor))

# Create 'LicenceType' column based on 'DriverExperience'
conditions = [
    (df_motor['driverExperience'] < 1),
    (df_motor['driverExperience'] >= 1) & (df_motor['driverExperience'] < 3),
    (df_motor['driverExperience'] >= 3) & (df_motor['driverExperience'] < 5),
    (df_motor['driverExperience'] >= 5)
]
choices = ['Ls', 'P1', 'P2', 'Full']
df_motor['licenceType'] = np.select(conditions, choices, default='')

# Construct the path for saving the enriched output CSV file
output_file_path = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'enriched', 'cleanedEnriched_dataset2.csv')

# Save the enriched dataframe to the output CSV file
df_motor.to_csv(output_file_path, index=False)

print("Data enrichment completed. The enriched dataset has been saved to 'cleanedEnriched_dataset2.csv'.")

