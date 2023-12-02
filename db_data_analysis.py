
import pandas as pd
import pickle 
import seaborn as sns
from db_clean_data import Plotter
from db_clean_data import DataFrameTransform
from db_datatransform import DataTransform
from db_info import DataFrameInfo

loan_payments_df = pd.read_pickle('cleaned_data.pickle')
# double check data is correct 
loan_payments_df.info()
cleaned_data_plotter_instance = Plotter(loan_payments_df)   
cleaned_data_plotter_instance.plot_corr_matrix()
column_names = loan_payments_df.columns.tolist() 
#for i in range(0, len(column_names)):
    #cleaned_data_plotter_instance.plot_KDE(column_names[i])

# Summarise currently what percentage of the loans are recovered against the investor funding and the total amount funded
out_prncp_zeros = (loan_payments_df.out_prncp == 0.00).sum()  
loans_recov_against_total_funding = (out_prncp_zeros/(len(loan_payments_df)))*100
print(f"{loans_recov_against_total_funding.round(2)} %")

# out_prncp_inv is same % as columns have 1:1 correlation?
loans_recov_against_inv_funding = loans_recov_against_total_funding 