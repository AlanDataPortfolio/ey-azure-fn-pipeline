#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 14:52:22 2024

@author: aasnayemgazzalichowdhury
"""

import pandas as pd
import numpy as np

# Load the dataset
df = pd.read_csv('/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/Cleaning/cleaned_dataset2.csv')

# Add empty column for DriverGender
df['DriverGender'] = np.nan

# Change ClaimStatus column to Fraud
# Convert 'A' to 0 and 'D' to 1
df['Fraud'] = df['ClaimStatus'].map({'A':0, 'D':1}) #Approved is not fraudulent and Denied is fraudulent

# Define Distribution of AccidentType
accident_type_distribution = {
    'Multi-vehicle Collision': 0.419,
    'Single Vehicle Collision': 0.403,
    'Vehicle Theft': 0.094,
    'Parked Car': 0.084
}

np.random.seed(0)  # For reproducibility

# Generate AccidentType based on the distribution
df['AccidentType'] = np.random.choice(
    list(accident_type_distribution.keys()),
    size=len(df),
    p=list(accident_type_distribution.values())
)

# Define Distribution of NumVehiclesInvolved
def distribution_num_vehicles_involved(accident_type):
    if accident_type == 'Multi-vehicle Collision':
        return np.random.normal(3, 0.38)
    else:
        return 1

# Generate NumVehiclesInvolved based on the distribution
df['NumVehiclesInvolved'] = df['AccidentType'].apply(lambda x: distribution_num_vehicles_involved(x)).round().astype(int)

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
df['VehicleAge'] = np.random.choice(
    list(vehicle_age_distribution.keys()),
    size=len(df),
    p=list(vehicle_age_distribution.values())
).astype(int)

# Define Distribution of InsuranceAccess
insurance_access_distribution = {
    500: 0.342,
    1000: 0.351,
    2000: 0.307
}

# Generate InsuranceAccess based on the distribution
df['InsuranceAccess'] = np.random.choice(
    list(insurance_access_distribution.keys()),
    size=len(df),
    p=list(insurance_access_distribution.values())
)

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

# Drop unwanted columns
df = df.drop(['TXN_DATE_TIME', 'TRANSACTION_ID', 'CUSTOMER_ID', 'POLICY_NUMBER',
                          'POLICY_EFF_DT', 'LOSS_DT', 'REPORT_DT', 'INSURANCE_TYPE',
                          'CUSTOMER_NAME', 'ADDRESS_LINE1', 'ADDRESS_LINE2', 'CITY', 'STATE',
                          'POSTAL_CODE', 'SSN', 'MARITAL_STATUS', 'EMPLOYMENT_STATUS', 'NO_OF_FAMILY_MEMBERS',
                          'RISK_SEGMENTATION', 'HOUSE_TYPE', 'SOCIAL_CLASS', 'ROUTING_NUMBER', 'ACCT_NUMBER',
                          'INCIDENT_STATE', 'INCIDENT_CITY', 'AGENT_ID', 'VENDOR_ID'], axis=1)


# Reorder columns
df = df[['TimeAsCustomer', 'DriverAge', 'InsuranceAccess', 'InsurancePremium', 'DriverGender', 'EducationLevel', 'AccidentType', 'IncidentSeverity', 'AuthoritiesInvolved', 'IncidentTime', 'NumVehiclesInvolved', 'NumBodilyInjuries', 'PoliceReportBool', 'TotalClaimAmount', 'Fraud', 'VehicleAge', 'DriverExperience', 'LicenceType']]

# Save the cleaned dataframe to a new CSV file
df.to_csv('/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/Enriching/cleanedEnriched_Dataset2.csv', index=False)

print("Data processing completed. The cleaned dataset has been saved to the relevant folder'.")
