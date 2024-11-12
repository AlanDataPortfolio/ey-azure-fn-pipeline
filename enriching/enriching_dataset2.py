import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import os
import numpy as np

bp = func.Blueprint('enriching_dataset2')

@bp.function_name("enriching_dataset2")
@bp.route(route="enriching_dataset2")
def enriching_dataset2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Step 1: Retrieve the Blob Storage connection string from environment variables
    connection_string = os.getenv("AzureWebJobsStorage")
    
    # Define container and blob names
    source_container_name = "silver"
    source_blob_name = "cleaned/dataset2.csv"
    destination_container_name = "silver"
    destination_blob_name = "enriched/dataset_2.csv"

    try:
        # Step 2: Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Step 3: Download the CSV from the "bronze" container
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name)
        downloaded_blob = blob_client.download_blob()
        blob_data = downloaded_blob.readall()

        # Step 4: Load the dataset into a pandas DataFrame (in-memory)
        df = pd.read_csv(io.BytesIO(blob_data), na_values=[], keep_default_na=False)

        # Multiply the InsurancePremium column by 12
        df['insurancePremium'] *= 12

        # Round InsurancePremium to whole numbers
        df['insurancePremium'] = df['insurancePremium'].round().astype(int)

        # Add empty column for DriverGender
        df['driverGender'] = np.nan

        # Define Distribution of AccidentType
        accident_type_distribution = {
            'Multi-vehicle Collision': 0.419,
            'Single Vehicle Collision': 0.403,
            'Vehicle Theft': 0.094,
            'Parked Car': 0.084
        }

        np.random.seed(0)  # For reproducibility

        # Generate AccidentType based on the distribution
        df['accidentType'] = np.random.choice(
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

        # Map 'claimStatus' to Fraud (1) and Not Fraud (0)
        df_motor['fraud'] = df_motor['claimStatus'].map({'A': 0, 'D': 1})

        # Ensure 'none' is preserved in 'authoritiesInvolved' column
        df_motor['authoritiesInvolved'] = df_motor['authoritiesInvolved'].fillna('none')

        # Select only the required columns
        required_columns = [
            'timeAsCustomer', 'driverAge', 'insuranceAccess', 'insurancePremium', 'driverGender',
            'educationLevel', 'accidentType', 'incidentSeverity', 'authoritiesInvolved',
            'incidentTime', 'numVehiclesInvolved', 'numBodilyInjuries', 'policeReportBool',
            'totalClaimAmount', 'fraud', 'vehicleAge', 'driverExperience', 'licenceType'
        ]

        # Filter the dataframe to keep only the required columns
        df_motor = df_motor[required_columns]

        # Step 7: Save the cleaned dataset to memory (BytesIO)
        output = io.BytesIO()
        df_motor.to_csv(output, index=False)
        output.seek(0)  # Move pointer to start of the stream

        # Step 8: Upload the cleaned dataset to the "silver" container
        cleaned_blob_client = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name)
        cleaned_blob_client.upload_blob(output, overwrite=True)

        logging.info(f"Cleaned dataset uploaded to blob: {destination_blob_name}")
        return func.HttpResponse(f"Cleaned dataset uploaded to 'silver/{destination_blob_name}'.", status_code=200)

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Error processing request: {str(e)}", status_code=500)



