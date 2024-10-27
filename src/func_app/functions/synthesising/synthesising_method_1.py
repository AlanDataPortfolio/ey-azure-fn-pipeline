import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
import numpy as np
import io
import os

bp = func.Blueprint('synthesising_method_1')

@bp.function_name("synthesising_method_1")
@bp.route(route="synthesising_method_1")
def synthesising_method_1(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Step 1: Retrieve the Blob Storage connection string from environment variables
    connection_string = os.getenv("AzureWebJobsStorage")
    
    # Define container and blob names
    source_container_name = "silver"
    source_blob_name = "merged/merged_dataset_1_2.csv"
    destination_container_name = "silver"
    destination_blob_name = "synthesised/method1.csv"

    try:
        # Step 2: Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Step 3: Download the CSV from the "merged" container
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name)
        downloaded_blob = blob_client.download_blob()
        blob_data = downloaded_blob.readall()

        # Step 4: Load the dataset into a pandas DataFrame (in-memory)
        df = pd.read_csv(io.BytesIO(blob_data), na_values=[], keep_default_na=False)

        # Ensure that 'authoritiesInvolved' contains no blanks or NaN values
        df['authoritiesInvolved'] = df['authoritiesInvolved'].replace('', 'none').fillna('none')


        # Set the number of synthetic rows you want to generate
        num_samples = 4000

        # Generate synthetic data by sampling from the original data's distribution (excluding the 'fraud' column)
        columns_to_sample = df.columns.difference(['fraud'])
        synthetic_data = df[columns_to_sample].sample(n=num_samples, replace=True, random_state=0).reset_index(drop=True)

        # Add the 'fraud' column back without modification
        synthetic_data['fraud'] = df['fraud'].sample(n=num_samples, replace=True, random_state=0).reset_index(drop=True)

        # **Ensure 'authoritiesInvolved' in synthetic_data is cleaned in case of any reintroduced missing values**
        synthetic_data['authoritiesInvolved'] = synthetic_data['authoritiesInvolved'].replace('', 'none').fillna('none')


        # Optionally, add some noise to numeric columns (excluding 'fraud') and ensure no negatives
        for column in synthetic_data.select_dtypes(include=[np.number]).columns.difference(['fraud']):
            noise = np.random.normal(0, 0.01, size=synthetic_data[column].shape)
            synthetic_data[column] += noise
            synthetic_data[column] = synthetic_data[column].round()  # Round to nearest whole number
            synthetic_data[column] = synthetic_data[column].clip(lower=0)  # Ensure no negative values

        # Save the synthetic data back to the blob storage
        destination_blob_client = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name)
        destination_blob_client.upload_blob(synthetic_data.to_csv(index=False))

        return func.HttpResponse("Synthetic data generation completed and saved to '{destination_blob_name}'")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return func.HttpResponse(f"An error occurred: {e}", status_code=500)
    


