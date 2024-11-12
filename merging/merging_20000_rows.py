import os
import pandas as pd
import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import io

bp = func.Blueprint('merging_20000_rows')

@bp.function_name("merging_20000_rows")
@bp.route(route="merging_20000_rows")
def merging_20000_rows(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Step 1: Retrieve the Blob Storage connection string from environment variables
    connection_string = os.getenv("AzureWebJobsStorage")
    
    # Define container and blob names
    source_container_name = "silver"
    source_blob_name_1 = "enriched/dataset_1.csv"
    source_blob_name_2 = "enriched/dataset_2.csv"
    source_blob_name_3 = "enriched/dataset_3.csv"
    source_blob_name_4 = "synthesised/method_1.csv"
    source_blob_name_5 = "synthesised/method_2.csv"
    destination_container_name = "gold"
    destination_blob_name = "unnormalised/20000_rows.csv"

    try:
        # Step 2: Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Step 3: Download the CSVs from the "enriched" and "synthesised" containers
        def download_blob_to_df(container_name, blob_name):
            blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            downloaded_blob = blob_client.download_blob()
            blob_data = downloaded_blob.readall()
            return pd.read_csv(io.BytesIO(blob_data), na_values=[], keep_default_na=False)

        df1 = download_blob_to_df(source_container_name, source_blob_name_1)
        df2 = download_blob_to_df(source_container_name, source_blob_name_2)
        df3 = download_blob_to_df(source_container_name, source_blob_name_3)
        df4 = download_blob_to_df(source_container_name, source_blob_name_4)
        df5 = download_blob_to_df(source_container_name, source_blob_name_5)

        # Drop the index columns in the synthesized datasets 
        df4 = df4.drop('index', axis=1, errors='ignore')
        df5 = df5.drop('index', axis=1, errors='ignore')

        # Combine the datasets using the concat function
        df_concat = pd.concat([df1, df2, df3, df4, df5])

        # Fill 'none' only for columns that are expected to have 'none' in existing rows,
        # but keep other columns where they should remain NaN if not present in the datasets
        columns_to_fill_none = ['driverGender', 'accidentType', 'incidentSeverity', 'authoritiesInvolved']

        for col in columns_to_fill_none:
            if col in df_concat.columns:
                df_concat[col] = df_concat[col].where(df_concat[col].notna(), None)

        # Set the index to start from 1 and not reset 
        df_concat.index = range(1, len(df_concat) + 1)

        # Set index name to 'index'
        df_concat.index.name = 'index'

        # Save the merged dataset back to the blob storage
        output_blob_client = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name)
        output_blob_client.upload_blob(df_concat.to_csv(index=True), overwrite=True)

        return func.HttpResponse(f"Merged dataset saved to {destination_blob_name}.", status_code=200)

    except Exception as e:
        logging.error(f"Error processing the dataset: {e}")
        return func.HttpResponse(f"Error processing the dataset: {e}", status_code=500)