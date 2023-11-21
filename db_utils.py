import yaml
with open('do_not_track/credentials.yaml') as f:
    animals = yaml.safe_load(f)

print(animals)
class RDSDatabaseConnector():
    '''
    This class contains the methods used to extract data from the RDS
    '''