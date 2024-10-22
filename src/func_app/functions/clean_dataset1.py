import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import os

bp = func.Blueprint('clean_dataset1')

@bp.function_name("clean_dataset1")
@bp.route(route="clean_dataset1")
def clean_dataset1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Step 1: Retrieve the Blob Storage connection string from environment variables
    connection_string = os.getenv("AzureWebJobsStorage")
    
    # Define container and blob names
    source_container_name = "bronze"
    source_blob_name = "dataset1.csv"
    destination_container_name = "silver"
    destination_blob_name = "cleaned/dataset_1.csv"

    try:
        # Step 2: Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Step 3: Download the CSV from the "bronze" container
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name)
        downloaded_blob = blob_client.download_blob()
        blob_data = downloaded_blob.readall()

        # Step 4: Load the dataset into a pandas DataFrame (in-memory)
        df = pd.read_csv(io.BytesIO(blob_data), na_values=[], keep_default_na=False)

        # Step 5: Rename columns for clarity
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

        # Step 6: Handle missing values
        df['policeReportBool'] = df['policeReportBool'].replace({'?': 'NO'})
        df['authoritiesInvolved'] = df['authoritiesInvolved'].fillna('None')

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
