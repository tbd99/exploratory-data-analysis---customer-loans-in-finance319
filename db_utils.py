import pandas as pd
import yaml
from sqlalchemy import create_engine 
from sqlalchemy import inspect


def load_yaml(myfile): 
   with open(myfile) as f:
      yaml_dict = yaml.safe_load(f)
   return yaml_dict

def save_to_csv(my_df,filename):
   my_df.to_csv(filename)
   
class RDSDatabaseConnector():
    '''
    This class contains the methods used to extract data from the RDS
    '''
    def __init__(self, credentials_dict):
       self.credentials = credentials_dict
    
    def SQLAlchemy_initialiser(self):
       DATABASE_TYPE = 'postgresql'
       #DBAPI = 'psycopg2'
       HOST = self.credentials['RDS_HOST']
       USER = self.credentials['RDS_USER']
       PASSWORD = self.credentials['RDS_PASSWORD']
       DATABASE = self.credentials['RDS_DATABASE']
       PORT = self.credentials['RDS_PORT']
       engine = create_engine(f"{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")   
       return engine
    
    def extract_to_pandas(self,engine, table_name):
       df = pd.read_sql_table(table_name, engine)
       return df

credentials_dict = load_yaml('credentials.yaml') 
table_name = 'loan_payments'  
file_name = 'loan_payments_csv'

my_test = RDSDatabaseConnector(credentials_dict)
my_engine = my_test.SQLAlchemy_initialiser()
conn = my_engine.connect() 
loan_payments_df = my_test.extract_to_pandas(my_engine, table_name)
save_to_csv(loan_payments_df,file_name)
conn.close()
loan_payments_df.info()

