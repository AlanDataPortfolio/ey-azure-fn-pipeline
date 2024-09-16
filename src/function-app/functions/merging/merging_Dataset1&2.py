#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:15:24 2024

@author: aasnayemgazzalichowdhury
"""

import pandas as pd

# Load dataset 1
df1 = pd.read_csv('/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/Enriching/cleanedEnriched_Dataset1.csv')

# Load dataset 2
df2 = pd.read_csv('/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/Enriching/cleanedEnriched_Dataset2.csv')

# Combine the two datasets using concat function
df_concat = pd.concat([df1, df2])

# Set the index to start from 1 and not reset after 1000
df_concat.index = range(1, len(df_concat) + 1)

#Set index name to 'index'
df_concat.index.name = 'index'

# Spit out the file
df_concat.to_csv('/Users/aasnayemgazzalichowdhury/Desktop/Uni Documents/2024 Session 2/COMP3850/Merging/merged_Dataset.csv')