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

