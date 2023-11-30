import pandas as pd

def read_csv(filename):
    df_csv = pd.read_csv(filename)
    return df_csv 

filename = 'loan_payments.csv'
loan_payments_df = read_csv(filename)
#print(loan_payments_df.head())


loan_payments_df.info()
#print(loan_payments_df.iloc[0])
#print(loan_payments_df.iloc[1])
#print(loan_payments_df.iloc[2])
#print(loan_payments_df.iloc[3000])
##print(loan_payments_df.iloc[35])
print(loan_payments_df.iloc[92]) 

#print(loan_payments_df['verification_status'].unique())
##print(loan_payments_df['home_ownership'].unique())
#print(loan_payments_df['loan_status'].unique())
#p#rint(loan_payments_df['purpose'].unique())
#print(loan_payments_df['payment_plan'].unique())
#print(loan_payments_df['application_type'].unique())

print(loan_payments_df.iloc[:,11]) 
print(loan_payments_df.iloc[:,6]) 

column_names = loan_payments_df.columns.tolist()
print(type(column_names))
print(len(column_names))
print(column_names)