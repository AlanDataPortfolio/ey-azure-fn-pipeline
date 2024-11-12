import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
import numpy as np
import os
import io
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer
from sdv.evaluation.single_table import evaluate_quality

bp = func.Blueprint('synthesising_method_2')

@bp.function_name("synthesising_method_2")
@bp.route(route="synthesising_method_2")
def synthesising_method_2(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Step 1: Retrieve the Blob Storage connection string from environment variables
    connection_string = os.getenv("AzureWebJobsStorage")
    
    # Define container and blob names
    source_container_name = "silver"
    source_blob_name = "merged/merged_dataset_1_2.csv"
    destination_container_name = "silver"
    destination_blob_name = "synthesised/method_2.csv"

    try:
        # Step 2: Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Step 3: Download the CSV from the "merged" container
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name)
        downloaded_blob = blob_client.download_blob()
        blob_data = downloaded_blob.readall()

        # Step 4: Load the dataset into a pandas DataFrame (in-memory)
        df = pd.read_csv(io.BytesIO(blob_data), na_values=[], keep_default_na=False)

        # Define the metadata for the dataset
        metadata = SingleTableMetadata()

        # Correct the argument passed to detect_from_csv by providing the input file path
        metadata.detect_from_csv(filepath=source_blob_name)

        # Define the synthesizer
        synthesizer = CTGANSynthesizer(
            metadata,
            enforce_rounding=False,
            epochs=1800,
            verbose=True
        )

        # Fit the synthesizer with the dataset
        synthesizer.fit(df)

        # Generate synthetic data
        synthetic_data = synthesizer.sample(num_rows=4000)

        # Convert synthetic data to a DataFrame
        synthetic_df = pd.DataFrame(synthetic_data)

        # Reset the index to ensure it starts from 1
        synthetic_df.reset_index(drop=True, inplace=True)

        # Set the index to range from 1 to 4000
        synthetic_df['index'] = synthetic_df.index = range(1, len(synthetic_df) + 1)

        # Evaluate the quality of the synthetic data
        quality_report = evaluate_quality(
            real_data=df,
            synthetic_data=synthetic_data,
            metadata=metadata
        )

        # Save the synthetic dataset back to the blob storage
        output_blob_client = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name)
        output_blob_client.upload_blob(synthetic_df.to_csv(index=False), overwrite=True)

        return func.HttpResponse(f"Synthetic dataset saved to {destination_blob_name}.", status_code=200)

    except Exception as e:
        logging.error(f"Error processing the dataset: {e}")
        return func.HttpResponse(f"Error processing the dataset: {e}", status_code=500)