import pandas as pd

def read_csv(filename):
    df_csv = pd.read_csv(filename)
    return df_csv 

filename = 'loan_payments.csv'
loan_payments_df = read_csv(filename)