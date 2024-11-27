import logging
import azure.functions as func
from azure.storage.blob import BlobServiceClient
import pandas as pd
import io
import os
import numpy as np
from scipy import stats
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sdv.metadata import SingleTableMetadata
from sdv.single_table import CTGANSynthesizer
from sdv.evaluation.single_table import evaluate_quality


app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="clean_dataset1")
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

@app.route(route="clean_dataset2", auth_level=func.AuthLevel.FUNCTION)
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
        df['CUSTOMER_EDUCATION_LEVEL'] = df['CUSTOMER_EDUCATION_LEVEL'].fillna('High School')

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
    
@app.route(route="clean_dataset3", auth_level=func.AuthLevel.FUNCTION)
def clean_dataset3(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Step 1: Retrieve the Blob Storage connection string from environment variables
    connection_string = os.getenv("AzureWebJobsStorage")
    
    # Define container and blob names
    source_container_name = "bronze"
    source_blob_name = "dataset3.csv"
    destination_container_name = "silver"
    destination_blob_name = "cleaned/dataset_3.csv"

    try:
        # Step 2: Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Step 3: Download the CSV from the "bronze" container
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name)
        downloaded_blob = blob_client.download_blob()
        blob_data = downloaded_blob.readall()

        # Step 4: Load the dataset into a pandas DataFrame (in-memory)
        df = pd.read_csv(io.BytesIO(blob_data), na_values=[], keep_default_na=False)

        # Clean The Dataset

        # Function to clean and convert columns to numeric
        def clean_numeric_column(df, column):
            """Cleans and converts columns to numeric values."""
            df[column] = df[column].replace(r'[\$,]', '', regex=True).astype(float)

        # Columns to convert
        columns_to_convert = ['INCOME', 'HOME_VAL', 'BLUEBOOK', 'OLDCLAIM', 'CLM_AMT']

        for column in columns_to_convert:
            clean_numeric_column(df, column)

        # After cleaning, confirm that data types are correct
        print("Numeric columns cleaned and converted.")
        print(df.dtypes)

        # Split into numerical and categorical columns
        numerical_columns = ['KIDSDRIV', 'AGE', 'HOMEKIDS', 'YOJ', 'TRAVTIME', 'TIF', 'MVR_PTS',
                            'INCOME', 'HOME_VAL', 'BLUEBOOK', 'CLM_AMT', 'CAR_AGE']
        categorical_columns = ['PARENT1', 'MSTATUS', 'GENDER', 'EDUCATION', 'OCCUPATION',
                            'CAR_USE', 'CAR_TYPE', 'RED_CAR', 'REVOKED', 'URBANICITY']
        
        # Filter out missing columns
        numerical_columns = [col for col in numerical_columns if col in df.columns]
        categorical_columns = [col for col in categorical_columns if col in df.columns]

        # Ensure the lists are correctly defined
        print(f"Numerical columns: {numerical_columns}")
        print(f"Categorical columns: {categorical_columns}")

        # Prepare Dataset

        # Select the relevant numerical and categorical features for imputation
        features_for_imputation = numerical_columns + categorical_columns

        # Copy the relevant columns into a new DataFrame
        df_impute = df[features_for_imputation].copy()

        # Encode categorical variables
        label_encoders = {}
        for col in categorical_columns:
            le = LabelEncoder()
            df_impute[col] = le.fit_transform(df_impute[col].astype(str))
            label_encoders[col] = le

        print("Categorical variables encoded.")

        # Initialize the KNN imputer
        print("Starting KNN imputation...")
        knn_imputer = KNNImputer(n_neighbors=5)

        # Apply KNN imputation to the data
        df_imputed = pd.DataFrame(knn_imputer.fit_transform(df_impute), columns=features_for_imputation)
        print("KNN imputation completed.")

        # Replace the original columns in the original DataFrame with the imputed values
        for col in numerical_columns:
            df[col] = df_imputed[col]

        print("Numeric columns imputed.")

        # Impute YOJ Column

        # Check if there are any missing values for 'YOJ' before RandomForest imputation
        print(f"Missing values in 'YOJ' before RandomForest imputation: {df['YOJ'].isnull().sum()}")

        if df['YOJ'].isnull().sum() > 0:
            print("Imputing 'YOJ' column using RandomForest...")
            df_complete_YOJ = df[df['YOJ'].notnull()].copy()
            df_missing_YOJ = df[df['YOJ'].isnull()].copy()

            # Separate the target variable from features
            y_complete_YOJ = df_complete_YOJ['YOJ']
            X_complete_YOJ = df_complete_YOJ.drop(columns=['YOJ'])
            X_missing_YOJ = df_missing_YOJ.drop(columns=['YOJ'])

            # Filter out columns not in X_complete
            numerical_columns_YOJ = [col for col in numerical_columns if col in X_complete_YOJ.columns]
            categorical_columns_YOJ = [col for col in categorical_columns if col in X_complete_YOJ.columns]

            # Prepare the column transformer to handle categorical and numerical data
            preprocessor_YOJ = ColumnTransformer(
                transformers=[
                    ('num', Pipeline(steps=[
                        ('imputer', SimpleImputer(strategy='mean')),
                        ('scaler', StandardScaler())
                    ]), numerical_columns_YOJ),
                    ('cat', Pipeline(steps=[
                        ('imputer', SimpleImputer(strategy='most_frequent')),
                        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
                    ]), categorical_columns_YOJ)
                ]
            )

            # Define the pipeline with RandomForestRegressor
            pipeline_impute_YOJ = Pipeline(steps=[
                ('preprocessor', preprocessor_YOJ),
                ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
            ])

            # Define parameter grid for hyperparameter tuning
            param_grid_YOJ = {
                'regressor__n_estimators': [50, 100, 200],
                'regressor__max_depth': [None, 10, 20, 30]
            }

            # Perform GridSearchCV
            grid_search_YOJ = GridSearchCV(pipeline_impute_YOJ, param_grid_YOJ, cv=5, scoring='neg_mean_squared_error')
            grid_search_YOJ.fit(X_complete_YOJ, y_complete_YOJ)

            # Use the best model to predict missing values
            best_pipeline_YOJ = grid_search_YOJ.best_estimator_
            y_predicted_YOJ = best_pipeline_YOJ.predict(X_missing_YOJ)

            # Fill missing values
            df.loc[df['YOJ'].isnull(), 'YOJ'] = y_predicted_YOJ

            # Check if missing values are filled
            print(f"Remaining missing values in 'YOJ' after RandomForest imputation: {df['YOJ'].isnull().sum()}")
        else:
            print("No missing values for 'YOJ' found. Skipping RandomForest imputation.")

        # Impute INCOME Column
        print("Imputing 'INCOME' column using median of non-zero values...")
        non_zero_income = df[df['INCOME'] > 0]['INCOME']
        median_income = np.median(non_zero_income)
        df['INCOME'] = df['INCOME'].fillna(median_income)
        print(f"Missing values in 'INCOME' after imputation: {df['INCOME'].isnull().sum()}")

        # Standardize Occupation Values
        print("Standardizing 'OCCUPATION' values...")
        df['OCCUPATION'] = df['OCCUPATION'].str.replace('z_', '')

        # Impute OCCUPATION based on INCOME brackets
        print("Imputing missing 'OCCUPATION' based on 'INCOME' correlation...")

        # Define income ranges for each occupation based on the mean values
        occupation_ranges = {
            'Blue Collar': (0, 60000),
            'Clerical': (30000, 40000),
            'Doctor': (120000, 140000),
            'Home Maker': (0, 25000),
            'Lawyer': (85000, 95000),
            'Manager': (80000, 95000),
            'Professional': (70000, 80000),
            'Student': (0, 15000)
        }

        # Function to assign occupation based on income
        def assign_occupation(income):
            for occupation, (low, high) in occupation_ranges.items():
                if low <= income <= high:
                    return occupation
            return None  # If income doesn't fall in any range

        # Apply this function to fill missing occupations based on income
        df['OCCUPATION'] = df.apply(
            lambda row: assign_occupation(row['INCOME']) if pd.isnull(row['OCCUPATION']) else row['OCCUPATION'],
            axis=1
        )

        # For cases with missing income or no matching range, randomly assign occupations
        missing_occupation = df['OCCUPATION'].isnull()
        if missing_occupation.sum() > 0:
            print(f"Randomly assigning 'OCCUPATION' to {missing_occupation.sum()} missing entries...")
            random_occupations = df['OCCUPATION'].dropna().sample(missing_occupation.sum(), replace=True)
            df.loc[missing_occupation, 'OCCUPATION'] = random_occupations.values

        print(f"Missing values in 'OCCUPATION' after imputation: {df['OCCUPATION'].isnull().sum()}")

        # Impute HOME_VAL Column
        print("Imputing 'HOME_VAL' column using KNN imputation...")
        df['HOME_VAL'] = df_imputed['HOME_VAL']
        print(f"Missing values in 'HOME_VAL' after imputation: {df['HOME_VAL'].isnull().sum()}")

        # Impute CAR_AGE column
        print("Imputing 'CAR_AGE' column using median...")
        df['CAR_AGE'] = df['CAR_AGE'].fillna(df['CAR_AGE'].median())
        print(f"Missing values in 'CAR_AGE' after imputation: {df['CAR_AGE'].isnull().sum()}")

        # Impute CLM_AMT column
        print("Imputing zero 'CLM_AMT' values using RandomForestRegressor...")

        # Split the data
        df_train_CLMAMT = df[df['CLM_AMT'] > 0].copy()
        df_predict_CLMAMT = df[df['CLM_AMT'] == 0].copy()

        # Define features (X) and target (y) for training
        X_train_CLMAMT = df_train_CLMAMT[numerical_columns + categorical_columns]
        y_train_CLMAMT = df_train_CLMAMT['CLM_AMT']
        X_predict_CLMAMT = df_predict_CLMAMT[numerical_columns + categorical_columns]

        # Preprocessing
        preprocessor_CLMAMT = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numerical_columns),
                ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_columns)
            ]
        )

        # Model Pipeline
        model_pipeline_CLMAMT = Pipeline(steps=[
            ('preprocessor', preprocessor_CLMAMT),
            ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
        ])

        # Train the model
        model_pipeline_CLMAMT.fit(X_train_CLMAMT, y_train_CLMAMT)

        # Predict CLM_AMT for rows where it was originally 0
        y_predicted_CLMAMT = model_pipeline_CLMAMT.predict(X_predict_CLMAMT)

        # Fill the $0 CLM_AMT values with the predicted values
        df.loc[df['CLM_AMT'] == 0, 'CLM_AMT'] = y_predicted_CLMAMT

        # Check that there are no more $0 values
        zero_claims_after = df[df['CLM_AMT'] == 0].shape[0]
        print(f"Number of $0 claim amounts after replacement: {zero_claims_after}")

        # Standardize the Dataset

        # Convert 'M' to 0 and 'z_F' to 1 in GENDER
        print("Standardizing 'GENDER' column...")
        df['GENDER'] = df['GENDER'].map({'M': 0, 'z_F': 1})

        # Standardize 'EDUCATION' column
        print("Standardizing 'EDUCATION' column...")
        education_mapping = {
            'z_High School': 'High School',
            'PhD': 'PhD',
            'Bachelors': 'Bachelor',
            '<High School': 'High School',
            'Masters': 'Masters'
        }
        df['EDUCATION'] = df['EDUCATION'].replace(education_mapping)

        # Standardize 'OCCUPATION' column
        print("Final standardization of 'OCCUPATION' column...")
        df['OCCUPATION'] = df['OCCUPATION'].str.strip().str.title()
        df['OCCUPATION'] = df['OCCUPATION'].replace({
            'Blue Collar': 'Blue Collar',
            'Manager': 'Manager',
            'Professional': 'Professional',
            'Clerical': 'Clerical',
            'Doctor': 'Doctor',
            'Home Maker': 'Home Maker',
            'Lawyer': 'Lawyer',
            'Student': 'Student'
        })

        # Standardize 'CAR_TYPE' column
        print("Standardizing 'CAR_TYPE' column...")
        df['CAR_TYPE'] = df['CAR_TYPE'].replace({'z_SUV': 'SUV'})

        # Standardize 'URBANICITY' column
        print("Standardizing 'URBANICITY' column...")
        df['URBANICITY'] = df['URBANICITY'].replace({'z_Highly Rural/ Rural': 'Highly Rural/ Rural'})

        print("Dataset standardized.")
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

