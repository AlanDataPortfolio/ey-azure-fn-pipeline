#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 13:52:38 2024

@author: aasnayemgazzalichowdhury
"""

import pandas as pd
import os 

# Define the base path (Working directory)
CWD = os.getcwd()

# Set the new working directory
new_wdir = '/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/ey-azure-fn-pipeline'
os.chdir(new_wdir)

# Verify the change
print("Current Working Directory:", os.getcwd())

# Load the dataset
df = pd.read_csv(os.path.join(new_wdir, 'assets', 'data', 'normalised', 'merged_20000_rows.csv'))

# Remove rows that contain null values in critical columns only
# Specify critical columns based on the table relationships
critical_columns = ['ClaimsID', 'DriverID', 'InsuranceID', 'IncidentID', 'VehicleID']
df.dropna(subset=critical_columns, inplace=True)

# Split the data into separate DataFrames based on table schema
claims_df = df[['ClaimsID', 'DriverID', 'InsuranceID', 'IncidentID', 'authoritiesInvolved', 'policeReportBool', 'totalClaimAmount', 'fraud', 'VehicleID']].dropna()
drivers_df = df[['DriverID', 'timeAsCustomer', 'driverAge', 'driverGender', 'educationLevel', 'driverExperience', 'licenceType']].dropna()
incidents_df = df[['IncidentID', 'accidentType', 'incidentSeverity', 'incidentTime', 'numVehiclesInvolved', 'numBodilyInjuries']].dropna()
insurance_df = df[['InsuranceID', 'insuranceAccess', 'insurancePremium']].dropna()
vehicles_df = df[['VehicleID', 'vehicleAge']].dropna()

# Define file paths to save each table as CSV
output_dir = '/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/ey-azure-fn-pipeline/assets/data/normalised/'

# Save each table as a separate CSV file with "index" as the first column name
claims_df.to_csv(output_dir + 'claims.csv', index=False)
drivers_df.to_csv(output_dir + 'drivers.csv', index=False)
incidents_df.to_csv(output_dir + 'incidents.csv', index=False)
insurance_df.to_csv(output_dir + 'insurance.csv', index=False)
vehicles_df.to_csv(output_dir + 'vehicles.csv', index=False)

# Confirm the output file paths
output_dir, ['claims.csv', 'drivers.csv', 'incidents.csv','insurance.csv', 'vehicles.csv']