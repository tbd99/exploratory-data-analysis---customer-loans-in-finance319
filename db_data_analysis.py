
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
#loan_payments_df.info()
cleaned_data_plotter_instance = Plotter(loan_payments_df)   
#cleaned_data_plotter_instance.plot_corr_matrix()
column_names = loan_payments_df.columns.tolist() 

# Summarise currently what percentage of the loans are recovered against the investor funding and the total amount funded
out_prncp_zeros = (loan_payments_df.out_prncp == 0.00).sum()  
loans_recov_against_total_funding = (out_prncp_zeros/(len(loan_payments_df)))*100
#print(f"{loans_recov_against_total_funding.round(2)} %")
loans_recov_against_inv_funding = loans_recov_against_total_funding # out_prncp_inv is same % as columns have 1:1 correlation
funding = ['total_funding','investor_funding']
recovery_pc = [loans_recov_against_total_funding, loans_recov_against_inv_funding]
funding_df = pd.DataFrame({'Funding': funding, 'Recovery_percentage': recovery_pc})
#plt.bar(funding_df['Funding'], funding_df['Recovery_percentage'], width=0.8)
#plt.xticks(rotation=90)
#plt.show() 

# visualise what percentage of the total amount would be recovered up to 6 months' in the future.
loan_payments_recovery_projection_df = loan_payments_df.copy()
loan_payments_recovery_projection_df['remaining_balance'] = loan_payments_recovery_projection_df['loan_amount'] -  loan_payments_recovery_projection_df['total_payment'] # calculate remaining balance of each loan
loan_payments_recovery_projection_df['month1'] = loan_payments_recovery_projection_df['remaining_balance'] - loan_payments_recovery_projection_df['instalment'] # minus monthly payment to get remaining balance for that month
loan_payments_recovery_projection_df['month2'] = loan_payments_recovery_projection_df['remaining_balance'] - (loan_payments_recovery_projection_df['instalment']*2) 
loan_payments_recovery_projection_df['month3'] = loan_payments_recovery_projection_df['remaining_balance'] - (loan_payments_recovery_projection_df['instalment']*3)
loan_payments_recovery_projection_df['month4'] = loan_payments_recovery_projection_df['remaining_balance'] - (loan_payments_recovery_projection_df['instalment']*4)
loan_payments_recovery_projection_df['month5'] = loan_payments_recovery_projection_df['remaining_balance'] - (loan_payments_recovery_projection_df['instalment']*5)
loan_payments_recovery_projection_df['month6'] = loan_payments_recovery_projection_df['remaining_balance'] - (loan_payments_recovery_projection_df['instalment']*6)

month1_pc = (((loan_payments_recovery_projection_df.month1 <= 0.00).sum())/(len(loan_payments_df)))*100 # calculate percentage of loans recovered after each month
month2_pc = (((loan_payments_recovery_projection_df.month2 <= 0.00).sum())/(len(loan_payments_df)))*100
month3_pc = (((loan_payments_recovery_projection_df.month3 <= 0.00).sum())/(len(loan_payments_df)))*100
month4_pc = (((loan_payments_recovery_projection_df.month4 <= 0.00).sum())/(len(loan_payments_df)))*100
month5_pc = (((loan_payments_recovery_projection_df.month5 <= 0.00).sum())/(len(loan_payments_df)))*100
month6_pc = (((loan_payments_recovery_projection_df.month6 <= 0.00).sum())/(len(loan_payments_df)))*100

month_no = [1,2,3,4,5,6]
loans_recovered_pc = [month1_pc, month2_pc, month3_pc, month4_pc, month5_pc, month6_pc]
recovery_df = pd.DataFrame({'Month': month_no,'Recovery_percentage': loans_recovered_pc}) # create df to plot data 
#sns.scatterplot(data=recovery_df, x='Month', y='Recovery_percentage') # scatter plot of data to visualise projection
#plt.show()


# Calculate the percentage of charged off loans historically 
charged_off_loans = (loan_payments_df.loan_status == 'Charged Off').sum()  
charged_off_loans_pc = (charged_off_loans/(len(loan_payments_df)))*100
#print(f"{charged_off_loans_pc.round(2)} %")

# and the total amount that was paid towards these loans before being charged off.
charged_off_loans_df = loan_payments_df.loc[loan_payments_df['loan_status']=='Charged Off']
total_loan_amount = charged_off_loans_df['loan_amount'].sum()
total_amount_paid = charged_off_loans_df['total_payment'].sum()
total_amount_paid_pc = (total_amount_paid/total_loan_amount)*100
#print(f"{total_amount_paid_pc.round(2)} %")

# Calculate the loss in revenue these loans would have generated for the company if they had finished their term. 

