#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 11:15:24 2024

@author: aasnayemgazzalichowdhury
"""

import pandas as pd
import os

# Get the directory of the current script
CWD = os.getcwd()

# Construct the relative path to the input dataset
input_file_path_dataset1 = os.path.join(CWD, 'assets', 'data', 'cleaned', 'enriched_dataset1.csv')
input_file_path_dataset2 = os.path.join(CWD, 'assets', 'data', 'cleaned', 'enriched_dataset2.csv')

# Load dataset 1
df1 = pd.read_csv(input_file_path_dataset1)

# Load dataset 2
df2 = pd.read_csv(input_file_path_dataset2)

# Combine the two datasets using concat function
df_concat = pd.concat([df1, df2])

# Set the index to start from 1 and not reset after 1000
df_concat.index = range(1, len(df_concat) + 1)

#Set index name to 'index'
df_concat.index.name = 'index'

# Construct the relative path to the output dataset
output_file_path = os.path.join(CWD, 'assets', 'data', 'merged', 'merged_dataset_1_2.csv')

# Spit out the file
df_concat.to_csv(output_file_path)