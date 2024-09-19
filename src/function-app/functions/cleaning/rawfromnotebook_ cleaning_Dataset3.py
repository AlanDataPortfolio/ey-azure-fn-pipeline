# Cleaning Dataset 3
# Noor's Version

# Import necessary libraries
import pandas as pd
import numpy as np
import os
from sklearn.svm import SVR
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import KNNImputer
from sklearn.neighbors import KNeighborsRegressor
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.feature_selection import SelectFromModel
from imblearn.over_sampling import SMOTE

# Clean Dataset

# Load Dataset

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the relative path to the input dataset
input_file_path = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'raw', 'dataset3.csv')

# Load the dataset
df = pd.read_csv(input_file_path)

# Clean The Dataset
# Function to clean and convert columns to numeric
def clean_numeric_column(df, column):
    df[column] = df[column].replace(r'[\$,]', '', regex=True).astype(float)

# Columns to convert
columns_to_convert = ['INCOME', 'HOME_VAL', 'BLUEBOOK', 'OLDCLAIM', 'CLM_AMT']

for column in columns_to_convert:
    clean_numeric_column(df, column)

# After cleaning, confirm that data types are correct
print(df.dtypes)

# Split into numerical and categorical columns
numerical_columns = ['KIDSDRIV', 'AGE', 'HOMEKIDS', 'YOJ', 'TRAVTIME', 'TIF', 'MVR_PTS', 'INCOME', 'HOME_VAL', 'BLUEBOOK', 'CLM_AMT']
categorical_columns = ['PARENT1', 'MSTATUS', 'GENDER', 'EDUCATION', 'CAR_USE', 'CAR_TYPE', 'RED_CAR', 'REVOKED', 'URBANICITY', 'OCCUPATION']

# Filter out missing columns
numerical_columns = [col for col in numerical_columns if col in df.columns]
categorical_columns = [col for col in categorical_columns if col in df.columns]

# Ensure the lists are correctly defined
print("Numerical columns:", numerical_columns)
print("Categorical columns:", categorical_columns)

# Prepare Dataset

#Select the relevant numerical and categorical features for imputation
features_for_imputation = ['YOJ', 'INCOME', 'HOME_VAL', 'BLUEBOOK', 'AGE', 'PARENT1', 
                           'MSTATUS', 'GENDER', 'EDUCATION', 'CAR_USE', 'CAR_TYPE', 
                           'RED_CAR', 'REVOKED', 'URBANICITY', 'OCCUPATION', 'CAR_AGE']

# Copy the relevant columns into a new DataFrame
df_impute = df[features_for_imputation].copy()

# Encode categorical variables
label_encoders = {}
for col in ['PARENT1', 'MSTATUS', 'GENDER', 'EDUCATION', 'CAR_USE', 
            'CAR_TYPE', 'RED_CAR', 'REVOKED', 'URBANICITY', 'OCCUPATION']:
    le = LabelEncoder()
    df_impute[col] = le.fit_transform(df_impute[col].astype(str))
    label_encoders[col] = le

# Initialize the KNN imputer
knn_imputer = KNNImputer(n_neighbors=5)

# Apply KNN imputation to the data
df_imputed = knn_imputer.fit_transform(df_impute)

# Replace the original AGE column in the original DataFrame with the imputed values
df['AGE'] = df_imputed[:, 0]

# Check if missing values are imputed
print(df['AGE'].isnull().sum())

# Impute YOJ Column

# Split into complete and missing data
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
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
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
print(f"Remaining missing values in 'YOJ': {df['YOJ'].isnull().sum()}")

# Impute Income Column

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
print(f"Remaining missing values in 'YOJ': {df['YOJ'].isnull().sum()}")

# Check if missing values are imputed
print(df['INCOME'].isnull().sum())

# Impute Home_Val Column

# Replace the original HOME_VAL column in the original DataFrame with the imputed values
df['HOME_VAL'] = df_imputed[:, 0]

# Check if missing values are imputed
print(df['HOME_VAL'].isnull().sum())

# Impute Occupation Column

# Split the data into rows with known and unknown 'OCCUPATION'
train_data_OCCUPATION = df_impute[df['OCCUPATION'].notnull()]
test_data_OCCUPATION = df_impute[df['OCCUPATION'].isnull()]

# Ensure there are rows in X_test for prediction
if test_data_OCCUPATION.empty:
    print("No missing 'OCCUPATION' values to predict.")
else:
    # Select features for training (drop 'OCCUPATION' only from features)
    X_train_OCCUPATION = train_data_OCCUPATION.drop(['OCCUPATION'], axis=1)
    y_train_OCCUPATION = train_data_OCCUPATION['OCCUPATION']

    X_test_OCCUPATION = test_data_OCCUPATION.drop(['OCCUPATION'], axis=1)

    # Impute missing values (use 'most_frequent' for categorical, 'mean' for numerical)
    imputer_OCCUPATION = SimpleImputer(strategy='most_frequent')
    X_train_OCCUPATION = pd.DataFrame(imputer_OCCUPATION.fit_transform(X_train_OCCUPATION), columns=X_train_OCCUPATION.columns)
    X_test_OCCUPATION = pd.DataFrame(imputer_OCCUPATION.transform(X_test_OCCUPATION), columns=X_test_OCCUPATION.columns)

    # Handle Class Imbalance with SMOTE
    smote_OCCUPATION = SMOTE(random_state=42)
    X_train_resampled_OCCUPATION, y_train_resampled_OCCUPATION = smote_OCCUPATION.fit_resample(X_train_OCCUPATION, y_train_OCCUPATION)

