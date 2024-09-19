import os
import pandas as pd

# Get the directory of the current script
CWD = os.getcwd()

# Construct the relative path to the input dataset
input_file_path = os.path.join(CWD, 'assets', 'data', 'raw', 'dataset2.csv')

# Load the dataset, ensuring 'none' is not treated as NaN
df = pd.read_csv(input_file_path, na_values=[], keep_default_na=False)

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

# Ensure 'none' values are preserved in 'authoritiesInvolved' column
df_motor['authoritiesInvolved'] = df_motor['authoritiesInvolved'].fillna('none')

# Construct the relative path to the output dataset
output_file_path = os.path.join(CWD, 'assets', 'data', 'cleaned', 'cleaned_dataset2.csv')

# Ensure the output directory exists
output_dir = os.path.dirname(output_file_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Save the cleaned dataset
df_motor.to_csv(output_file_path, index=False)
print(f"Cleaned dataset saved to {output_file_path}.")
