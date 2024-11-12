import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import os

bp = func.Blueprint('merging_dataset_1_2')

@bp.function_name("merging_dataset_1_2")
@bp.route(route="merging_dataset_1_2")
def merging_dataset_1_2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Step 1: Retrieve the Blob Storage connection string from environment variables
    connection_string = os.getenv("AzureWebJobsStorage")
    
    # Define container and blob names
    source_container_name = "silver"
    source_blob_name_dataset1 = "enriched/dataset_1.csv"
    source_blob_name_dataset2 = "enriched/dataset_2.csv"
    destination_container_name = "silver"
    destination_blob_name = "merged/merged_dataset_1_2.csv"

    try:
        # Step 2: Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Step 3: Download the first dataset from the "silver" container
        blob_client_dataset1 = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name_dataset1)
        downloaded_blob_dataset1 = blob_client_dataset1.download_blob()
        blob_data_dataset1 = downloaded_blob_dataset1.readall()

        # Step 4: Download the second dataset from the "silver" container
        blob_client_dataset2 = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name_dataset2)
        downloaded_blob_dataset2 = blob_client_dataset2.download_blob()
        blob_data_dataset2 = downloaded_blob_dataset2.readall()

        # Step 5: Load the datasets into pandas DataFrames (in-memory)
        df1 = pd.read_csv(io.BytesIO(blob_data_dataset1))
        df2 = pd.read_csv(io.BytesIO(blob_data_dataset2))

        # Step 6: Combine the two datasets using concat function
        df_concat = pd.concat([df1, df2])

        # Step 7: Set the index to start from 1 and not reset after 1000
        df_concat.index = range(1, len(df_concat) + 1)

        # Set index name to 'index'
        df_concat.index.name = 'index'

        # Step 8: Save the merged dataset back to the blob storage
        output_blob_client = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name)
        output_blob_client.upload_blob(df_concat.to_csv(index=True), overwrite=True)

        return func.HttpResponse(f"Merged dataset saved to {destination_blob_name}.", status_code=200)

    except Exception as e:
        logging.error(f"Error processing the datasets: {e}")
        return func.HttpResponse(f"Error processing the datasets: {e}", status_code=500)