@app.route(route="enriching_dataset1", auth_level=func.AuthLevel.FUNCTION)
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
    
@app.route(route="enriching_dataset2", auth_level=func.AuthLevel.FUNCTION)
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

@app.route(route="enriching_dataset3", auth_level=func.AuthLevel.FUNCTION)
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

@app.route(route="merging_dataset_1_2", auth_level=func.AuthLevel.FUNCTION)
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
    
@app.route(route="merging_20000_rows", auth_level=func.AuthLevel.FUNCTION)
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


@app.route(route="synthesising_method_1", auth_level=func.AuthLevel.FUNCTION)
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
    

@app.route(route="synthesising_method_2", auth_level=func.AuthLevel.FUNCTION)
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
    
@app.route(route="normalise", auth_level=func.AuthLevel.FUNCTION)
def normalise(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Step 1: Retrieve the Blob Storage connection string from environment variables
    connection_string = os.getenv("AzureWebJobsStorage")
    
    # Define container and blob names
    source_container_name = "gold"
    source_blob_name = "unnormalised/20000_rows.csv"
    destination_container_name = "gold"
    destination_blob_name_1 = "normalised/claims.csv"
    destination_blob_name_2 = "normalised/drivers.csv"
    destination_blob_name_3 = "normalised/incidents.csv"
    destination_blob_name_4 = "normalised/insurance.csv"
    destination_blob_name_5 = "normalised/vehicles.csv"

    try:
        # Step 2: Initialize BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Step 3: Download the CSV from the "merged" container
        blob_client = blob_service_client.get_blob_client(container=source_container_name, blob=source_blob_name)
        downloaded_blob = blob_client.download_blob()
        blob_data = downloaded_blob.readall()

        # Step 4: Load the dataset into a pandas DataFrame (in-memory)
        df = pd.read_csv(io.BytesIO(blob_data), na_values=[], keep_default_na=False)

        # Remove rows that contain null values in critical columns only
        # Specify critical columns based on the table relationships
        critical_columns = ['ClaimsID', 'DriverID', 'InsuranceID', 'IncidentID', 'VehicleID']
        df.dropna(subset=critical_columns, inplace=True)

        # Split the data into separate DataFrames based on table schema
        claims_df = df[['ClaimsID', 'DriverID', 'InsuranceID', 'IncidentID', 'authoritiesInvolved', 'policeReportBool', 'totalClaimAmount', 'fraud', 'VehicleID']].dropna()
        drivers_df = df[['DriverID', 'timeAsCustomer', 'driverAge', 'driverGender', 'educationLevel', 'driverExperience', 'licenceType']].dropna()
        incidents_df = df[['IncidentID', 'accidentType', 'incidentSeverity', 'incidentTime', 'numVehiclesInvolved', 'numBodilyInjuries']].dropna()
        insurance_df = df[['InsuranceID', 'insuranceAccess', 'insurancePremium']].dropna()
        vehicles_df = df[['VehicleID', 'vehicleAge']].dropna()

        # Save the synthetic dataset back to the blob storage
        output_blob_client_1 = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name_1)
        output_blob_client_1.upload_blob(claims_df.to_csv(index=False), overwrite=True)
        
        output_blob_client_2 = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name_2)
        output_blob_client_2.upload_blob(drivers_df.to_csv(index=False), overwrite=True)
        
        output_blob_client_3 = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name_3)
        output_blob_client_3.upload_blob(incidents_df.to_csv(index=False), overwrite=True)
        
        output_blob_client_4 = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name_4)
        output_blob_client_4.upload_blob(insurance_df.to_csv(index=False), overwrite=True)
        
        output_blob_client_5 = blob_service_client.get_blob_client(container=destination_container_name, blob=destination_blob_name_5)
        output_blob_client_5.upload_blob(vehicles_df.to_csv(index=False), overwrite=True)

    except Exception as e:
        logging.error(f"Error processing the dataset: {e}")
        return func.HttpResponse(f"Error processing the dataset: {e}", status_code=500)