import pandas as pd
import yaml
from sqlalchemy import create_engine 
from sqlalchemy import inspect


def load_yaml(myfile): 
   '''
   This function loads a yaml file
   It takes a file as an argument and uses the safe_load method to load the yaml file to a dictionary
   '''
   with open(myfile) as f:
      yaml_dict = yaml.safe_load(f)
   return yaml_dict

def save_to_csv(my_df, filename):
   '''
   This function saves a dataframe to a csv file
   '''
   my_df.to_csv(filename)
   
class RDSDatabaseConnector():
    '''
    This class contains the methods used to extract data from the RDS
    '''
    def __init__(self, credentials_dict):
       self.credentials = credentials_dict
    
    def SQLAlchemy_initialiser(self):
       '''
       This function initialises a SQLAlchemy engine
       The provided credentials are used to initialise the engine, which is returned
       '''
       DATABASE_TYPE = 'postgresql'
       HOST = self.credentials['RDS_HOST']
       USER = self.credentials['RDS_USER']
       PASSWORD = self.credentials['RDS_PASSWORD']
       DATABASE = self.credentials['RDS_DATABASE']
       PORT = self.credentials['RDS_PORT']
       engine = create_engine(f"{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}") # creates engine from credentials provided  
       return engine
    
    def extract_to_pandas(self,engine, table_name):
       '''
       This function extracts data from the RDS database, returning a pandas DataFrame
       '''
       df = pd.read_sql_table(table_name, engine)
       return df

credentials_filename = 'credentials.yaml' # data type str
table_name = 'loan_payments'  # data type str
csv_file_name = 'loan_payments.csv' # data type str

if __name__ == "__main__": # guard to ensure the file only runs when the script is executed directly 
   credentials_dict = load_yaml(credentials_filename) 
   my_instance = RDSDatabaseConnector(credentials_dict) # initialises an instance of the RDSDatabaseConnector class 
   my_engine = my_instance.SQLAlchemy_initialiser() # calls the SQLAlchemy_initialiser method to initialise an engine
   conn = my_engine.connect() # intialises connection to RDS database
   loan_payments_df = my_instance.extract_to_pandas(my_engine, table_name) # calls the extract_to_pandas method to load RDS data to pd DataFrame
   save_to_csv(loan_payments_df,csv_file_name) # calls the save_to_csv funciton to save dataframe data to local machine
   conn.close() # closes connection to RDS database


