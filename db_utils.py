import yaml


def load_yaml(myfile): 
   with open(myfile) as f:
      yaml_dict = yaml.safe_load(f)
   return yaml_dict

credentials_dict = load_yaml('credentials.yaml')


class RDSDatabaseConnector():
    '''
    This class contains the methods used to extract data from the RDS
    '''