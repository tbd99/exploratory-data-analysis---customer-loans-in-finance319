import numpy as np
import pandas as pd
from datetime import datetime 

def read_csv(filename):
    df_csv = pd.read_csv(filename)
    return df_csv 

class DataFrameInfo():
    '''
    This class
    '''
    def __init__(self,df):
        self.dataframe = df
        return 
    
    def get_datatypes(self):
        dtypes = self.dataframe.dtypes
        return dtypes
    
    def get_uniquevals(self,column):
        unique_vals = self.dataframe[column].unique()
        return unique_vals
    
    def get_median(self,column):
       median = self.dataframe[column].median()
       return median
    
    def get_stdev(self,column):
       stdev = self.dataframe[column].std()
       return stdev
    
    def get_mean(self,column):
       mean = np.mean(self.dataframe[column])
       return mean
    
    def get_mode(self,column):
       mode = self.dataframe[column].mode()
       return mode
    
    def print_shape(self):
        print(self.dataframe.shape)
        return 
    
    def null_percentage(self,column):
        null_pc = ((self.dataframe[column].isnull().sum())/len(self.dataframe))*100
        return null_pc
   
    def get_range(self,column):
        range = self.dataframe[column].max() - self.dataframe[column].min()
        return range

if __name__ == "__main__": # guard added to ensure the game only runs when the script is executed directly 
   filename = 'loan_payments_transformed.csv'
   loan_payments_df = read_csv(filename)  
   my_instance = DataFrameInfo(loan_payments_df)
   dtypes = my_instance.get_datatypes()   
   print(loan_payments_df.head())
   column_names = loan_payments_df.columns.tolist()
   print(type(column_names))
   print(len(column_names))
   print(column_names)


       