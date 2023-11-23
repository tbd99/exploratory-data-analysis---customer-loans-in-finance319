
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
        return self.dataframe.dtypes()

       