time_passed = ((charged_off_loans_df['last_payment_date'] - charged_off_loans_df['issue_date'])) # calculate how much time has passed of the loan term
time_passed_days = time_passed.dt.days # convert to days 
charged_off_loans_df_calc = charged_off_loans_df.copy()
charged_off_loans_df_calc['time_passed_months'] = (time_passed_days/30.5).round() # convert to int value and divide by avg month length to get no of months
charged_off_loans_df_calc['time_remaining'] = charged_off_loans_df_calc['term'] - charged_off_loans_df_calc['time_passed_months'] # calculate number of months left of the term
charged_off_loans_df_calc['lost_revenue'] = charged_off_loans_df_calc['time_remaining']*charged_off_loans_df_calc['instalment'] # amount that would be paid over the remaining term
#print(charged_off_loans_df_calc['time_remaining'].head(10))
#print(total_loan_amount)

# Visualise the loss projected over the remaining term of these loans.
# ?? 

# print(loan_payments_df['loan_status'].head(10))
# calculate the percentage of users behind with loan payments 
late_loans_1 = (loan_payments_df.loan_status == 'Late (16-30 days)').sum()   # count no of loans marked as late
late_loans_2 = (loan_payments_df.loan_status == 'Late (31-120 days)').sum()   # count no of loans marked as late
late_loans_pc = ((late_loans_1 + late_loans_2)/(len(loan_payments_df)))*100 # calculate total % of late loans 
#print(late_loans_1,late_loans_2,late_loans_pc)

# calculate how much loss the company would incur their status was changed to Charged Off

late_loans_df = loan_payments_df.apply(lambda row: row[loan_payments_df['loan_status'].isin(['Late (16-30 days)','Late (31-120 days)'])]) # filter df to obtain only rows with late status 
loss_incurred = late_loans_df['out_prncp'].sum() # sum the outstanding amount for each late loan to calculate loss 
#print(loss_incurred)

# What is the projected loss of these loans if the customer were to finish the full loans term?
time_passed_lateloans = ((late_loans_df['last_payment_date'] - late_loans_df['issue_date'])) # calculate how much time has passed of the loan term
time_passed_days_lateloans = time_passed_lateloans.dt.days # convert to days 
late_loans_df['time_passed_months'] = (time_passed_days_lateloans/30.5).round() # convert to int value and divide by avg month length to get no of months
late_loans_df['time_remaining'] = late_loans_df['term'] - late_loans_df['time_passed_months'] # calculate number of months left of the term
late_loans_df['outstanding_payments'] = late_loans_df['time_remaining']*late_loans_df['instalment'] # amount that would be paid over the remaining term
projected_loss = late_loans_df['outstanding_payments'].sum() # 
print(projected_loss)

# If customers late on payments converted to Charged Off
# what percentage of total expected revenue do these customers and the customers who have already defaulted on their loan represent?
lost_revenue_df = loan_payments_df.apply(lambda row: row[loan_payments_df['loan_status'].isin(['Late (16-30 days)','Late (31-120 days)','Charged Off'])]) # filters customers who have already defaulted on loans as well as those with late payment status 
monthly_revenue_late_customers = lost_revenue_df['instalment'].sum()
#print(monthly_revenue_late_customers)
total_monthly_revenue = loan_payments_df['instalment'].sum()
#print(total_monthly_revenue)
total_revenue_pc = (monthly_revenue_late_customers/total_monthly_revenue)*100
#print(total_revenue_pc.round(2))

# visualise the possible indicators that a customer will not be able to pay the loan.

loan_payments_df_stopped_paying = loan_payments_df.loc[loan_payments_df['loan_status']=='Charged Off'] # subset containing only customers who have stopped paying
loan_payments_df_late_payments = loan_payments_df.apply(lambda row: row[loan_payments_df['loan_status'].isin(['Late (16-30 days)','Late (31-120 days)'])]) # subset containings customers with late payments

# initialise instances of plotter class for each df
original_df_plotter = Plotter(loan_payments_df)
stopped_paying_df_plotter = Plotter(loan_payments_df_stopped_paying)
late_payments_df_plotter = Plotter(loan_payments_df_late_payments)

# intiailise instances of dataframeinfo class for each df

original_df_info = DataFrameInfo(loan_payments_df)
stopped_paying_df_info = DataFrameInfo(loan_payments_df_stopped_paying)
late_payments_df_info = DataFrameInfo(loan_payments_df_late_payments)

# visualise data for different columns for entire dataset, customers who hae stopped paying, customers late on payment to identify indicators

# grade of the loan as an indicator - NOT STRONG INDICATOR
#fig1 = plt.figure(1)
#original_df_plotter.plot_countplot('grade') # visualise distribution for all data
#fig2 = plt.figure(2)
#stopped_paying_df_plotter.plot_countplot('grade')  # visualise distribution for customers who are not paying
#fig3 = plt.figure(3)
#late_payments_df_plotter.plot_countplot('grade') # visualise distribution for customers who are late paying

