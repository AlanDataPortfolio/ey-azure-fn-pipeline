# Correlation Test for Occupation

import pandas as pd
from scipy import stats

# Load the dataset
df = pd.read_csv('D:/Documents/GitHub/PACE/ey-azure-fn-pipeline/assets/data/raw/dataset3.csv')

# Remove the '$' and ',' from INCOME column and convert it to numeric
df['INCOME'] = df['INCOME'].replace('[\$,]', '', regex=True).astype(float)

# Remove rows where INCOME or OCCUPATION is missing
df = df[df['INCOME'].notnull() & df['OCCUPATION'].notnull()]

# Remove rows where INCOME is zero since we don't want to use them
df = df[df['INCOME'] > 0]

# Remove the 'z_' prefix from OCCUPATION if it exists
df['OCCUPATION'] = df['OCCUPATION'].str.replace('z_', '')

# Group the data by OCCUPATION and calculate the mean income for each group
occupation_income = df.groupby('OCCUPATION')['INCOME'].mean()
print("\nMean income per occupation:")
print(occupation_income)

# Perform a one-way ANOVA to test if income differs significantly between occupations
occupation_groups = [group['INCOME'].values for name, group in df.groupby('OCCUPATION')]
anova_result = stats.f_oneway(*occupation_groups)

print("\nANOVA test result:")
print(f"F-statistic: {anova_result.statistic}, p-value: {anova_result.pvalue}")

# Interpret the ANOVA result
if anova_result.pvalue < 0.05:
    print("There is a significant relationship between OCCUPATION and INCOME.")
else:
    print("There is no significant relationship between OCCUPATION and INCOME.")

