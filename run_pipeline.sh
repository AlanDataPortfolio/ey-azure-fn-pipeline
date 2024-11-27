#!/bin/bash

# Prompt the user for the secret key
read -p "Enter the secret key: " secret_key

# Base URL for the Azure Functions
base_url="https://func-azfnpipeline-prod.azurewebsites.net/api"

# List of function endpoints
functions=(
    "clean_dataset1"
    "clean_dataset2"
    "clean_dataset3"
    "enriching_dataset1"
    "enriching_dataset2"
    "merging_dataset_1_2"
    "synthesising_method_1"
    "synthesising_method_2"
    "enriching_dataset3"
    "merging_20000_rows"
    "normalise"
)

# Loop through each function and make the API call
for function in "${functions[@]}"; do
    url="${base_url}/${function}?code=${secret_key}"
    echo "Calling ${url}..."
    response=$(curl -s -w "\nHTTP_STATUS_CODE:%{http_code}" -X GET "${url}")
    http_status=$(echo "${response}" | grep HTTP_STATUS_CODE | awk -F: '{print $2}')
    body=$(echo "${response}" | sed -e 's/HTTP_STATUS_CODE\:.*//g')

    echo "Response:"
    echo "${body}"
    echo "HTTP Status Code: ${http_status}"
    echo "-----------------------------------"
done