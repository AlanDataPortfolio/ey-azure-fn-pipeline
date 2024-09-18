import os
import pandas as pd

# Construct the absolute path to the input dataset on the D: drive
input_file_path = 'D:/Documents/GitHub/PACE/ey-azure-fn-pipeline/assets/data/raw/dataset2.csv'

# Load the dataset
df = pd.read_csv(input_file_path)

# Filter for motor claims
df_motor = df.loc[df["INSURANCE_TYPE"] == "Motor"].copy()

# Fill in null values with the lowest degree for EducationLevel
df_motor['CUSTOMER_EDUCATION_LEVEL'] = df_motor['CUSTOMER_EDUCATION_LEVEL'].fillna('High School')

# Rename the columns for clarity using camelCase
df_motor.rename(columns={
    'TENURE': 'timeAsCustomer',
    'INCIDENT_HOUR_OF_THE_DAY': 'incidentTime',
    'POLICE_REPORT_AVAILABLE': 'policeReportBool',
    'AGE': 'driverAge',
    'CUSTOMER_EDUCATION_LEVEL': 'educationLevel',
    'PREMIUM_AMOUNT': 'insurancePremium',
    'INCIDENT_SEVERITY': 'incidentSeverity',
    'ANY_INJURY': 'numBodilyInjuries',
    'AUTHORITY_CONTACTED': 'authoritiesInvolved',
    'CLAIM_AMOUNT': 'totalClaimAmount',
    'CLAIM_STATUS': 'claimStatus',
}, inplace=True)

# Construct the absolute path for saving the cleaned output CSV file on the D: drive
output_file_path = 'D:/Documents/GitHub/PACE/ey-azure-fn-pipeline/assets/data/cleaned/cleaned_dataset2.csv'

# Ensure proper casing when saving the file
df_motor.to_csv(output_file_path, index=False)

print("Data cleaning completed. The cleaned dataset has been saved to 'cleaned_dataset2.csv'.")
