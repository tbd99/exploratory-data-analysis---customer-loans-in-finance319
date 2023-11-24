import numpy as np
import pandas as pd
from datetime import datetime 
from db_info import DataFrameInfo

def read_csv(filename):
    df_csv = pd.read_csv(filename)
    return df_csv 

filename = 'loan_payments_transformed.csv'
loan_payments_df = read_csv(filename)  # calls the read_csv funciton to load data 
my_instance = DataFrameInfo(loan_payments_df) # initialises an instnce of the class 
column_names = loan_payments_df.columns.tolist() # creates a list of the column headings as strings 
dtypes = my_instance.get_datatypes()   
print(loan_payments_df.head())