
from datetime import datetime 
from db_datatransform import DataTransform
from db_info import DataFrameInfo
from db_info import read_csv
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px 
import seaborn as sns
import pickle as pkl

class Plotter():
   '''
   This class contains functions to plot data
   Attributes:
    df (pd DataFrame): The dataframe to be evaluated 
   '''
   def __init__(self,df):
      self.dataframe = df 

   def plot_hist(self,column):
      '''
      This function plots a histogram of the specified column
      '''
      self.dataframe[column].hist(bins=100)
      title = str(column)
      plt.title(title)
      plt.show() 
   
   def plot_KDE(self,column):
      '''
      This function plots KDE plot of the specified column
      '''
      sns.histplot(data=self.dataframe, x=column, kde=True)
      sns.despine()
      title = str(column)
      plt.title(title)
      #plt.show()

   def plot_box_whiskers(self,column):
      '''
      This function plots a box and whisker plot for the specified column
      '''
      fig = px.box(self.dataframe, y=column,width=600, height=500, title=str(column))
      fig.show()
   
   def plot_corr_matrix(self):
      '''
      This funciton plots a correlation heatmap of the dataframe for numeric values
      '''
      sns.heatmap(self.dataframe.select_dtypes('number').corr(), annot=True, cmap='coolwarm', xticklabels=True, yticklabels=True)
      plt.show()
   
   def plot_bar_chart(self,my_data,x_axis,y_axis):
      '''
      This funciton plots a bar chart for a given dataset and specified axes
      '''
      sns.barplot(data=my_data, y=y_axis, x=x_axis)
      plt.show()
   
   def plot_countplot(self,column):
      '''
      This function plots a count plot for the specified column
      '''
      sns.countplot(self.dataframe[column]).set(title=column)
      #plt.show()
   
