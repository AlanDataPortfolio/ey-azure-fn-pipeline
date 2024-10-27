import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import os
import numpy as np

bp = func.Blueprint('enriching_dataset3')

@bp.function_name("enriching_dataset3")
@bp.route(route="enriching_dataset3")
def enriching_dataset3(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Step 1: Retrieve the Blob Storage connection string from environment variables
    connection_string = os.getenv("AzureWebJobsStorage")
    
    # Define container and blob names
    source_container_name = "silver"
    source_blob_name = "cleaned/dataset3.csv"
    destination_container_name = "silver"
    destination_blob_name = "enriched/dataset_3.csv"

    try:
        # Step 2: Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Step 3: Download the CSV from the "bronze" container
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name)
        downloaded_blob = blob_client.download_blob()
        blob_data = downloaded_blob.readall()

        # Step 4: Load the dataset into a pandas DataFrame (in-memory)
        df = pd.read_csv(io.BytesIO(blob_data), na_values=[], keep_default_na=False)

        # DROP SPECIFIED COLUMNS
        columns_to_drop = ['ID', 'KIDSDRIV', 'BIRTH', 'HOMEKIDS', 'YOJ', 'INCOME', 'PARENT1', 'HOME_VAL', 
                        'MSTATUS', 'GENDER', 'OCCUPATION', 'TRAVTIME', 'CAR_USE', 'BLUEBOOK', 'TIF', 
                        'CAR_TYPE', 'RED_CAR', 'OLDCLAIM', 'CLM_FREQ', 'MVR_PTS', 'CLAIM_FLAG', 'URBANICITY']

        # Drop the columns
        df = df.drop(columns=columns_to_drop)
        print(f"Columns dropped. Remaining columns: {df.columns.tolist()}")

        # RENAME COLUMNS
        print("Renaming columns...")
        df.rename(columns={
            'AGE': 'driverAge',
            'EDUCATION': 'educationLevel',
            'CLM_AMT': 'totalClaimAmount',
            'CAR_AGE': 'vehicleAge',
            'REVOKED': 'fraud'
        }, inplace=True)

        # Convert fraud column to 0 (No) and 1 (Yes)
        df['fraud'] = df['fraud'].map({'No': 0, 'Yes': 1})

        # Create New Columns

        # Assuming 'driverAge' represents the driver's age
        print("Generating 'driverExperience' column...")
        np.random.seed(0)  # For reproducibility
        df['driverExperience'] = df['driverAge'] - 16 - np.random.randint(0, 7, size=len(df))

        # Create 'licenceType' column based on 'driverExperience'
        print("Generating 'licenceType' column...")
        conditions = [
            (df['driverExperience'] < 1),
            (df['driverExperience'] >= 1) & (df['driverExperience'] < 3),
            (df['driverExperience'] >= 3) & (df['driverExperience'] < 5),
            (df['driverExperience'] >= 5)
        ]
        choices = ['Ls', 'P1', 'P2', 'Full']
        df['licenceType'] = np.select(conditions, choices, default='')

        # Convert Remaining Numeric Columns to Whole Numbers

        print("Converting numeric columns to whole numbers...")
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
        df[numeric_cols] = df[numeric_cols].round(0).astype(int)

        # REARRANGE COLUMNS
        column_order = [
            'timeAsCustomer', 'driverAge', 'insuranceAccess', 'insurancePremium', 'driverGender', 'educationLevel',
            'accidentType', 'incidentSeverity', 'authoritiesInvolved', 'incidentTime', 'numVehiclesInvolved',
            'numBodilyInjuries', 'policeReportBool', 'totalClaimAmount', 'fraud', 'vehicleAge',
            'driverExperience', 'licenceType'
        ]

        # Only keep columns that exist in the current dataframe
        column_order = [col for col in column_order if col in df.columns]

        df = df[column_order]

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



