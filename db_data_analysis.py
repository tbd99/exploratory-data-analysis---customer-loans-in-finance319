
import pandas as pd
import pickle 
from db_clean_data import Plotter

loan_payments_df = pd.read_pickle('cleaned_data.pickle')

print('woooo')


loan_payments_df.info()

cleaned_data_plotter_instance = Plotter(loan_payments_df)   
cleaned_data_plotter_instance.plot_corr_matrix()