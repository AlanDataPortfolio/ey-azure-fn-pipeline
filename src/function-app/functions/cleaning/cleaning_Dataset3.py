# CLEANING DATASET 3
# Noor's Version

# IMPORT NECESSARY LIBRARIES
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

# LOAD DATASET

# Get the directory of the current script
script_dir = os.path.dirname(__file__)

# Construct the relative path to the input dataset
input_file_path = os.path.join(script_dir, '..', '..', '..', '..', 'assets', 'data', 'raw', 'dataset3.csv')

# Load the dataset
print("Loading dataset...")
df = pd.read_csv(input_file_path)

# CLEAN THE DATASET

# Function to clean and convert columns to numeric
def clean_numeric_column(df, column):
    """Cleans and converts columns to numeric values."""
    df[column] = df[column].replace(r'[\$,]', '', regex=True).astype(float)

# Columns to convert
columns_to_convert = ['INCOME', 'HOME_VAL', 'BLUEBOOK', 'OLDCLAIM', 'CLM_AMT']
for column in columns_to_convert:
    clean_numeric_column(df, column)

print("Numeric columns cleaned and converted.")
print(df.dtypes)

# SPLIT INTO NUMERICAL AND CATEGORICAL COLUMNS
numerical_columns = ['KIDSDRIV', 'AGE', 'HOMEKIDS', 'YOJ', 'TRAVTIME', 'TIF', 'MVR_PTS', 'INCOME', 'HOME_VAL', 'BLUEBOOK', 'CLM_AMT']
categorical_columns = ['PARENT1', 'MSTATUS', 'GENDER', 'EDUCATION', 'CAR_USE', 'CAR_TYPE', 'RED_CAR', 'REVOKED', 'URBANICITY', 'OCCUPATION']

# Filter out missing columns
numerical_columns = [col for col in numerical_columns if col in df.columns]
categorical_columns = [col for col in categorical_columns if col in df.columns]

print(f"Numerical columns: {numerical_columns}")
print(f"Categorical columns: {categorical_columns}")

# PREPARE DATASET

# Select the relevant numerical and categorical features for imputation
features_for_imputation = ['YOJ', 'INCOME', 'HOME_VAL', 'BLUEBOOK', 'AGE', 'PARENT1', 
                           'MSTATUS', 'GENDER', 'EDUCATION', 'CAR_USE', 'CAR_TYPE', 
                           'RED_CAR', 'REVOKED', 'URBANICITY', 'OCCUPATION', 'CAR_AGE']

# Copy the relevant columns into a new DataFrame
df_impute = df[features_for_imputation].copy()

# ENCODE CATEGORICAL VARIABLES
label_encoders = {}
for col in ['PARENT1', 'MSTATUS', 'GENDER', 'EDUCATION', 'CAR_USE', 
            'CAR_TYPE', 'RED_CAR', 'REVOKED', 'URBANICITY', 'OCCUPATION']:
    le = LabelEncoder()
    df_impute[col] = le.fit_transform(df_impute[col].astype(str))
    label_encoders[col] = le

print("Categorical variables encoded.")

# INITIALIZE KNN IMPUTER
knn_imputer = KNNImputer(n_neighbors=5)

# Apply KNN imputation to the data
df_imputed = knn_imputer.fit_transform(df_impute)
print("KNN imputation applied.")

# Replace the original AGE column in the original DataFrame with the imputed values
df['AGE'] = df_imputed[:, 0]

print("AGE column imputed.")
print(f"Missing values in 'AGE': {df['AGE'].isnull().sum()}")

# IMPUTE YOJ COLUMN

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
        ('num', Pipeline(steps=[('imputer', SimpleImputer(strategy='mean')), ('scaler', StandardScaler())]), numerical_columns_YOJ),
        ('cat', Pipeline(steps=[('imputer', SimpleImputer(strategy='most_frequent')), ('onehot', OneHotEncoder(handle_unknown='ignore'))]), categorical_columns_YOJ)
    ]
)

