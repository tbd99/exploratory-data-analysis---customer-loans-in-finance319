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
    
    def obj_to_datetime(self,column_name,datetime_format):
        self.dataframe[column_name] = pd.to_datetime(self.dataframe[column_name], format = datetime_format) 
        #self.dataframe[column_name] = self.dataframe[column_name].floor('M').astype(datetime)
        return self.dataframe 

my_test = DataTransform(loan_payments_df) #initialise instance of class
col_to_convert_to_datetime = ['issue_date', 'earliest_credit_line', 'last_payment_date','next_payment_date', 'last_credit_pull_date']

for i in range(0,len(col_to_convert_to_datetime)):
    datetime_format = '%b-%Y'
    my_test.obj_to_datetime(col_to_convert_to_datetime[i],datetime_format)

loan_payments_df.info()
print(loan_payments_df.iloc[0])
