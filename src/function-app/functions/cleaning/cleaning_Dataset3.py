# CLEANING DATASET 3
# Noor's Version

# IMPORT NECESSARY LIBRARIES
import pandas as pd
import numpy as np
import os
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from imblearn.over_sampling import SMOTE

# LOAD DATASET

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the relative path to the input dataset
input_file_path = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'raw', 'dataset3.csv')

# Load the dataset
print("Loading dataset...")
df = pd.read_csv(input_file_path)

# CLEAN NUMERIC COLUMNS

# Function to clean and convert columns to numeric
def clean_numeric_column(df, column):
    df[column] = df[column].replace(r'[\$,]', '', regex=True).astype(float)

columns_to_convert = ['INCOME', 'HOME_VAL', 'BLUEBOOK', 'OLDCLAIM', 'CLM_AMT']
for column in columns_to_convert:
    clean_numeric_column(df, column)
print("Numeric columns cleaned and converted.")

# SPLIT INTO NUMERICAL AND CATEGORICAL COLUMNS
numerical_columns = ['KIDSDRIV', 'AGE', 'HOMEKIDS', 'YOJ', 'TRAVTIME', 'TIF', 'MVR_PTS', 'INCOME', 'HOME_VAL', 'BLUEBOOK', 'CLM_AMT']
categorical_columns = ['PARENT1', 'MSTATUS', 'GENDER', 'EDUCATION', 'CAR_USE', 'CAR_TYPE', 'RED_CAR', 'REVOKED', 'URBANICITY', 'OCCUPATION']

# Filter out missing columns
numerical_columns = [col for col in numerical_columns if col in df.columns]
categorical_columns = [col for col in categorical_columns if col in df.columns]

print(f"Numerical columns: {numerical_columns}")
print(f"Categorical columns: {categorical_columns}")

# ENCODE CATEGORICAL VARIABLES
label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le
print("Categorical variables encoded.")

# PREPARE DATASET

# Handle missing values in INCOME by replacing them with the median of non-zero values
print("Handling missing values in 'INCOME'...")
non_zero_income = df[df['INCOME'] > 0]['INCOME']
median_income = np.median(non_zero_income)
df['INCOME'] = df['INCOME'].fillna(median_income)
print(f"Missing values in 'INCOME' after imputation: {df['INCOME'].isnull().sum()}")

# Standardize 'CAR_TYPE' and 'URBANICITY' columns
print("Standardizing 'CAR_TYPE' and 'URBANICITY' columns...")
df['CAR_TYPE'] = df['CAR_TYPE'].replace({'z_SUV': 'SUV'})
df['URBANICITY'] = df['URBANICITY'].replace({'z_Highly Rural/ Rural': 'Highly Rural/ Rural'})
print("Columns standardized.")

# HANDLE MISSING VALUES IN 'CAR_AGE'
print("Handling missing values in 'CAR_AGE'...")
df['CAR_AGE'] = df['CAR_AGE'].fillna(df['CAR_AGE'].median())
print(f"Missing values in 'CAR_AGE' after imputation: {df['CAR_AGE'].isnull().sum()}")

# KNN IMPUTATION FOR NUMERIC COLUMNS
print("Starting KNN imputation for other numeric columns...")
knn_imputer = KNNImputer(n_neighbors=5)
df[numerical_columns] = knn_imputer.fit_transform(df[numerical_columns])
print("KNN imputation completed.")

# IMPUTE ZERO VALUES IN 'CLM_AMT' USING RANDOM FOREST MODEL
print("Imputing zero values in 'CLM_AMT' using a model...")

# Define features (X) and target (y) for training the imputation model
df_train_CLMAMT = df[df['CLM_AMT'] > 0].copy()
df_predict_CLMAMT = df[df['CLM_AMT'] == 0].copy()

X_train_CLMAMT = df_train_CLMAMT.drop(['CLM_AMT'], axis=1)  # Exclude 'CLM_AMT' itself
y_train_CLMAMT = df_train_CLMAMT['CLM_AMT']
X_predict_CLMAMT = df_predict_CLMAMT.drop(['CLM_AMT'], axis=1)

# Preprocessing for CLM_AMT
preprocessor_CLMAMT = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_columns),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_columns)
    ]
)

# Model Pipeline for CLM_AMT
model_pipeline_CLMAMT = Pipeline(steps=[
    ('preprocessor', preprocessor_CLMAMT),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train the model for CLM_AMT
model_pipeline_CLMAMT.fit(X_train_CLMAMT, y_train_CLMAMT)

# Predict and fill zero 'CLM_AMT' values
y_predicted_CLMAMT = model_pipeline_CLMAMT.predict(X_predict_CLMAMT)
df.loc[df['CLM_AMT'] == 0, 'CLM_AMT'] = y_predicted_CLMAMT
print(f"Number of $0 claim amounts after replacement: {df[df['CLM_AMT'] == 0].shape[0]}")

# IMPUTE YOJ USING RANDOM FOREST MODEL
print("Imputing YOJ using RandomForest...")

# Split data into complete and missing YOJ
df_complete_YOJ = df[df['YOJ'].notnull()].copy()
df_missing_YOJ = df[df['YOJ'].isnull()].copy()

X_complete_YOJ = df_complete_YOJ.drop(columns=['YOJ'])
y_complete_YOJ = df_complete_YOJ['YOJ']
X_missing_YOJ = df_missing_YOJ.drop(columns=['YOJ'])

# Preprocessing for YOJ
preprocessor_YOJ = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[('imputer', SimpleImputer(strategy='mean')), ('scaler', StandardScaler())]), numerical_columns),
        ('cat', Pipeline(steps=[('imputer', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore'))]), categorical_columns)
    ]
)

# Define RandomForest model pipeline for YOJ
pipeline_impute_YOJ = Pipeline(steps=[
    ('preprocessor', preprocessor_YOJ),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Perform GridSearchCV for YOJ
param_grid_YOJ = {
    'regressor__n_estimators': [50, 100, 200],
    'regressor__max_depth': [None, 10, 20, 30]
}

grid_search_YOJ = GridSearchCV(pipeline_impute_YOJ, param_grid_YOJ, cv=5, scoring='neg_mean_squared_error')
grid_search_YOJ.fit(X_complete_YOJ, y_complete_YOJ)

# Use the best model to predict YOJ
best_pipeline_YOJ = grid_search_YOJ.best_estimator_
y_predicted_YOJ = best_pipeline_YOJ.predict(X_missing_YOJ)
df.loc[df['YOJ'].isnull(), 'YOJ'] = y_predicted_YOJ
print(f"Remaining missing values in 'YOJ': {df['YOJ'].isnull().sum()}")

# STANDARDIZE 'GENDER' AND 'EDUCATION'
print("Standardizing 'GENDER' and 'EDUCATION' columns...")

df['GENDER'] = df['GENDER'].map({'M': 0, 'z_F': 1})

education_mapping = {
    'z_High School': 'High School',
    'PhD': 'PhD',
    'Bachelors': 'Bachelor',
    '<High School': 'High School',
    'Masters': 'Masters'
}
df['EDUCATION'] = df['EDUCATION'].replace(education_mapping)
print("Columns standardized.")

# SAVE CLEANED DATASET

# Correct relative path for saving the cleaned file
output_file_path = os.path.join(script_dir, '..', '..', 'assets', 'data', 'cleaned', 'cleaned_Dataset3.csv')

# Ensure the output directory exists
output_dir = os.path.dirname(output_file_path)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Created directory: {output_dir}")

# Save cleaned dataset
df.to_csv(output_file_path, index=False)
print(f"Cleaned dataset saved to {output_file_path}.")



