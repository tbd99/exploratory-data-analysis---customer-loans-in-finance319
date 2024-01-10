import numpy as np
import pandas as pd
from datetime import datetime 
from scipy.stats import normaltest 

def read_csv(filename):
    df_csv = pd.read_csv(filename)
    return df_csv 

class DataFrameInfo():
    '''
    This class contains functions that get information from the DataFrame
    Attributes:
    df (pd DataFrame): The dataframe to be evaluated 
    '''
    def __init__(self, df):
        self.dataframe = df
        return 
    
    def get_datatypes(self):
        '''
        This function returns the datatype of each column in the dataframe
        '''
        dtypes = self.dataframe.dtypes
        return dtypes
    
    def get_uniquevals(self, column):
        '''
        This function returns the unique values of a column in the dataframe
        '''
        unique_vals = self.dataframe[column].unique()
        return unique_vals
    
    def get_median(self, column):
       '''
       This function returns the median value of a column in the dataframe
       '''
       median = self.dataframe[column].median()
       return median
    
    def get_stdev(self, column):
       '''
       This function returns the standard deviation of a column in the dataframe
       '''
       stdev = self.dataframe[column].std()
       return stdev
    
    def get_mean(self, column):
       '''
       This function returns the mean of a column in the dataframe
       '''
       mean = np.mean(self.dataframe[column])
       return mean
    
    def get_mode(self, column):
       '''
       This function returns the mode of a column in the dataframe
       '''
       mode = self.dataframe[column].mode()
       return mode
    
    def print_shape(self):
        '''
        This function prints the shape of the dataframe 
        '''
        print(self.dataframe.shape)
        return 
    
    def null_percentage(self, column):
        '''
        This function returns the percentage of null values in a column in the dataframe 
        '''
        null_pc = ((self.dataframe[column].isnull().sum())/len(self.dataframe))*100
        return null_pc
   
    def get_range(self, column):
        '''
        This function returns the percentage of null values in a column in the dataframe 
        '''
        range = self.dataframe[column].max() - self.dataframe[column].min()
        return range
    
    def get_normal_dist(self, column):
        '''
        This function returns the p value of the data, giving the normal distribution
        '''
        stat, p = normaltest(self.dataframe[column], nan_policy='omit')
        print('Statistics=%.3f, p=%.3f' % (stat, p))
        return stat, p
    



       