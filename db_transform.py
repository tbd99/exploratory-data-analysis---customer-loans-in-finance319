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
      '''
      This function deletes a specified column from the dataframe
      '''
      self.dataframe = self.dataframe.drop(column, axis =1)
      return self.dataframe
   
   def drop_null_rows(self,column):
      '''
      This function deletes all rows containing null values in the specified column
      '''
      self.dataframe = self.dataframe.dropna(subset=[column])
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
   
   columns_to_drop = ['mths_since_last_delinq','mths_since_last_record','next_payment_date','mths_since_last_major_derog'] # columns with > 50% null values, drop entire column
   columns_to_impute = ['funded_amount','term','int_rate','employment_length'] # columns with a small amount of null values to be imputed
   columns_to_drop_null_value_rows = ['last_payment_date','last_credit_pull_date','collections_12_mths_ex_med'] # columns with < 1% null values, can drop rows with null values 
   loan_payments_df_copy = loan_payments_df.copy() #create copy of dataframe before removing any values 

   remove_null = DataFrameTransform(loan_payments_df_copy) # initialises an instance of the DataFrameTransform class 
   for i in range(0, len(columns_to_drop)):
      loan_payments_df_copy = remove_null.drop_column(columns_to_drop[i]) # drops columns with > 50 % null values
   for i in range(0, len(columns_to_drop_null_value_rows)):
      loan_payments_df_copy = remove_null.drop_null_rows(columns_to_drop_null_value_rows[i]) # drops rows with null values in specific columns
    
   
   my_instance_copy = DataFrameInfo(loan_payments_df_copy) # initialises an instnce of the class 

   column_names_copy = loan_payments_df_copy.columns.tolist() # creates a list of the column headings as strings 
   null_columns_copy = []
   for i in range (0, len(column_names_copy)): # to check that the correct columns and rows have been dropped 
      null_pc = my_instance_copy.null_percentage(column_names_copy[i])
      print(column_names_copy[i], null_pc)
      if null_pc > 0.0:
        null_columns_copy.append(column_names_copy[i]) # append columns with null values to list 
   print(null_columns_copy)
   
   


   
   