# DEFINE RANDOM FOREST REGRESSOR FOR YOJ IMPUTATION
pipeline_impute_YOJ = Pipeline(steps=[
    ('preprocessor', preprocessor_YOJ),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# DEFINE PARAMETER GRID FOR YOJ
param_grid_YOJ = {'regressor__n_estimators': [50, 100, 200], 'regressor__max_depth': [None, 10, 20, 30]}

# Perform GridSearchCV for YOJ
grid_search_YOJ = GridSearchCV(pipeline_impute_YOJ, param_grid_YOJ, cv=5, scoring='neg_mean_squared_error')
grid_search_YOJ.fit(X_complete_YOJ, y_complete_YOJ)

# Predict missing YOJ values using the best model
best_pipeline_YOJ = grid_search_YOJ.best_estimator_
y_predicted_YOJ = best_pipeline_YOJ.predict(X_missing_YOJ)

# Fill missing values for YOJ
df.loc[df['YOJ'].isnull(), 'YOJ'] = y_predicted_YOJ

print(f"Remaining missing values in 'YOJ': {df['YOJ'].isnull().sum()}")

# IMPUTE INCOME COLUMN
print(f"Missing values in 'INCOME': {df['INCOME'].isnull().sum()}")

# IMPUTE HOME_VAL COLUMN
df['HOME_VAL'] = df_imputed[:, 0]
print(f"Missing values in 'HOME_VAL': {df['HOME_VAL'].isnull().sum()}")

# IMPUTE OCCUPATION COLUMN

# Split the data into rows with known and unknown 'OCCUPATION'
train_data_OCCUPATION = df_impute[df['OCCUPATION'].notnull()]
test_data_OCCUPATION = df_impute[df['OCCUPATION'].isnull()]

if test_data_OCCUPATION.empty:
    print("No missing 'OCCUPATION' values to predict.")
else:
    X_train_OCCUPATION = train_data_OCCUPATION.drop(['OCCUPATION'], axis=1)
    y_train_OCCUPATION = train_data_OCCUPATION['OCCUPATION']

    X_test_OCCUPATION = test_data_OCCUPATION.drop(['OCCUPATION'], axis=1)

    imputer_OCCUPATION = SimpleImputer(strategy='most_frequent')
    X_train_OCCUPATION = pd.DataFrame(imputer_OCCUPATION.fit_transform(X_train_OCCUPATION), columns=X_train_OCCUPATION.columns)
    X_test_OCCUPATION = pd.DataFrame(imputer_OCCUPATION.transform(X_test_OCCUPATION), columns=X_test_OCCUPATION.columns)

    smote_OCCUPATION = SMOTE(random_state=42)
    X_train_resampled_OCCUPATION, y_train_resampled_OCCUPATION = smote_OCCUPATION.fit_resample(X_train_OCCUPATION, y_train_OCCUPATION)

    param_grid_OCCUPATION = {
        'n_estimators': [100, 200, 500],
        'max_features': ['sqrt', 'log2', None],
        'max_depth': [10, 20, 30, None],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'bootstrap': [True, False]
    }

    clf_OCCUPATION = RandomForestClassifier(random_state=42)
    random_search_OCCUPATION = RandomizedSearchCV(clf_OCCUPATION, param_distributions=param_grid_OCCUPATION, n_iter=10, cv=3, random_state=42, n_jobs=-1)
    random_search_OCCUPATION.fit(X_train_resampled_OCCUPATION, y_train_resampled_OCCUPATION)

    selector_OCCUPATION = SelectFromModel(random_search_OCCUPATION.best_estimator_, threshold='median')
    X_train_selected_OCCUPATION = selector_OCCUPATION.fit_transform(X_train_resampled_OCCUPATION, y_train_resampled_OCCUPATION)
    X_test_selected_OCCUPATION = selector_OCCUPATION.transform(X_test_OCCUPATION)

    best_clf_OCCUPATION = random_search_OCCUPATION.best_estimator_
    best_clf_OCCUPATION.fit(X_train_selected_OCCUPATION, y_train_resampled_OCCUPATION)

    predicted_occupation_encoded = best_clf_OCCUPATION.predict(X_test_selected_OCCUPATION)

    le_occupation = label_encoders['OCCUPATION'] 
    predicted_occupation = le_occupation.inverse_transform(predicted_occupation_encoded)

    missing_indices = df[df['OCCUPATION'].isnull()].index

    if len(missing_indices) != len(predicted_occupation):
        raise ValueError(f"Length mismatch: {len(missing_indices)} missing values but {len(predicted_occupation)} predictions.")

    df.loc[missing_indices, 'OCCUPATION'] = predicted_occupation

print(f"Missing values in 'OCCUPATION': {df['OCCUPATION'].isnull().sum()}")

# STANDARDIZATION
print("Standardizing columns...")

# GENDER
df['GENDER'] = df['GENDER'].map({'M': 0, 'z_F': 1})

# EDUCATION
education_mapping = {'z_High School': 'High School', 'PhD': 'PhD', 'Bachelors': 'Bachelor', '<High School': 'High School', 'Masters': 'Masters'}
df['EDUCATION'] = df['EDUCATION'].replace(education_mapping)

# OCCUPATION
df['OCCUPATION'] = df['OCCUPATION'].str.strip().str.title().replace({
    'Z_Blue Collar': 'Blue Collar', 'Manager': 'Manager', 'Professional': 'Professional', 'Clerical': 'Clerical', 'Doctor': 'Doctor'
})

print("Dataset standardized.")

# SAVE CLEANED DATASET
output_file_path = os.path.join(script_dir, '..', '..', 'assets', 'data', 'cleaned', 'cleaned_Dataset3.csv')
df.to_csv(output_file_path, index=False)
print(f"Cleaned dataset saved to {output_file_path}.")
