
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from db_clean_data import Plotter
from db_clean_data import DataFrameTransform
from db_datatransform import DataTransform
from db_info import DataFrameInfo


loan_payments_df = pd.read_pickle('cleaned_data.pickle') # load in cleaned and transformed data from pickle file
cleaned_data_plotter_instance = Plotter(loan_payments_df)   # initialise an instance of the plotter class with cleaned data
column_names = loan_payments_df.columns.tolist() # create list of column names for analysis

# Summarise currently what percentage of the loans are recovered against the investor funding and the total amount funded
out_prncp_zeros = (loan_payments_df.out_prncp == 0.00).sum()  
loans_recov_against_total_funding = (out_prncp_zeros/(len(loan_payments_df)))*100
print(f"Percentage of the loans recovered against the investor funding and the total amount funded = {loans_recov_against_total_funding.round(2)} %")
loans_recov_against_inv_funding = loans_recov_against_total_funding # out_prncp_inv is same % as columns have 1:1 correlation
funding = ['total_funding','investor_funding']
recovery_pc = [loans_recov_against_total_funding, loans_recov_against_inv_funding]
funding_df = pd.DataFrame({'Funding': funding, 'Recovery_percentage': recovery_pc}) # load data into df to enable plotting
fig1 = plt.figure(1)
plt.bar(funding_df['Funding'], funding_df['Recovery_percentage'], width=0.8) # plot bar chart of % recovery
plt.xticks(rotation=90)

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
fig2 = plt.figure(2)
sns.scatterplot(data=recovery_df, x='Month', y='Recovery_percentage') # scatter plot of data to visualise projection

# Calculate the percentage of charged off loans historically 
charged_off_loans = (loan_payments_df.loan_status == 'Charged Off').sum()  
charged_off_loans_pc = (charged_off_loans/(len(loan_payments_df)))*100
print(f"Percentage of charged off loans historically = {charged_off_loans_pc.round(2)} %")

# and the total amount that was paid towards these loans before being charged off.
charged_off_loans_df = loan_payments_df.loc[loan_payments_df['loan_status']=='Charged Off']
total_loan_amount = charged_off_loans_df['loan_amount'].sum()
total_amount_paid = charged_off_loans_df['total_payment'].sum()
total_amount_paid_pc = (total_amount_paid/total_loan_amount)*100
print(f"total amount that was paid towards these loans before being charged off = £{total_amount_paid.round(2)}")

# Calculate the loss in revenue these loans would have generated for the company if they had finished their term. 
time_passed = ((charged_off_loans_df['last_payment_date'] - charged_off_loans_df['issue_date'])) # calculate how much time has passed of the loan term
time_passed_days = time_passed.dt.days # convert to days 
charged_off_loans_df_calc = charged_off_loans_df.copy()
charged_off_loans_df_calc['time_passed_months'] = (time_passed_days/30.5).round() # convert to int value and divide by avg month length to get no of months
charged_off_loans_df_calc['time_remaining'] = charged_off_loans_df_calc['term'] - charged_off_loans_df_calc['time_passed_months'] # calculate number of months left of the term
charged_off_loans_df_calc['lost_revenue'] = charged_off_loans_df_calc['time_remaining']*charged_off_loans_df_calc['instalment'] # amount that would be paid over the remaining term
total_revenue_loss = charged_off_loans_df_calc['lost_revenue'].sum()
print(f"total loss in revenue these loans would have generated for the company  = £{total_revenue_loss.round(2)}")

# Visualise the loss projected over the remaining term of these loans.
# ?? 

# calculate the percentage of users behind with loan payments 
late_loans_1 = (loan_payments_df.loan_status == 'Late (16-30 days)').sum()   # count no of loans marked as late
late_loans_2 = (loan_payments_df.loan_status == 'Late (31-120 days)').sum()   # count no of loans marked as late
late_loans_pc = ((late_loans_1 + late_loans_2)/(len(loan_payments_df)))*100 # calculate total % of late loans 
print(f"total percentage of users behind with loan payments  = {late_loans_pc.round(2)} %")

