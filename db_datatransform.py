import pandas as pd
from datetime import datetime 

def read_csv(filename):
    df_csv = pd.read_csv(filename)
    return df_csv 

filename = 'loan_payments.csv'
loan_payments_df = read_csv(filename)

class DataTransform():
    '''
    This class is used to tranform data types in a pandas DataFrame
    '''
    def __init__(self,df):
        self.dataframe = df
        return 
    '''
    This function converts obj/str datatype to datetime 
    A dataframe column is specified to be converted from str to datetime, the specific column and datetime format are arguments of the function
    '''
    def obj_to_datetime(self,column_name,datetime_format):
        self.dataframe[column_name] = pd.to_datetime(self.dataframe[column_name], format = datetime_format) 
        #self.dataframe[column_name] = self.dataframe[column_name].floor('M').astype(datetime)
        return self.dataframe 
    
    def obj_to_int(self,column_name):
        #self.dataframe[column_name] = self.dataframe[column_name].astype(int)
        self.dataframe[column_name] = (self.dataframe[column_name].str.extract('(\d+)'))
        self.dataframe[column_name] = pd.to_numeric(self.dataframe[column_name])
#
        #self.dataframe[column_name] = (self.dataframe[column_name].astype('int64', errors='ignore'))
        return self.dataframe


my_instance = DataTransform(loan_payments_df) #initialise instance of class

col_to_convert_to_datetime = ['issue_date', 'earliest_credit_line', 'last_payment_date','next_payment_date', 'last_credit_pull_date'] # list of strings specifying columns to be converted
col_to_convert_to_int = ['term','employment_length']

for i in range(0,len(col_to_convert_to_datetime)): #loops over list of column names
    datetime_format = '%b-%Y'
    my_instance.obj_to_datetime(col_to_convert_to_datetime[i],datetime_format) #calls the obj_to_datetime method of the DataTransform class to convert data

for i in range(0,len(col_to_convert_to_int)): #loops over list of column names
    my_instance.obj_to_int(col_to_convert_to_int[i])


loan_payments_df.info()
print(loan_payments_df.iloc[26])