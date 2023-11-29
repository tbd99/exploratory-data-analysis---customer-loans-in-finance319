
from datetime import datetime 
from db_datatransform import DataTransform
from db_info import DataFrameInfo
from db_info import read_csv
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px 


class Plotter():
   '''
   This class contains functions to plot data
   '''
   def __init__(self,df):
      self.dataframe = df 

   def plot_hist(self,column):
      '''
      This function plots a histogram of the specified column's data
      '''
      self.dataframe[column].hist(bins=100)
      title = str(column)
      plt.title(title)
      plt.show() 
   
   def plot_KDE(self,column):
      '''
      THis function plots KDE plot of the specified column's data 
      '''
      sns.histplot(data=self.dataframe, x=column, kde=True)
      sns.despine()
      title = str(column)
      plt.title(title)
      plt.show()

   def plot_box_whiskers(self,column):
      '''
      This function plots a box and whisker plot for the specified column
      '''
      fig = px.box(self.dataframe, y=column,width=600, height=500, title=str(column))
      fig.show()

   
class DataFrameTransform():
   '''
   This class contains functions to remove null values from data and functions for data transformations 
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
   
   def impute_na_with_mean(self,column):
      '''
      This function replaces null values in a specified column with the mean of the column
      '''
      self.dataframe[column] = self.dataframe[column].fillna(self.dataframe[column].median())
      return self.dataframe
   
   def impute_na_with_mode(self,column):
      '''
      This function replaces null values in a specified column with the mode of the column
      '''
      self.dataframe[column] = self.dataframe[column].fillna(self.dataframe[column].mode()[0])
      return self.dataframe
   
   def impute_na_with_median(self,column):
      '''
      This function replaces null values in a specified column with the median of the column
      '''
      self.dataframe[column] = self.dataframe[column].fillna(self.dataframe[column].median())
      return self.dataframe
   
   def log_transform(self,column):
      '''
      This function performs a log transform on the specified column, excluding 0 values
      '''
      self.dataframe[column] = self.dataframe[column].map(lambda i: np.log(i) if i > 0 else 0)
      return self.dataframe
   
   def box_cox_transform(self,column):
      '''
      This function performs a box cox transformation on the specified column 
      '''
      boxcox_population = self.dataframe[column]
      boxcox_population= stats.boxcox(boxcox_population)
      boxcox_population= pd.Series(boxcox_population[0])  
      self.dataframe[column] = boxcox_population
      return self.dataframe
   
   def remove_top_val(self,column):
      '''
      This function removes the row corresponding to the maximum value for the specified column
      '''
      max_val = self.dataframe[column].max()
      self.dataframe = self.dataframe.drop(self.dataframe[self.dataframe[column] == max_val].index)
      return self.dataframe
   
   def remove_negatives(self,column):
      '''
      This function removes rows containining negative values in the specified column
      '''
      self.dataframe = self.dataframe[self.dataframe[column] >= 0]
      return self.dataframe



if __name__ == "__main__":
   filename = 'loan_payments.csv'
   loan_payments_df = read_csv(filename)  # calls the read_csv funciton to load data 
   col_to_convert_to_datetime = ['issue_date', 'earliest_credit_line', 'last_payment_date','next_payment_date', 'last_credit_pull_date'] # list of strings specifying columns to be converted
   col_to_convert_to_float = ['term','employment_length']
   col_to_convert_to_str = ['grade', 'sub_grade']
   col_to_convert_to_categorical = ['home_ownership','verification_status','loan_status','payment_plan','purpose','application_type']  
   
   data_transform_instance = DataTransform(loan_payments_df) #initialise instance of class for data type transformations
   
   for i in range(0,len(col_to_convert_to_datetime)): #loops over list of column names
       datetime_format = '%b-%Y'
       data_transform_instance.obj_to_datetime(col_to_convert_to_datetime[i],datetime_format) #calls the obj_to_datetime method of the DataTransform class to convert data

   for i in range(0,len(col_to_convert_to_float)): #loops over list of column names
       data_transform_instance.obj_to_int(col_to_convert_to_float[i])

   for i in range(0,len(col_to_convert_to_str)): #loops over list of column names
       data_transform_instance.obj_to_str(col_to_convert_to_str[i])

   for i in range(0,len(col_to_convert_to_categorical)): #loops over list of column names
       data_transform_instance.obj_to_str(col_to_convert_to_categorical[i])
  

   my_instance = DataFrameInfo(loan_payments_df) # initialises an instnce of the class to obtain information on the dataframe
   column_names = loan_payments_df.columns.tolist() # creates a list of the column headings as strings 
   loan_payments_df = loan_payments_df.drop(columns=loan_payments_df.columns[0], axis=1) # remove additional index column
   null_columns = []
   for i in range (0, len(column_names)):
      null_pc = my_instance.null_percentage(column_names[i])
      #print(column_names[i], null_pc)
      if null_pc > 0.0:
        null_columns.append(column_names[i])
   
   columns_to_drop = ['mths_since_last_delinq','mths_since_last_record','next_payment_date','mths_since_last_major_derog'] # columns with > 50% null values, drop entire column
   columns_to_impute = ['funded_amount','term','int_rate','employment_length'] # columns with a small amount of null values to be imputed
   columns_to_drop_null_value_rows = ['last_payment_date','last_credit_pull_date','collections_12_mths_ex_med'] # columns with < 1% null values, can drop rows with null values 
   loan_payments_df_copy = loan_payments_df.copy() #create copy of dataframe before removing any values for data preservation

   remove_null = DataFrameTransform(loan_payments_df_copy) # initialises an instance of the DataFrameTransform class for dealing with null values 
   for i in range(0, len(columns_to_drop)):
      loan_payments_df_copy = remove_null.drop_column(columns_to_drop[i]) # drops columns with > 50 % null values
   for i in range(0, len(columns_to_drop_null_value_rows)):
      loan_payments_df_copy = remove_null.drop_null_rows(columns_to_drop_null_value_rows[i]) # drops rows with null values in specific columns
    
   loan_payments_df_copy = remove_null.impute_na_with_mode('term') # impute null values with mode, as this is categorical data
   loan_payments_df_copy = remove_null.impute_na_with_median('employment_length') # impute null value with median, to keep all values as whole numbers 
   loan_payments_df_copy = remove_null.impute_na_with_mean('funded_amount') # impute null values with mean as data is continuous with a normal distribution 
   loan_payments_df_copy = remove_null.impute_na_with_mean('int_rate') # impute null values with mean as data is continuous with a normal distribution
   
   
   my_instance_copy = DataFrameInfo(loan_payments_df_copy) # initialises an instnce of the class to obtain information on the dataframe
   column_names_copy = loan_payments_df_copy.columns.tolist() # creates a list of the column headings as strings 
   null_columns_copy = []
   for i in range (0, len(column_names_copy)): # to check that the correct columns and rows have been dropped and view null percentages to confirm 
      null_pc = my_instance_copy.null_percentage(column_names_copy[i])
      print(column_names_copy[i], null_pc)
      if null_pc > 0.0:
        null_columns_copy.append(column_names_copy[i]) # append columns with null values to list 
   #print(null_columns_copy)
   
   for i in range(0, len(columns_to_impute)):
      mean = my_instance_copy.get_mean(columns_to_impute[i])
      #print('MEAN', columns_to_impute[i], mean)

   for i in range(0, len(columns_to_impute)):
      stdv = my_instance_copy.get_stdev(columns_to_impute[i])
      #print('STDEV', columns_to_impute[i], stdv)

   for i in range(0, len(columns_to_impute)):
       mode = my_instance_copy.get_mode(columns_to_impute[i])
       #print('MODE', columns_to_impute[i], mode)
    
   for i in range(0, len(columns_to_impute)):
       median = my_instance_copy.get_median(columns_to_impute[i])
       #print('MEDIAN', columns_to_impute[i], median)
    
   for i in range(0, len(columns_to_impute)):
       ranges = my_instance_copy.get_range(columns_to_impute[i])
       #print('RANGE',columns_to_impute[i], ranges)
    
   for i in range(0, len(columns_to_impute)):
       my_instance_copy.get_normal_dist(columns_to_impute[i])
   
   plotter_instance = Plotter(loan_payments_df_copy) # initialise an instance of the plotter class for data visualisation

   loan_df_skew = loan_payments_df_copy.skew(axis=0,numeric_only = True) # obtain the skew of each numeric column in the dataframe
   print(loan_df_skew)
   check_skewed_columns = loan_df_skew.index
   skewed_columns = []
   for i in range(0, len(loan_df_skew)): 
      if loan_df_skew.iloc[i] > 2 or loan_df_skew.iloc[i] < -2: # append columns with a skew < -2 or > 2 to the list
         skewed_columns.append(check_skewed_columns[i])
   #print(skewed_columns)

   columns_to_remove = ['id','member_id','delinq_2yrs','inq_last_6mths','collections_12_mths_ex_med'] # skewed columns that do not need to be transformed
   for i in range(0, len(columns_to_remove)):
      skewed_columns.remove(columns_to_remove[i]) # removes columns that represent IDs or are categorical data
   
   #print(skewed_columns)
   zero_columns_to_remove = ['out_prncp','out_prncp_inv','total_rec_late_fee','collection_recovery_fee'] # list of columns containing a majority of 0 values
   for i in range(0, len(zero_columns_to_remove)):
      skewed_columns.remove(zero_columns_to_remove[i]) # removes columns that contain a majority of 0 values (median =0), meaning transformations are not appropriate
   loan_payments_df_transformed = loan_payments_df_copy.copy()
   transform_instance = DataFrameTransform(loan_payments_df_transformed) # initialise an instance of the class with a copy of the df 

   for i in range(0, len(skewed_columns)): 
      transform_instance.log_transform(skewed_columns[i]) # perform log transform on selected columns 
   
   loan_df_skew_log = loan_payments_df_transformed.skew(axis=0,numeric_only = True) # obtain the skew of each numeric column in the dataframe to check results of the transformation
   print(loan_df_skew_log) 
   
   loan_payments_df_transformed = transform_instance.remove_top_val('total_rec_late_fee') 
   loan_payments_df_transformed = transform_instance.remove_top_val('total_rec_late_fee') 
   loan_payments_df_transformed = transform_instance.remove_top_val('open_accounts') 
   loan_payments_df_transformed = transform_instance.remove_top_val('total_rec_late_fee') 
   loan_payments_df_transformed = transform_instance.remove_top_val('total_rec_late_fee') 
   loan_payments_df_transformed = transform_instance.remove_top_val('total_accounts') 
   loan_payments_df_transformed = transform_instance.remove_top_val('collection_recovery_fee') 
   loan_payments_df_transformed = transform_instance.remove_top_val('collection_recovery_fee') 

   plotter_log_transformed = Plotter(loan_payments_df_transformed) # initialise an instanc of the plotter class with transformed data
   #for i in range(0, len(column_names_copy)): 
    #  plotter_log_transformed.plot_KDE(column_names_copy[i])
   #plotter_log_transformed.plot_box_whiskers('recoveries')
   
   #for i in range(0, len(column_names_copy)): 
   plotter_log_transformed.plot_box_whiskers('open_accounts')
   plotter_log_transformed.plot_box_whiskers('total_rec_late_fee')
   plotter_log_transformed.plot_box_whiskers('total_accounts')
   plotter_log_transformed.plot_box_whiskers('collection_recovery_fee')

   


   
    
       


   


   
   