# calculate how much loss the company would incur their status was changed to Charged Off
late_loans_df = loan_payments_df.apply(lambda row: row[loan_payments_df['loan_status'].isin(['Late (16-30 days)','Late (31-120 days)'])]) # filter df to obtain only rows with late status 
loss_incurred = late_loans_df['out_prncp'].sum() # sum the outstanding amount for each late loan to calculate loss 
print(f"total loss the company would incur if their status was changed to Charged Off  = £{loss_incurred.round(2)}")

# What is the projected loss of these loans if the customer were to finish the full loans term?
time_passed_lateloans = ((late_loans_df['last_payment_date'] - late_loans_df['issue_date'])) # calculate how much time has passed of the loan term
time_passed_days_lateloans = time_passed_lateloans.dt.days # convert to days 
late_loans_df['time_passed_months'] = (time_passed_days_lateloans/30.5).round() # convert to int value and divide by avg month length to get no of months
late_loans_df['time_remaining'] = late_loans_df['term'] - late_loans_df['time_passed_months'] # calculate number of months left of the term
late_loans_df['outstanding_payments'] = late_loans_df['time_remaining']*late_loans_df['instalment'] # amount that would be paid over the remaining term
projected_loss = late_loans_df['outstanding_payments'].sum() 
print(f"total projected loss of these loans if the customers were to finish the full loans term  = £{projected_loss.round(2)}")

# If customers late on payments converted to Charged Off, what percentage of total expected revenue do these customers and the customers who have already defaulted on their loan represent?
lost_revenue_df = loan_payments_df.apply(lambda row: row[loan_payments_df['loan_status'].isin(['Late (16-30 days)','Late (31-120 days)','Charged Off'])]) # filters customers who have already defaulted on loans as well as those with late payment status 
monthly_revenue_late_customers = lost_revenue_df['instalment'].sum()
total_monthly_revenue = loan_payments_df['instalment'].sum()
total_revenue_pc = (monthly_revenue_late_customers/total_monthly_revenue)*100
print(f"total percentage of total expected revenue from late and stopped payments  = {total_revenue_pc.round(2)} %")

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
#fig3 = plt.figure(3)
#original_df_plotter.plot_countplot('grade') # visualise distribution for all data
#fig4 = plt.figure(4)
#stopped_paying_df_plotter.plot_countplot('grade')  # visualise distribution for customers who are not paying
#fig5 = plt.figure(5)
#late_payments_df_plotter.plot_countplot('grade') # visualise distribution for customers who are late paying

# purpose of loan as indicator - NOT STRONG INDICATOR
#fig6 = plt.figure(6)
#original_df_plotter.plot_countplot('purpose') # visualise distribution for all data
#fig7 = plt.figure(7)
#stopped_paying_df_plotter.plot_countplot('purpose')  # visualise distribution for customers who are not paying
#fig8 = plt.figure(8)
#late_payments_df_plotter.plot_countplot('purpose') # visualise distribution for customers who are late paying

# home owenership as indicator - NOT STRONG INDICATOR
#fig9 = plt.figure(9)
#original_df_plotter.plot_countplot('home_ownership') # visualise distribution for all data
#fig10 = plt.figure(10)
#stopped_paying_df_plotter.plot_countplot('home_ownership')  # visualise distribution for customers who are not paying
#fig11 = plt.figure(11)
#late_payments_df_plotter.plot_countplot('home_ownership') # visualise distribution for customers who are late paying


#out_prncp as indicator 
fig12 = plt.figure(12)
original_df_plotter.plot_KDE('out_prncp') # visualise distribution for all data
fig13 = plt.figure(13)
stopped_paying_df_plotter.plot_KDE('out_prncp')  # visualise distribution for customers who are not paying
fig14 = plt.figure(14)
late_payments_df_plotter.plot_KDE('out_prncp') # visualise distribution for customers who are late paying

