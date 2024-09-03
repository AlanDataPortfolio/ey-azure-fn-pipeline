import os
import pandas as pd

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the relative path to the input dataset
input_file_path = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'raw', 'dataset1.csv')

# Load the dataset
df = pd.read_csv(input_file_path)

# Rename columns for clarity and easier access (using camelCase)
df.rename(columns={
    'incident_type': 'accidentType',
    'incident_hour_of_the_day': 'incidentTime',
    'number_of_vehicles_involved': 'numVehiclesInvolved',
    'police_report_available': 'policeReportBool',
    'insured_sex': 'driverGender',
    'age': 'driverAge',
    'insured_education_level': 'educationLevel',
    'policy_annual_premium': 'insurancePremium',
    'policy_deductable': 'insuranceAccess',
    'months_as_customer': 'timeAsCustomer',
    'fraud_reported': 'fraud',
    'incident_severity': 'incidentSeverity',
    'bodily_injuries': 'numBodilyInjuries',
    'authorities_contacted': 'authoritiesInvolved',
    'total_claim_amount': 'totalClaimAmount',
    'auto_year': 'vehicleYear'
}, inplace=True)

# Handle missing values
df['policeReportBool'] = df['policeReportBool'].replace({'?': 'NO'})
df['authoritiesInvolved'] = df['authoritiesInvolved'].fillna('None')

# Construct the path for saving the output CSV file
output_file_path = os.path.join(script_dir, 'cleaned_dataset1.csv')

# Save the cleaned dataframe to the output CSV file
df.to_csv(output_file_path, index=False)

print("Data cleaning completed. The cleaned dataset has been saved to 'cleaned_dataset1.csv'.")
