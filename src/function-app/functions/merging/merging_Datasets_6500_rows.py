import pandas as pd

# Load dataset 1
df1 = pd.read_csv('/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/Enriching/cleanedEnriched_Dataset1.csv')

# Load dataset 2
df2 = pd.read_csv('/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/Enriching/cleanedEnriched_Dataset2.csv')

# Load synthesized data
df3 = pd.read_csv('/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/Synthesizing/SynthesisedMethod1.csv')

# Drop the index column in the synthesized dataset 
df3 = df3.drop('index', axis=1)

# Combine the two datasets using concat function
df_concat = pd.concat([df1, df2, df3])

# Set the index to start from 1 and not reset after 1000
df_concat.index = range(1, len(df_concat) + 1)

#Set index name to 'index'
df_concat.index.name = 'index'

# Spit out the file
df_concat.to_csv('/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/Merging/merged_Dataset_6500_rows.csv')
