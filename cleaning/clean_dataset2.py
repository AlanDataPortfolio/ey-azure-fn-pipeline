import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import os

bp = func.Blueprint('clean_dataset2')

@bp.function_name("clean_dataset2")
@bp.route(route="clean_dataset2")

def clean_dataset2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Step 1: Retrieve the Blob Storage connection string from environment variables
    connection_string = os.getenv("AzureWebJobsStorage")
    
    # Define container and blob names
    source_container_name = "bronze"
    source_blob_name = "dataset2.csv"
    destination_container_name = "silver"
    destination_blob_name = "cleaned/dataset_2.csv"

    try:
        # Step 2: Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Step 3: Download the CSV from the "bronze" container
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name)
        downloaded_blob = blob_client.download_blob()
        blob_data = downloaded_blob.readall()

        # Step 4: Load the dataset into a pandas DataFrame (in-memory)
        df = pd.read_csv(io.BytesIO(blob_data), na_values=[], keep_default_na=False)

        # Step 5: Filter for motor claims
        df = df.loc[df["INSURANCE_TYPE"] == "Motor"].copy()

        # Step 6: Fill in null values with the lowest degree for EducationLevel
        df['CUSTOMER_EDUCATION_LEVEL'] = df_motor['CUSTOMER_EDUCATION_LEVEL'].fillna('High School')

        # Step 7: Rename the columns for clarity using camelCase
        df.rename(columns={
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

        # Step 8: Ensure 'none' values are preserved in 'authoritiesInvolved' column
        df['authoritiesInvolved'] = df['authoritiesInvolved'].fillna('none')

        # Step 9: Save the cleaned dataset to memory (BytesIO)
        output = io.BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)  # Move pointer to start of the stream

        # Step 10: Upload the cleaned dataset to the "silver" container
        cleaned_blob_client = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name)
        cleaned_blob_client.upload_blob(output, overwrite=True)

        logging.info(f"Cleaned dataset saved to {destination_blob_name}.")
        return func.HttpResponse(f"Cleaned dataset uploaded to 'silver/{destination_blob_name}'.", status_code=200)
    
    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)