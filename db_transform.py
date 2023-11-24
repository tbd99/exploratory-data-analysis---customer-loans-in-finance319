import numpy as np
import pandas as pd
from datetime import datetime 
from db_datatransform import DataTransform
from db_info import DataFrameInfo
from db_info import read_csv

class Plotter():
   '''
   '''
   
class DataFrameTransform():
   '''
   '''
   def __init__(self,df):
      self.dataframe = df 
      
   def drop_column(self,column):
      self.dataframe = self.dataframe.drop(column, axis =1)
      return self.dataframe
   
   

if __name__ == "__main__":
   filename = 'loan_payments.csv'
   loan_payments_df = read_csv(filename)  # calls the read_csv funciton to load data 
   col_to_convert_to_datetime = ['issue_date', 'earliest_credit_line', 'last_payment_date','next_payment_date', 'last_credit_pull_date'] # list of strings specifying columns to be converted
   col_to_convert_to_float = ['term','employment_length']
   col_to_convert_to_str = ['grade', 'sub_grade']
   col_to_convert_to_categorical = ['home_ownership','verification_status','loan_status','payment_plan','purpose','application_type']  
   
   data_transform_instance = DataTransform(loan_payments_df) #initialise instance of class
   
   for i in range(0,len(col_to_convert_to_datetime)): #loops over list of column names
       datetime_format = '%b-%Y'
       data_transform_instance.obj_to_datetime(col_to_convert_to_datetime[i],datetime_format) #calls the obj_to_datetime method of the DataTransform class to convert data

   for i in range(0,len(col_to_convert_to_float)): #loops over list of column names
       data_transform_instance.obj_to_int(col_to_convert_to_float[i])

   for i in range(0,len(col_to_convert_to_str)): #loops over list of column names
       data_transform_instance.obj_to_str(col_to_convert_to_str[i])

   for i in range(0,len(col_to_convert_to_categorical)): #loops over list of column names
       data_transform_instance.obj_to_str(col_to_convert_to_categorical[i])
  

   my_instance = DataFrameInfo(loan_payments_df) # initialises an instnce of the class 
   column_names = loan_payments_df.columns.tolist() # creates a list of the column headings as strings 
   null_columns = []
   print(type(null_columns))
   for i in range (0, len(column_names)):
      null_pc = my_instance.null_percentage(column_names[i])
      print(column_names[i], null_pc)
      if null_pc > 0.0:
        null_columns.append(column_names[i])
   print(null_columns)
   #loan_payments_df.info()
   columns_to_drop = ['mths_since_last_delinq','mths_since_last_record','next_payment_date','mths_since_last_major_derog']
   columns_to_impute = ['funded_amount','term','int_rate','employment_length','collections_12_mths_ex_med',]
   columns_to_drop_null_value_rows = ['last_payment_date','last_credit_pull_date']

   loan_payments_df_copy = loan_payments_df.copy() #create copy of dataframe before removing any values 
   remove_null = DataFrameTransform(loan_payments_df_copy)
   for i in range(0, len(columns_to_drop)):
      loan_payments_df_copy = remove_null.drop_column(columns_to_drop[i])
   column_names_df_copy = loan_payments_df_copy.columns.tolist()
   print(column_names_df_copy)
   #loan_payments_df_copy.info()
   print(loan_payments_df_copy.head(5))

   
   
# drop columns where null values > 50%