
import pandas as pd
import pickle 
import seaborn as sns
import matplotlib.pyplot as plt
from db_clean_data import Plotter
from db_clean_data import DataFrameTransform
from db_datatransform import DataTransform
from db_info import DataFrameInfo

loan_payments_df = pd.read_pickle('cleaned_data.pickle')
# double check data is correct 
loan_payments_df.info()
cleaned_data_plotter_instance = Plotter(loan_payments_df)   
#cleaned_data_plotter_instance.plot_corr_matrix()
column_names = loan_payments_df.columns.tolist() 
#for i in range(0, len(column_names)):
    #cleaned_data_plotter_instance.plot_KDE(column_names[i])

# Summarise currently what percentage of the loans are recovered against the investor funding and the total amount funded
out_prncp_zeros = (loan_payments_df.out_prncp == 0.00).sum()  
loans_recov_against_total_funding = (out_prncp_zeros/(len(loan_payments_df)))*100
print(f"{loans_recov_against_total_funding.round(2)} %")
loans_recov_against_inv_funding = loans_recov_against_total_funding # out_prncp_inv is same % as columns have 1:1 correlation
funding = ['total_funding','investor_funding']
recovery_pc = [loans_recov_against_total_funding, loans_recov_against_inv_funding]
funding_df = pd.DataFrame({'Funding': funding, 'Recovery_percentage': recovery_pc})
#plt.bar(funding_df['Funding'], funding_df['Recovery_percentage'], width=0.8)
#plt.xticks(rotation=90)
#plt.show() 

# Calculate the percentage of charged off loans historically 
charged_off_loans = (loan_payments_df.loan_status == 'Charged Off').sum()  
charged_off_loans_pc = (charged_off_loans/(len(loan_payments_df)))*100
print(f"{charged_off_loans_pc.round(2)} %")

# and the total amount that was paid towards these loans before being charged off.
charged_off_loans_df = loan_payments_df.loc[loan_payments_df['loan_status']=='Charged Off']
total_loan_amount = charged_off_loans_df['loan_amount'].sum()
total_amount_paid = charged_off_loans_df['total_payment'].sum()
total_amount_paid_pc = (total_amount_paid/total_loan_amount)*100
print(f"{total_amount_paid_pc.round(2)} %")

# Calculate the loss in revenue these loans would have generated for the company if they had finished their term. 
# amount paid each month, calc how many months of payments left, and how much each month 
time_passed = ((charged_off_loans_df['last_payment_date'] - charged_off_loans_df['issue_date']))
time_passed_days = time_passed.dt.days 
charged_off_loans_df_calc = charged_off_loans_df.copy()
charged_off_loans_df_calc['time_passed_months'] = (time_passed_days/30.5).round() # convert to int value and divide by avg month length to get no of months
charged_off_loans_df_calc['time_remaining'] = charged_off_loans_df_calc['term'] - charged_off_loans_df_calc['time_passed_months']
charged_off_loans_df_calc['lost_revenue'] = charged_off_loans_df_calc['time_remaining']*charged_off_loans_df_calc['instalment']
#print(charged_off_loans_df_calc['time_remaining'].head(10))
total_lost_revenue = charged_off_loans_df_calc['lost_revenue'].sum()
print(total_loan_amount)

# Visualise the loss projected over the remaining term of these loans.
# scatter plot of amount paid per month across months 

# print(loan_payments_df['loan_status'].head(10))
# calculate the percentage of users behind with loan payments 
late_loans_1 = (loan_payments_df.loan_status == 'Late (16-30 days)').sum()   # count no of loans marked as late
late_loans_2 = (loan_payments_df.loan_status == 'Late (31-120 days)').sum()   # count no of loans marked as late
late_loans_pc = ((late_loans_1 + late_loans_2)/(len(loan_payments_df)))*100 # calculate total % of late loans 
print(late_loans_1,late_loans_2,late_loans_pc)

# calculate amount owed here 