# purpose of loan as indicator - NOT STRONG INDICATOR
#fig4 = plt.figure(4)
#original_df_plotter.plot_countplot('purpose') # visualise distribution for all data
#fig5 = plt.figure(5)
#stopped_paying_df_plotter.plot_countplot('purpose')  # visualise distribution for customers who are not paying
#fig6 = plt.figure(6)
#late_payments_df_plotter.plot_countplot('purpose') # visualise distribution for customers who are late paying

# home owenership as indicator - NOT STRONG INDICATOR
#fig7 = plt.figure(7)
#original_df_plotter.plot_countplot('home_ownership') # visualise distribution for all data
#fig8 = plt.figure(8)
#stopped_paying_df_plotter.plot_countplot('home_ownership')  # visualise distribution for customers who are not paying
#fig9 = plt.figure(9)
#late_payments_df_plotter.plot_countplot('home_ownership') # visualise distribution for customers who are late paying


#out_prncp as indicator 
fig19 = plt.figure(19)
original_df_plotter.plot_KDE('out_prncp') # visualise distribution for all data
fig20 = plt.figure(20)
stopped_paying_df_plotter.plot_KDE('out_prncp')  # visualise distribution for customers who are not paying
fig21 = plt.figure(21)
late_payments_df_plotter.plot_KDE('out_prncp') # visualise distribution for customers who are late paying

original_mean_out_prncp = original_df_info.get_mean('out_prncp') # caluclate mean for all data
stopped_paying_mean_out_prncp = stopped_paying_df_info.get_mean('out_prncp') # calcualte mean for customers who are not paying
late_payment_mean_out_prncp = late_payments_df_info.get_mean('out_prncp') # calcualte mean for customers who are late paying
print(original_mean_out_prncp, stopped_paying_mean_out_prncp, late_payment_mean_out_prncp) 
# higher average out_prncp for those with late payments, suggests this is an indicator for late payments 

# total_rec_late_fee as indicator 
fig22 = plt.figure(22)
original_df_plotter.plot_KDE('total_rec_late_fee') # visualise distribution for all data
fig23 = plt.figure(23)
stopped_paying_df_plotter.plot_KDE('total_rec_late_fee')  # visualise distribution for customers who are not paying
fig24 = plt.figure(24)
late_payments_df_plotter.plot_KDE('total_rec_late_fee') # visualise distribution for customers who are late paying
original_mean_total_rec_late_fee = original_df_info.get_mean('total_rec_late_fee') # caluclate mean for all data
stopped_paying_mean_total_rec_late_fee = stopped_paying_df_info.get_mean('total_rec_late_fee') # calcualte mean for customers who are not paying
late_payment_mean_total_rec_late_fee = late_payments_df_info.get_mean('total_rec_late_fee') # calcualte mean for customers who are late paying
print(original_mean_total_rec_late_fee, stopped_paying_mean_total_rec_late_fee, late_payment_mean_total_rec_late_fee) 
# higher average total late fees for those with late payments or charged off payments, suggests this is an indicator of late payment

# total_rec_int as indicator - NOT strong indicator
fig25 = plt.figure(25) 
original_df_plotter.plot_KDE('total_rec_int') # visualise distribution for all data
fig26 = plt.figure(26)
stopped_paying_df_plotter.plot_KDE('total_rec_int') # visualise distribution for customers who are not paying
fig27 = plt.figure(27)
late_payments_df_plotter.plot_KDE('total_rec_int') # visualise distribution for customers who are late paying
original_mean_total_rec_int = original_df_info.get_mean('total_rec_int') # caluclate mean for all data
stopped_paying_mean_total_rec_int = stopped_paying_df_info.get_mean('total_rec_int') # calcualte mean for customers who are not paying
late_payment_mean_total_rec_int= late_payments_df_info.get_mean('total_rec_int') # calcualte mean for customers who are late paying
print(original_mean_total_rec_int, stopped_paying_mean_total_rec_int, late_payment_mean_total_rec_int) 
# minimal difference in averages suggests total_rec_int not an indicator 

#last_payment_amount as indicator 
fig125 = plt.figure(125)
original_df_plotter.plot_KDE('last_payment_amount') # visualise distribution for all data
fig126 = plt.figure(126)
stopped_paying_df_plotter.plot_KDE('last_payment_amount') # visualise distribution for customers who are not paying
fig127 = plt.figure(127)
late_payments_df_plotter.plot_KDE('last_payment_amount') # visualise distribution for customers who are late paying

original_mean_last_payment_amount = original_df_info.get_mean('last_payment_amount') # caluclate mean for all data
stopped_paying_mean_last_payment_amount = stopped_paying_df_info.get_mean('last_payment_amount') # calcualte mean for customers who are not paying
late_payment_mean_last_payment_amount= late_payments_df_info.get_mean('last_payment_amount') # calcualte mean for customers who are late paying
print(original_mean_last_payment_amount, stopped_paying_mean_last_payment_amount, late_payment_mean_last_payment_amount)



plt.show() 