class DataFrameTransform():
   '''
   This class contains functions to remove null values from data and functions for data transformations 
   Attributes:
    df (pd DataFrame): The dataframe to be evaluated 
   '''
   def __init__(self,df):
      self.dataframe = df 
      
   def drop_column(self,column):
      '''
      This function drops the specified column from the dataframe
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
      self.dataframe[column] = pd.Series((stats.boxcox(self.dataframe[column]))[0]) 
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



if __name__ == "__main__": # guard added to ensure code below only runs when the script is executed directly 
   filename = 'loan_payments.csv'
   loan_payments_df = read_csv(filename)  # calls the read_csv funciton to load data 

   col_to_convert_to_datetime = ['issue_date', 'earliest_credit_line', 'last_payment_date','next_payment_date', 'last_credit_pull_date'] # list of strings specifying columns to be converted
   col_to_convert_to_float = ['term','employment_length'] # list of strings of column names
   col_to_convert_to_str = ['grade', 'sub_grade'] # list of strings of column names
   col_to_convert_to_categorical = ['home_ownership','verification_status','loan_status','payment_plan','purpose','application_type']  # list of strings of column names
   
   data_transform_instance = DataTransform(loan_payments_df) # initialise instance of class for data type transformations
   
   for i in range(0,len(col_to_convert_to_datetime)): # loops over list of column names
       datetime_format = '%b-%Y'
       data_transform_instance.obj_to_datetime(col_to_convert_to_datetime[i],datetime_format) # calls the obj_to_datetime method to convert data to datetime

   for i in range(0,len(col_to_convert_to_float)): # loops over list of column names
       data_transform_instance.obj_to_int(col_to_convert_to_float[i]) # calls the obj_to_int method to convert data to int

   for i in range(0,len(col_to_convert_to_str)): # loops over list of column names
       data_transform_instance.obj_to_str(col_to_convert_to_str[i]) # calls the obj_to_string method to convert data to str

   for i in range(0,len(col_to_convert_to_categorical)): #loops over list of column names
       data_transform_instance.obj_to_cat(col_to_convert_to_categorical[i]) # calls the obj_to_ method to convert data to categorical
  

   nulls_info_instance = DataFrameInfo(loan_payments_df) # initialises an instnce of the class to obtain information on the dataframe
   column_names = loan_payments_df.columns.tolist() # creates a list of the column headings as strings 
   loan_payments_df = loan_payments_df.drop(columns=loan_payments_df.columns[0], axis=1) # remove additional index column
   null_columns = [] # initialise list of null columns
   for i in range (0, len(column_names)):
      null_pc = nulls_info_instance.null_percentage(column_names[i])
      #print(column_names[i], null_pc)
      if null_pc > 0.0:
        null_columns.append(column_names[i]) # append to list of columns if there are any null values 
   
   columns_to_drop = ['mths_since_last_delinq','mths_since_last_record','next_payment_date','mths_since_last_major_derog'] # list of strings of columns with > 50% null values, drop entire column
   columns_to_impute = ['funded_amount','term','int_rate','employment_length'] # list of strings of columns with a small amount of null values to be imputed
   columns_to_drop_null_value_rows = ['last_payment_date','last_credit_pull_date','collections_12_mths_ex_med'] # list of strings of columns with < 1% null values, can drop rows with null values 

   loan_payments_df_copy = loan_payments_df.copy() #create copy of dataframe before removing any values for data preservation

   remove_null_instance = DataFrameTransform(loan_payments_df_copy) # initialises an instance of the DataFrameTransform class for dealing with null values 
   for i in range(0, len(columns_to_drop)):
      loan_payments_df_copy = remove_null_instance.drop_column(columns_to_drop[i]) # drops columns with > 50 % null values
   for i in range(0, len(columns_to_drop_null_value_rows)):
      loan_payments_df_copy = remove_null_instance.drop_null_rows(columns_to_drop_null_value_rows[i]) # drops rows with null values in specific columns
   
   df_info_instance = DataFrameInfo(loan_payments_df_copy) # initialises an instnce of the class to obtain information on the dataframe to decide how to impute remaining nulls
   
   for i in range(0, len(columns_to_impute)):
      mean = df_info_instance.get_mean(columns_to_impute[i])
      #print('MEAN', columns_to_impute[i], mean)

   for i in range(0, len(columns_to_impute)):
      stdv = df_info_instance.get_stdev(columns_to_impute[i])
      #print('STDEV', columns_to_impute[i], stdv)

   for i in range(0, len(columns_to_impute)):
       mode = df_info_instance.get_mode(columns_to_impute[i])
       #print('MODE', columns_to_impute[i], mode)
    
   for i in range(0, len(columns_to_impute)):
       median = df_info_instance.get_median(columns_to_impute[i])
       #print('MEDIAN', columns_to_impute[i], median)
    
   for i in range(0, len(columns_to_impute)):
       ranges = df_info_instance.get_range(columns_to_impute[i])
       #print('RANGE',columns_to_impute[i], ranges)
    
   for i in range(0, len(columns_to_impute)):
       df_info_instance.get_normal_dist(columns_to_impute[i])
   
   loan_payments_df_copy = remove_null_instance.impute_na_with_mode('term') # impute null values with mode, as this is categorical data
   loan_payments_df_copy = remove_null_instance.impute_na_with_median('employment_length') # impute null value with median, to keep all values as whole numbers 
   loan_payments_df_copy = remove_null_instance.impute_na_with_mean('funded_amount') # impute null values with mean as data is continuous with a normal distribution 
   loan_payments_df_copy = remove_null_instance.impute_na_with_mean('int_rate') # impute null values with mean as data is continuous with a normal distribution
   
   column_names_copy = loan_payments_df_copy.columns.tolist() # creates a list of the column headings as strings 
   null_columns_copy = []
   for i in range (0, len(column_names_copy)): # to check that the correct columns and rows have been dropped and view null percentages to confirm 
      null_pc = df_info_instance.null_percentage(column_names_copy[i])
      #print(column_names_copy[i], null_pc)
      if null_pc > 0.0:
        null_columns_copy.append(column_names_copy[i]) # append columns with null values to list 
   #print(null_columns_copy) # check print to ensure correct columns and rows have been dropped 
   
   plotter_instance = Plotter(loan_payments_df_copy) # initialise an instance of the plotter class for data visualisation
    # visualise data to observe skew
   #for i in range(0, len(column_names_copy)):
    #  plotter_instance.plot_hist(column_names_copy[i])

    # for i in range(0, len(column_names_copy)):
     # plotter_instance.plot_KDE(column_names_copy[i])

   loan_df_skew = loan_payments_df_copy.skew(axis=0,numeric_only = True) # obtain the skew of each numeric column in the dataframe
   # print(loan_df_skew)
   check_skewed_columns = loan_df_skew.index
   skewed_columns = []
   for i in range(0, len(loan_df_skew)): 
      if loan_df_skew.iloc[i] > 2 or loan_df_skew.iloc[i] < -2: # append columns with a skew < -2 or > 2 to the list
         skewed_columns.append(check_skewed_columns[i])
  

   skewed_columns_to_ignore = ['id','member_id','delinq_2yrs','inq_last_6mths','collections_12_mths_ex_med'] # skewed columns that do not need to be transformed
   for i in range(0, len(skewed_columns_to_ignore)):
      skewed_columns.remove(skewed_columns_to_ignore[i]) # removes columns that represent IDs or are categorical data from list of skewed columns
   #print(skewed_columns)
   zero_maj_skewed_columns_to_ignore = ['out_prncp','out_prncp_inv','total_rec_late_fee','collection_recovery_fee'] # list of columns containing a majority of 0 values
   for i in range(0, len(zero_maj_skewed_columns_to_ignore)):
      skewed_columns.remove(zero_maj_skewed_columns_to_ignore[i]) # removes columns that contain a majority of 0 values (median =0), meaning transformations are not appropriate
   # print(f"WOOOOOOOO{skewed_columns}")
   loan_payments_df_transformed = loan_payments_df_copy.copy() # create copy of transformed data with appropriate naming

   transform_instance = DataFrameTransform(loan_payments_df_transformed) # initialise an instance of the class with the transformed dataframe

   for i in range(0, len(skewed_columns)): 
      transform_instance.log_transform(skewed_columns[i]) # perform log transform on selected skewed columns columns 
   
   loan_df_skew_log = loan_payments_df_transformed.skew(axis=0,numeric_only = True) # obtain the skew of each numeric column in the dataframe to check results of the transformation
   # print(loan_df_skew_log) 
    
   transformed_plotter_instance = Plotter(loan_payments_df_transformed) # initialise an instance of the plotter class for data visualisation
    # visualise data to identify outliers 
   #for i in range(0, len(column_names_copy)):
    #  transformed_plotter_instance.plot_hist(column_names_copy[i])

   #for i in range(0, len(column_names_copy)):
    #  transformed_plotter_instance.plot_KDE(column_names_copy[i])
   
   # remove outliers observed in visualisation of data 
   columns_with_max_outliers = ['total_rec_late_fee','open_accounts','total_accounts','collection_recovery_fee'] # list of strings of column names for columns with high values to remove
   for i in range(0, len(columns_with_max_outliers)):
      loan_payments_df_transformed = transform_instance.remove_top_val(columns_with_max_outliers[i]) # remove max values

   # additional to remove highest val again
   loan_payments_df_transformed = transform_instance.remove_top_val('collection_recovery_fee') 
   loan_payments_df_transformed = transform_instance.remove_top_val('total_rec_late_fee') 

   columns_with_negatives = ['recoveries','last_payment_amount'] # list of strings of column names for columns with -ve values to remove
   for i in range(0, len(columns_with_negatives)):
      loan_payments_df_transformed = transform_instance.remove_negatives(columns_with_negatives[i]) # remove negative values

   correlated_columns = ['funded_amount','funded_amount_inv','total_payment_inv','total_rec_prncp','out_prncp_inv'] # drops some columns with correlation > 0.9 to give no correlation values above 0.9 #'instalment',
   correlation_drop = DataFrameTransform(loan_payments_df_transformed) #initialise and instance of the class for removing correlated columns
   for i in range(0, len(correlated_columns)):
      loan_payments_df_transformed = correlation_drop.drop_column(correlated_columns[i])

 # initialise an instanc of the plotter class with transformed data
   cleaned_data_plotter_instance = Plotter(loan_payments_df_transformed)   
   cleaned_data_plotter_instance.plot_corr_matrix()
   
   loan_payments_df_transformed.to_pickle('cleaned_data.pickle') # saves data in pickle format to preserve data types/data transformations 
