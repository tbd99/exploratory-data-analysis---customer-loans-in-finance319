import pandas as pd
from datetime import datetime 






def read_csv(filename):
    df_csv = pd.read_csv(filename)
    return df_csv 

filename = 'loan_payments.csv'
loan_payments_df = read_csv(filename)
#loan_payments_df['term'] = pd.to_datetime(loan_payments_df['term'], format = '%m/%Y') 

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
column_name = 'issue_date' # data type str 
datetime_format = '%b-%Y' # data type str 
my_test.obj_to_datetime(column_name,datetime_format)
loan_payments_df.info()
print(loan_payments_df.iloc[0])



      # need column name as arg and df ? 
        #return 
        # need column name as arg and df ? 

   # def obj_to_int(self):
    #    return 
    
