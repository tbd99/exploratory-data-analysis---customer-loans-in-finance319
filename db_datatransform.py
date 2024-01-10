import pandas as pd
from datetime import datetime 


def read_csv(filename):
    df_csv = pd.read_csv(filename)
    return df_csv 

def save_to_csv(my_df, filename):
   '''
   This function saves a dataframe to a csv file
   '''
   my_df.to_csv(filename, index=False) # add index=False so index column is not saved to csv 

class DataTransform():
    '''
    This class is used to tranform data types in a pandas DataFrame
    '''
    def __init__(self, df):
        self.dataframe = df
        return 
    
    def obj_to_datetime(self, column_name, datetime_format):
        '''
        This function converts obj/str datatype to datetime
        A dataframe column is specified to be converted from str to datetime, the specific column and datetime format are arguments of the function
        '''
        self.dataframe[column_name] = pd.to_datetime(self.dataframe[column_name], format = datetime_format) 
        return self.dataframe 
    
    def obj_to_int(self, column_name):
        '''
        This function converts obj datatype to float 
        A dataframe column is specified to be converted from obj to float, the text is split to only obtain numerical values, which are then converted to float
        float is chosen over int as it can accomoate NaN/null values in conversion
        '''
        self.dataframe[column_name] = (self.dataframe[column_name].str.extract('(\d+)'))
        self.dataframe[column_name] = pd.to_numeric(self.dataframe[column_name])
        return self.dataframe
    
    def obj_to_str(self, column_name):
        '''
        This function converts obj datatype to string
        Takes the column name as an argument, passed as a string
        '''
        self.dataframe[column_name] = (self.dataframe[column_name]).astype('string')
        return self.dataframe
    
    def obj_to_cat(self, column_name):
        '''
        This function converts obj datatype to categorical
        Takes the column name as an argument, passed as a string
        '''
        self.dataframe[column_name] = (self.dataframe[column_name]).astype('category')
        return self.dataframe