original_mean_out_prncp = original_df_info.get_mean('out_prncp') # caluclate mean for all data
stopped_paying_mean_out_prncp = stopped_paying_df_info.get_mean('out_prncp') # calcualte mean for customers who are not paying
late_payment_mean_out_prncp = late_payments_df_info.get_mean('out_prncp') # calcualte mean for customers who are late paying
print(original_mean_out_prncp, stopped_paying_mean_out_prncp, late_payment_mean_out_prncp) 
# higher average out_prncp for those with late payments, suggests this is an indicator for late payments 

# total_rec_late_fee as indicator 
fig15 = plt.figure(15)
original_df_plotter.plot_KDE('total_rec_late_fee') # visualise distribution for all data
fig16 = plt.figure(16)
stopped_paying_df_plotter.plot_KDE('total_rec_late_fee')  # visualise distribution for customers who are not paying
fig17 = plt.figure(17)
late_payments_df_plotter.plot_KDE('total_rec_late_fee') # visualise distribution for customers who are late paying
original_mean_total_rec_late_fee = original_df_info.get_mean('total_rec_late_fee') # caluclate mean for all data
stopped_paying_mean_total_rec_late_fee = stopped_paying_df_info.get_mean('total_rec_late_fee') # calcualte mean for customers who are not paying
late_payment_mean_total_rec_late_fee = late_payments_df_info.get_mean('total_rec_late_fee') # calcualte mean for customers who are late paying
print(original_mean_total_rec_late_fee, stopped_paying_mean_total_rec_late_fee, late_payment_mean_total_rec_late_fee) 
# higher average total late fees for those with late payments or charged off payments, suggests this is an indicator 

# total_rec_int as indicator - NOT STRONG INDICATOR
fig18 = plt.figure(18) 
original_df_plotter.plot_KDE('total_rec_int') # visualise distribution for all data
fig18 = plt.figure(18)
stopped_paying_df_plotter.plot_KDE('total_rec_int') # visualise distribution for customers who are not paying
fig18 = plt.figure(18)
late_payments_df_plotter.plot_KDE('total_rec_int') # visualise distribution for customers who are late paying
original_mean_total_rec_int = original_df_info.get_mean('total_rec_int') # caluclate mean for all data
stopped_paying_mean_total_rec_int = stopped_paying_df_info.get_mean('total_rec_int') # calcualte mean for customers who are not paying
late_payment_mean_total_rec_int= late_payments_df_info.get_mean('total_rec_int') # calcualte mean for customers who are late paying
print(original_mean_total_rec_int, stopped_paying_mean_total_rec_int, late_payment_mean_total_rec_int) 
# minimal difference in averages suggests total_rec_int not an indicator 

#last_payment_amount as indicator 
fig19 = plt.figure(19)
original_df_plotter.plot_KDE('last_payment_amount') # visualise distribution for all data
fig20 = plt.figure(20)
stopped_paying_df_plotter.plot_KDE('last_payment_amount') # visualise distribution for customers who are not paying
fig21 = plt.figure(21)
late_payments_df_plotter.plot_KDE('last_payment_amount') # visualise distribution for customers who are late paying
original_mean_last_payment_amount = original_df_info.get_mean('last_payment_amount') # caluclate mean for all data
stopped_paying_mean_last_payment_amount = stopped_paying_df_info.get_mean('last_payment_amount') # calcualte mean for customers who are not paying
late_payment_mean_last_payment_amount= late_payments_df_info.get_mean('last_payment_amount') # calcualte mean for customers who are late paying
print(original_mean_last_payment_amount, stopped_paying_mean_last_payment_amount, late_payment_mean_last_payment_amount)
# Last payments amount is lower for late payments and charged off payments, suggests lower last payment amount is an indicator of not paying back/paying late

plt.show() 