# Hyperparameter tuning using RandomizedSearchCV
param_grid_OCCUPATION = {
    'n_estimators': [100, 200, 500],
    'max_features': ['sqrt', 'log2', None],
    'max_depth': [10, 20, 30, None],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}

# Create a RandomForestClassifier with randomized search
clf_OCCUPATION = RandomForestClassifier(random_state=42)
random_search_OCCUPATION = RandomizedSearchCV(clf_OCCUPATION, param_distributions=param_grid_OCCUPATION, n_iter=10, cv=3, random_state=42, n_jobs=-1)
random_search_OCCUPATION.fit(X_train_resampled_OCCUPATION, y_train_resampled_OCCUPATION)

 # Feature Selection based on importance
selector_OCCUPATION = SelectFromModel(random_search_OCCUPATION.best_estimator_, threshold='median')
X_train_selected_OCCUPATION = selector_OCCUPATION.fit_transform(X_train_resampled_OCCUPATION, y_train_resampled_OCCUPATION)
X_test_selected_OCCUPATION = selector_OCCUPATION.transform(X_test_OCCUPATION)

# Train the best model on the selected features
best_clf_OCCUPATION = random_search_OCCUPATION.best_estimator_
best_clf_OCCUPATION.fit(X_train_selected_OCCUPATION, y_train_resampled_OCCUPATION)

# Predict missing 'OCCUPATION' values for the test data
predicted_occupation_encoded = best_clf_OCCUPATION.predict(X_test_selected_OCCUPATION)

# Convert the predicted encoded values back to their original categorical values
le_occupation = label_encoders['OCCUPATION']  # Retrieve the label encoder for 'OCCUPATION'
predicted_occupation = le_occupation.inverse_transform(predicted_occupation_encoded)

# Check if the number of predicted values matches the number of missing rows
missing_indices = df[df['OCCUPATION'].isnull()].index

if len(missing_indices) != len(predicted_occupation):
    raise ValueError(f"Length mismatch: {len(missing_indices)} missing values but {len(predicted_occupation)} predictions.")

# Replace the missing 'OCCUPATION' values in the original dataframe
df.loc[missing_indices, 'OCCUPATION'] = predicted_occupation

# Check if missing values are imputed
print(df['OCCUPATION'].isnull().sum())

# Impute Car_Age column

# Replace the original CAR_AGE column in the original DataFrame with the imputed values
df['CAR_AGE'] = df_imputed[:, 0]

# Check if missing values are imputed
print(df['CAR_AGE'].isnull().sum())

# Impute Clm_AMT column

# Split the data
df_train_CLMAMT = df[df['CLM_AMT'] > 0].copy()
df_predict_CLMAMT = df[df['CLM_AMT'] == 0].copy()

# Define features (X) and target (y) for training
X_train_CLMAMT = df_train_CLMAMT[numerical_columns + categorical_columns]  # Ensure columns used in features exist
y_train_CLMAMT = df_train_CLMAMT['CLM_AMT']

X_predict_CLMAMT = df_predict_CLMAMT[numerical_columns + categorical_columns]  # Ensure columns used in prediction exist

# Preprocessing
preprocessor_CLMAMT = ColumnTransformer(
    transformers=[
        ('num', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='mean')),
            ('scaler', StandardScaler())
        ]), numerical_columns),
        
        ('cat', Pipeline(steps=[
            ('imputer', SimpleImputer(strategy='most_frequent')),
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ]), categorical_columns)
    ]
)

# Step 3: Create and fit the model pipeline
model_pipeline_CLMAMT = Pipeline(steps=[
    ('preprocessor', preprocessor_CLMAMT),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Fit the model on the training set
model_pipeline_CLMAMT.fit(X_train_CLMAMT, y_train_CLMAMT)

# Predict CLM_AMT for rows where it was originally 0
y_predicted_CLMAMT = model_pipeline_CLMAMT.predict(X_predict_CLMAMT)

# Fill the $0 CLM_AMT values with the predicted values
df.loc[df['CLM_AMT'] == 0, 'CLM_AMT'] = y_predicted_CLMAMT

# Check that there are no more $0 values
zero_claims_after = df[df['CLM_AMT'] == 0].shape[0]
print(f"Number of $0 claim amounts after replacement: {zero_claims_after}")

# Standardise the Dataset

#Convert 'MALE' to 0 and 'FEMALE' to 1

df['GENDER'] = df['GENDER'].map({'M': 0, 'z_F': 1})

#Mapping of existing values to standardized values
education_mapping = {
    'z_High School': 'High School',
    'PhD': 'PhD',
    'Bachelors': 'Bachelor',
    '<High School': 'High School',
    'Masters': 'Masters',
}

#Replace the values in the EDUCATION column (L)
df['EDUCATION'] = df['EDUCATION'].replace(education_mapping) 
print (" Education Standarised")

# Strip leading/trailing whitespace and standardize to title case
df['OCCUPATION'] = df['OCCUPATION'].str.strip().str.title()

# Replace specific values with the standardized terms
df['OCCUPATION'] = df['OCCUPATION'].replace({
    'Z_Blue Collar': 'Blue Collar',
    'Manager': 'Manager',  # Remove leading space from ' Manager'
    'Professional': 'Professional',
    'Clerical': 'Clerical',
    'Doctor': 'Doctor'
})

print("Names standardized")
print(df['OCCUPATION'].head(20))

