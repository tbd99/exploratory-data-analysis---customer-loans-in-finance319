import pandas as pd
import yaml
from sqlalchemy import create_engine 


def load_yaml(myfile): 
   with open(myfile) as f:
      yaml_dict = yaml.safe_load(f)
   return yaml_dict

credentials_dict = load_yaml('credentials.yaml')


class RDSDatabaseConnector():
    '''
    This class contains the methods used to extract data from the RDS
    '''
    def __init__(self, credentials_dict):
       self.credentials = credentials_dict
    
    def SQLAlchemy_initialiser(self):
       DATABASE_TYPE = 'postgresql'
       DBAPI = 'psycopg2'
       HOST = self.credentials['RDS_HOST']
       USER = self.credentials['RDS_USER']
       PASSWORD = self.credentials['RDS_PASSWORD']
       DATABASE = self.credentials['RDS_DATABASE']
       PORT = self.credentials['RDS_PORT']
       engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")  
       engine.connect()
       #engine.close()
       return engine
    
    def extract_to_pandas(self,engine):
       df = pd.read_sql_table(self.credentials['RDS_DATABASE'], engine)
       return df
    
my_test = RDSDatabaseConnector(credentials_dict)
my_engine = my_test.SQLAlchemy_initialiser()
loan_payments = my_test.extract_to_pandas(my_engine)