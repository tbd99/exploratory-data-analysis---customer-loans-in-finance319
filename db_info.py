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

mode = my_instance.get_mode('purpose')
print(mode)


nulls = my_instance.null_percentage('mths_since_last_record')
print(nulls)

range = my_instance.get_range('total_payment')
print(range)




       