import numpy as np
import pandas as pd
from datetime import datetime 
from db_info import DataFrameInfo
from db_info import read_csv

class Plotter():
   '''
   '''
   
class DataFrameTransform():
   '''
   '''
   

if __name__ == "__main__":
   filename = 'loan_payments_transformed.csv'
   loan_payments_df = read_csv(filename)  # calls the read_csv funciton to load data 
   my_instance = DataFrameInfo(loan_payments_df) # initialises an instnce of the class 
   column_names = loan_payments_df.columns.tolist() # creates a list of the column headings as strings 
   null_columns = []
   print(type(null_columns))
   for i in range (0, len(column_names)):
      null_pc = my_instance.null_percentage(column_names[i])
      if null_pc > 0.0:
        null_columns.append(column_names[i])
   print(null_columns)

   
