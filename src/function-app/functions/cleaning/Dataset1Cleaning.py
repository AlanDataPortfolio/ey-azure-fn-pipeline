# CLEANING DATSET 1

import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('D:/Documents/PACE_Dev/raw_dataset1.csv')

# Rename columns for clarity and easier access
df.rename(columns={
    'incident_type': 'AccidentType',
    'incident_hour_of_the_day': 'IncidentTime',
    'number_of_vehicles_involved': 'NumVehiclesInvolved',
    'police_report_available': 'PoliceReportBool',
    'insured_sex': 'DriverGender',
    'age': 'DriverAge',
    'insured_education_level': 'EducationLevel',
    'policy_annual_premium': 'InsurancePremium',
    'policy_deductable': 'InsuranceAccess',
    'months_as_customer': 'TimeAsCustomer',
    'fraud_reported': 'Fraud',
    'incident_severity': 'IncidentSeverity',
    'bodily_injuries': 'NumBodilyInjuries',
    'authorities_contacted': 'AuthoritiesInvolved',
    'total_claim_amount': 'TotalClaimAmount',
    'auto_year': 'VehicleYear'
}, inplace=True)

# Clean 'PoliceReportBool' column
df['PoliceReportBool'] = df['PoliceReportBool'].replace({'?': 'NO'})
df['PoliceReportBool'] = df['PoliceReportBool'].map({'YES': 1, 'NO': 0})

# Convert 'DriverGender' to numerical
df['DriverGender'] = df['DriverGender'].map({'MALE': 0, 'FEMALE': 1})

# Convert 'Fraud' to numerical
df['Fraud'] = df['Fraud'].map({'Y': 1, 'N': 0})

# Create 'VehicleAge' column
df['VehicleAge'] = 2015 - df['VehicleYear']

# Drop the 'VehicleYear' column since it is no longer needed
df.drop(columns=['VehicleYear'], inplace=True)

# Create 'DriverExperience' column
np.random.seed(0)  # For reproducibility
df['DriverExperience'] = df['DriverAge'] - 16 - np.random.randint(0, 7, size=len(df))

# Create 'LicenceType' column based on 'DriverExperience'
conditions = [
    (df['DriverExperience'] < 1),
    (df['DriverExperience'] >= 1) & (df['DriverExperience'] < 3),
    (df['DriverExperience'] >= 3) & (df['DriverExperience'] < 5),
    (df['DriverExperience'] >= 5)
]
choices = ['Ls', 'P1', 'P2', 'Full']
df['LicenceType'] = np.select(conditions, choices, default='')

# Handle missing values in 'AuthoritiesInvolved' column
df['AuthoritiesInvolved'] = df['AuthoritiesInvolved'].fillna('None')

# Convert 'InsurancePremium' to whole numbers
df['InsurancePremium'] = df['InsurancePremium'].round(0).astype(int)

# Drop unnecessary columns
columns_to_drop = ['policy_number', 'policy_bind_date', 'policy_state', 'policy_csl', 'umbrella_limit',
                   'insured_zip', 'insured_occupation', 'insured_hobbies', 'insured_relationship',
                   'capital-gains', 'capital-loss', 'incident_date', 'collision_type', 'incident_state',
                   'incident_city', 'incident_location', 'property_damage', 'witnesses', 'injury_claim',
                   'property_claim', 'vehicle_claim', 'auto_make', 'auto_model']
df.drop(columns=columns_to_drop, inplace=True)

# Save the cleaned dataframe to a new CSV file
df.to_csv('D:/Documents/PACE_Dev/cleaned_dataset1.csv', index=False)

print("Data cleaning and transformation completed. The cleaned dataset has been saved to 'D:/Documents/PACE_Dev/cleaned_dataset1.csv'.")
