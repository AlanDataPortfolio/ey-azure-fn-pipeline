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

bp = func.Blueprint('clean_dataset3')

@bp.function_name("clean_dataset3")
@bp.route(route="clean_dataset3")

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
