import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import os
import numpy as np

bp = func.Blueprint('enriching_dataset1')

@bp.function_name("enriching_dataset1")
@bp.route(route="enriching_dataset1")
def enriching_dataset1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Step 1: Retrieve the Blob Storage connection string from environment variables
    connection_string = os.getenv("AzureWebJobsStorage")
    
    # Define container and blob names
    source_container_name = "silver"
    source_blob_name = "cleaned/dataset1.csv"
    destination_container_name = "silver"
    destination_blob_name = "enriched/dataset_1.csv"

    try:
        # Step 2: Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Step 3: Download the CSV from the "bronze" container
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name)
        downloaded_blob = blob_client.download_blob()
        blob_data = downloaded_blob.readall()

        # Step 4: Load the dataset into a pandas DataFrame (in-memory)
        df = pd.read_csv(io.BytesIO(blob_data), na_values=[], keep_default_na=False)

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

        # Step 7: Save the cleaned dataset to memory (BytesIO)
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)  # Move pointer to start of the stream

        # Step 8: Upload the cleaned dataset to the "silver" container
        cleaned_blob_client = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name)
        cleaned_blob_client.upload_blob(output, overwrite=True)

        logging.info(f"Cleaned dataset uploaded to blob: {destination_blob_name}")
        return func.HttpResponse(f"Cleaned dataset uploaded to 'silver/{destination_blob_name}'.", status_code=200)

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Error processing request: {str(e)}", status_code=500)