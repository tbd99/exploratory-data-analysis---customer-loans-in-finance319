import numpy as np
import pandas as pd
from datetime import datetime 

def read_csv(filename):
    df_csv = pd.read_csv(filename)
    return df_csv 

filename = 'loan_payments_transformed.csv'
loan_payments_df = read_csv(filename)

#loan_payments_df.info()
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
    
    def print_shape(self):
        print(self.dataframe.shape)
        return 
    
    #function to calcualte mode of column
    #function to print dataframe shape 
    #function to generate a count/percentage count of null values of a column
    #function to count frequency of each option in categorical data 

    

my_instance = DataFrameInfo(loan_payments_df)
dtypes = my_instance.get_datatypes()   
u_vals = my_instance.get_uniquevals('home_ownership')
print(u_vals)
mode = my_instance.get_median('total_payment')
print(mode)

sd = my_instance.get_stdev('total_payment')
print(sd)

mean = my_instance.get_mean('total_payment')
print(mean)

my_instance.print_shape()





       