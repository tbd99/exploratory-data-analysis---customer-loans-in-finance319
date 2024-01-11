# exploratory-data-analysis---customer-loans-in-finance319
Perform exploratory data analysis on the loan portfolio, using various statistical and data visualisation techniques to uncover patterns, relationships, and anomalies in the loan data.

## Project description
The aim of this project is to gain a comprehensive understanding of the loan portfolio data of a large financial instiution by performing exploratory data analysis (EDA) using various statistical and data visualistion methods, demonstrating a strong understanding and knowledge of these techniques. This will enable patterns, relationships and anomalies in the data to be revealed, thereby facilitating the improvement of the the performance and profitability of the loan portfolio. 

This project will be a practical application and demonstration of the various data analysis skills developed in the AiCore data analysis course.

## Table of contents 
1. [Project Execution](#project-execution)
   - [Extracting loans data from the cloud](#extracting-loans-data-from-the-cloud)
      - [Creating the RDSDatabaseConnector class](#creating-the-rdsdatabaseconnector-class-and-functions)
      - [Loading the data](#loading-the-data)
   - [Exploratory data analysis (EDA) and data cleaning ](#exploratory-data-analysis-eda-and-data-cleaning)
      - [Creating the DataFrameInfo class and functions](#creating-the-dataframeinfo-class-and-functions)
      - [Creating the DataTransform class and functions](#creating-the-datatransform-class-and-functions)
      - [Creating the Plotter class and functions](#creating-the-plotter-class-and-functions)
      - [Creating the DataFrameTransform class and functions](#creating-the-dataframetransform-class-and-functions)
      - [Converting columns to the correct format](#converting-columns-to-the-correct-format)
      - [Handling null values](#handling-null-values)
      - [Identification of skewed columns](#identification-of-skewed-columns)
      - [Handling of outliers](#handling-of-outliers)
      - [Identification of overly correlated columns](#identification-of-overly-correlated-columns)
      - [Saving the cleaned data](#saving-the-cleaned-data)
   - [Data analysis and visualisation](#data-analysis-and-visualisation)
2. [Installation Instructions](#installation-instructions)
3. [Usage Instructions](#usage-instructions)
4. [File Structure](#file-structure)
5. [License Information](#license-information)

# Project execution 
## Extracting loans data from the cloud
- The loan payment data to be analysed is stored in an AWS RDS database in the cloud
- Python classes are created in order to extract this data from the database and save it locally as a pandas DataFrame, enabling analysis

### Creating the RDSDatabaseConnector class and functions
- The functions load_yaml and save_to_csv are created for data loading and saving
- The RDSDatabaseConnector class is created to extract the loans data from an AWS RDS database
- The SQLAlchemy_initialiser function is created within the class, this function intiialises a SQLAlchemy engine using the provided credentials and returns the engine
- The extract_to_pandas function is created within the class, this function reads data from the RDS database and returns it as a pandas DataFrame
    ~~~
    class RDSDatabaseConnector():

    def __init__(self, credentials_dict):
       self.credentials = credentials_dict
    
    def SQLAlchemy_initialiser(self):
      
       DATABASE_TYPE = 'postgresql'
       HOST = self.credentials['RDS_HOST']
       USER = self.credentials['RDS_USER']
       PASSWORD = self.credentials['RDS_PASSWORD']
       DATABASE = self.credentials['RDS_DATABASE']
       PORT = self.credentials['RDS_PORT']
       engine = create_engine(f"{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}") # creates engine from credentials provided  
       return engine
    
    def extract_to_pandas(self,engine, table_name):
      
       df = pd.read_sql_table(table_name, engine)
       return df
    ~~~   

### Loading the data 
- Credentials are loaded from a yaml file with the defined load_yaml function, database credentials are added to the .gitignore file in order to maintain security
- An instance of the RDSDatabaseConnector class is intiailised and the SQLAlchemy_initialiser method is called to initialise an engine
- A connection is initilised to the RDS database and the RDS data is loaded to a pandas DataFrame using the extract_to_pandas function
- The resulting dataframe is saved to a .csv file using the save_to_csv function and the connection to the RDS database is closed
~~~
if __name__ == "__main__": # guard 
   credentials_dict = load_yaml(credentials_filename)
   my_instance = RDSDatabaseConnector(credentials_dict) # initialises an instance of the RDSDatabaseConnector class 
   my_engine = my_instance.SQLAlchemy_initialiser() # calls the SQLAlchemy_initialiser method to initialise an engine
   conn = my_engine.connect() # intialises connection to RDS database
   loan_payments_df = my_instance.extract_to_pandas(my_engine, table_name) # load RDS data to pd DataFrame
   save_to_csv(loan_payments_df,csv_file_name) # save dataframe data to local machine
   conn.close() # closes connection to RDS database
~~~

## Exploratory data analysis (EDA) and data cleaning 
- Several classes are created to facilitate EDA and data visualisation, including handling nulls, outliers, skewed data, correlated columns and incorrect data types
- Data is cleaned and transformed to prepare for final analysis and visualisation for presentation of results

### Creating the DataFrameInfo class and functions
- The DataFrameInfo class is created containing functions get information and descriptive statistics from the pandas DataFrame being analysed
- These functions are used to gain insight into the data when performing EDA and enables the identification of outliers, nulls, incorrect data types etc.
- The following functions are created within this class, with some example code shown below:
- get_datatypes: returns the datatype of each column in the dataframe using df.dtypes 
- get_uniquevals: returns the unique values a specified column in the dataframe using the .unique() method
- get_median: returns the median value of a specified column in the dataframe using the .median() method
- get_stdev: returns the standard deviation value of a specified column in the dataframe using the .std() method
- get_mean: returns the mean value of a specified column in the dataframe using np.mean
- get_mode: returns the mode value of a specified column in the dataframe using the .mode() method
- print_shape: prints the shape of the dataframe using df.shape
- null_percentage: returns the percentage of null values in a specified column in the dataframe using the .isnull() method
~~~
def null_percentage(self, column):

    null_pc = ((self.dataframe[column].isnull().sum())/len(self.dataframe))*100
    return null_pc
~~~
- get_range: returns the range of values in a specified column in the dataframe using .min() and .max() methods
~~~
def get_range(self, column):

    range = self.dataframe[column].max() - self.dataframe[column].min()
    return range
~~~
- get_normal_dist: returns the p value of the data in a specified column, giving the normal distribution using normaltest
~~~
def get_normal_dist(self, column):
        
    stat, p = normaltest(self.dataframe[column], nan_policy='omit')
    print('Statistics=%.3f, p=%.3f' % (stat, p))
    return stat, p
~~~

### Creating the DataTransform class and functions
- The DataTransform class is created containing functions to transform data types in the pandas DataFrame 
- These functions are used to convert columns to a more appropriate format to facilitate analysis and visualisation
- The following functions are created within this class:
- obj_to_datetime: this function converts obj/str datatype to datetime, a dataframe column is specified to be converted from str to datetime using pd.to_datetime, the specific column and datetime format are arguments of the function. The dataframe is returned.
~~~
def obj_to_datetime(self, column_name, datetime_format):
    
    self.dataframe[column_name] = pd.to_datetime(self.dataframe[column_name], format = datetime_format) 
    return self.dataframe 
~~~
- obj_to_int: this function converts obj datatype to float, a dataframe column is specified to be converted from obj to float, the text is split to only obtain numerical values, which are then converted to float using pd.to_numeric. Float type is chosen over int as it can accomoate NaN/null values in conversion. The dataframe is returned.
~~~
def obj_to_int(self, column_name):

    self.dataframe[column_name] = (self.dataframe[column_name].str.extract('(\d+)'))
    self.dataframe[column_name] = pd.to_numeric(self.dataframe[column_name])
    return self.dataframe
~~~
- obj_to_str: this function converts obj datatype to string, a dataframe column is specified to be converted from obj to string using df.astype(). The dataframe is returned.
~~~
def obj_to_str(self, column_name):

    self.dataframe[column_name] = (self.dataframe[column_name]).astype('string')
    return self.dataframe
~~~
- obj_to_cat: this function converts obj datatype to categorical, a dataframe column is specified to be converted from obj to categorical using df.astype(). The dataframe is returned.
~~~
def obj_to_cat(self, column_name):

    self.dataframe[column_name] = (self.dataframe[column_name]).astype('category')
    return self.dataframe
~~~

### Creating the Plotter class and functions
- The Plotter class is created containing functions for data visualisation, this enables the identification of skewed data and outliers
- seaborn, plotly, and maplotlib libraries are used to create visualisation functions
- The following functions are created within this class, with some example code shown below:
- plot_hist: plots a histogram of the specified column of the dataframe
- plot_KDE: plots a kernel density estimation (KDE) plot of the specified column of the dataframe
- plot_box_whiskers: plots a box and whiskers plot of the specified column of the dataframe
- plot_corr_matrix: plots a correlation heatmap of the dataframe for columns containing numeric values only 
~~~
def plot_corr_matrix(self):

    sns.heatmap(self.dataframe.select_dtypes('number').corr(), annot=True, cmap='coolwarm', xticklabels=True, yticklabels=True)
    plt.show()
~~~  
- plot_bar_chart: plots a bar chart for a given dataset and specified axes
~~~
def plot_bar_chart(self, my_data, x_axis, y_axis):
      
    sns.barplot(data=my_data, y=y_axis, x=x_axis)
    plt.show()
~~~
- plot_countplot: plots a count plot of the specified column of the dataframe
~~~
def plot_countplot(self,column):

    sns.countplot(self.dataframe[column]).set(title=column)
    plt.show()
~~~

### Creating the DataFrameTransform class and functions
- The DataFrameTransform class is created containing functions for data transformation, this enables data cleaning and transformations
- The following functions are created within this class:
- drop_column: drops the specified column from the dataframe using df.drop()
~~~
def drop_column(self, column):

    self.dataframe = self.dataframe.drop(column, axis =1)
    return self.dataframe
~~~
- drop_null_rows: deletes all rows containing null values in the specified column using df.dropna()
~~~
def drop_null_rows(self, column):

    self.dataframe = self.dataframe.dropna(subset=[column])
    return self.dataframe
~~~
- impute_na_with_mean: replaces null values in a specified column with the mean of the column using df.fillna()
- impute_na_with_mode: replaces null values in a specified column with the mode of the column using df.fillna()
- impute_na_with_median: replaces null values in a specified column with the median of the column using df.fillna()
~~~
def impute_na_with_median(self, column):

    self.dataframe[column] = self.dataframe[column].fillna(self.dataframe[column].median())
    return self.dataframe
~~~
- log_transform: performs a log transform on the data in the specified column using a map function, excluding 0 values
~~~
def log_transform(self, column):

    self.dataframe[column] = self.dataframe[column].map(lambda i: np.log(i) if i > 0 else 0)
    return self.dataframe
~~~
- sqrt_transform: performs a square root transform on the data in the specified column using a map function, excluding negative values
~~~
def sqrt_transform(self, column):

    self.dataframe[column] = self.dataframe[column].map(lambda i: np.sqrt(i) if i >= 0 else i)
    return self.dataframe
~~~
- cubrt_transform: performs a cube root transform on data in the the specified column using a map function
~~~
def cubrt_transform(self, column):

    self.dataframe[column] = self.dataframe[column].map(lambda i: np.cbrt(i))
    return self.dataframe
~~~
- box_cox_transform: performs a cube root transform on data in the specified column using the inbuilt stats.boxcox
~~~
def box_cox_transform(self, column):

    self.dataframe[column] = pd.Series((stats.boxcox(self.dataframe[column]))[0]) 
    return self.dataframe
~~~
- yeo_johnson_transform: performs a yeo-johnson transformation on data in the specified column using the inbuilt stats.yeojohnson
~~~
def yeo_johnson_transform(self, column):

    self.dataframe[column] = pd.Series((stats.yeojohnson(self.dataframe[column]))[0])
    return self.dataframe
~~~
- remove_top_val: drops the entire dataframe row corresponding to the maximum value for the specified column using df.drop()
~~~
def remove_top_val(self, column):

    max_val = self.dataframe[column].max()
    self.dataframe = self.dataframe.drop(self.dataframe[self.dataframe[column] == max_val].index)
    return self.dataframe
~~~
- remove_negatives: drops the entire dataframe row corresponding to negative values in the specified column
~~~
def remove_negatives(self, column):

    self.dataframe = self.dataframe[self.dataframe[column] >= 0]
    return self.dataframe
~~~
### Converting columns to the correct format
- Methods in the DataFrameInfo class are employed to identify the data types of each column and investigate whether these are the most appropriate data types
- Columns that are the wrong data type are identified and transformed to the correct type using the DataTransform class methods
- For example, 'issue_date', 'earliest_credit_line', 'last_payment_date','next_payment_date', and 'last_credit_pull_date' were all loaded in string format, and will be converted to datetime type to enable timedelta calculations  
- Columns to be converted to a specific type are appended to a list, and data transformation is achieved by applying the applying DataTransform method to all elements of the list as shown below
~~~
col_to_convert_to_datetime = ['issue_date', 
                                 'earliest_credit_line', 
                                 'last_payment_date',
                                 'next_payment_date', 
                                 'last_credit_pull_date'] # list of strings specifying columns to be converted
for i in range(0,len(col_to_convert_to_datetime)): # loops over list of column names
       datetime_format = '%b-%Y'
       data_transform_instance.obj_to_datetime(col_to_convert_to_datetime[i],datetime_format) # calls obj_to_datetime method
~~~
### Handling null values
- Null values are identified in each column using the null_percentage method of the DataFrameInfo class
- The null percentage of each column containing nulls is printed and nulls are handled based on this percentage
~~~
nulls_info_instance = DataFrameInfo(loan_payments_df) # initialises an instnce of the class to obtain information on the dataframe
null_columns = [] # initialise list of null columns
for i in range (0, len(column_names)):
    null_pc = nulls_info_instance.null_percentage(column_names[i])
    print(column_names[i], null_pc)
    if null_pc > 0.0:
        null_columns.append(column_names[i]) # append to list of columns if there are any null values 
print(null_columns)
~~~
- Columns with a high percentage of null values (>50%) are dropped entirely as imputation is not appopriate and dropping null rows would lead to excessive data loss. Columns of this cateogry are appended to a list of strings 'columns_to_drop'
- Columns with a very small amount (<1%) of null values will have rows containing null values dropped, this can be safely done without incurring data loss as the percentage of nulls is very small. Columns of this cateogry are appended to a list of strings 'columns_to_drop_null_value_rows'
~~~
for i in range(0, len(columns_to_drop)):
      loan_payments_df_copy = remove_null_instance.drop_column(columns_to_drop[i]) # drops columns with > 50 % null values
for i in range(0, len(columns_to_drop_null_value_rows)):
      loan_payments_df_copy = remove_null_instance.drop_null_rows(columns_to_drop_null_value_rows[i]) # drops
~~~
- Columns with a moderate amount (1<%<49) of null values will be handled by imputing values, as dropping these rows could cause information loss
- Descriptive stastics (mean, median, mode, range, standard deviation) are calculated for these columns using methods from the DataFrameInfo class to determine if missing values are imputed by the mean, mode or median value
- Based on these statistics, different columns are imputed individually with the most appropriate imputation method
- For example, the 'term' column nulls are imputed with the mode value as the data in this column contains categorical data and the 'employment_length' column nulls are imputed with the median to keep all values as integers
~~~
loan_payments_df_copy = remove_null_instance.impute_na_with_mode('term') # impute null values with mode, as this is categorical data
loan_payments_df_copy = remove_null_instance.impute_na_with_median('employment_length') # impute null value with median, to keep all values as whole numbers 
loan_payments_df_copy = remove_null_instance.impute_na_with_mean('funded_amount') # impute null values with mean as data is continuous with a normal distribution 
loan_payments_df_copy = remove_null_instance.impute_na_with_mean('int_rate') # impute null values with m
~~~
- Null percentages are re-calculated for each column after nulls are dropped or imputed as a sense check 
### Identification of skewed columns
- Skewed columns are identified through data visualisation using the KDE and histogram methods from the Plotter class
~~~
for i in range(0, len(column_names_copy)):
      plotter_instance.plot_hist(column_names_copy[i])

for i in range(0, len(column_names_copy)):
      plotter_instance.plot_KDE(column_names_copy[i])
~~~
- The skew of each column is also assigned a numerical value calculated using statistical methods
- Columns with a numeric skew value <-2 or >2 are defined as skewed columns and appended to a list of skewed columns
~~~
loan_df_skew = loan_payments_df_copy.skew(axis=0,numeric_only = True) # obtain the skew of each numeric column in the dataframe
print(loan_df_skew)
check_skewed_columns = loan_df_skew.index
skewed_columns = []
for i in range(0, len(loan_df_skew)): 
      if loan_df_skew.iloc[i] > 2 or loan_df_skew.iloc[i] < -2: # append columns with a skew < -2 or > 2 to the list
         skewed_columns.append(check_skewed_columns[i])
print(skewed_columns) # show skewed columns
~~~
- Some skewed columns are not appropriate candidates for transformation and are removed from the list
- This includes columns with a majority of 0 values and those containing categorical data or ID data
- A list containing identified skewed columns is created, but no skew transformations are performed to enable querying and analysis of the data in the analysis and visualisation section
### Handling of outliers
- Data is visualised for each column using historgrams and KDE plots generated from the Plotter class to identify outliers
- Several outliers that were far beyond the normal distribution of data were identified, these were removed using the remove_top_val method of the DataFrameTransform class
~~~
columns_with_max_outliers = ['total_rec_late_fee','open_accounts','total_accounts','collection_recovery_fee'] # list of strings of column names for columns with high values to remove
for i in range(0, len(columns_with_max_outliers)):
      loan_payments_df_transformed = transform_instance.remove_top_val(columns_with_max_outliers[i]) # re
~~~
- Negative outliers were identified in columns where context specific knowledge indicated that negative values were not logical, these were removed using the remove_negatives method of the DataFrameTransform class
~~~
columns_with_negatives = ['recoveries','last_payment_amount'] # list of strings of column names for columns with -ve values to remove
for i in range(0, len(columns_with_negatives)):
      loan_payments_df_transformed = transform_instance.remove_negatives(columns_with_negatives[i]) # remove negative values
~~~
### Identification of overly correlated columns
- Overly correlated columns are identified with a correlation heatmap but no correlated columns are dropped in order to enable querying and analysis of the full dataset
- Overly correlated columns are identified as those with a correlation heatmap value >0.9
~~~
transformed_plotter_instance.plot_corr_matrix() # visualise correlated columns
~~~
### Saving the cleaned data
- Data cleaning has been completed and the cleaned data is saved to a pickle file to preserve data types 
~~~
loan_payments_df_transformed.to_pickle('cleaned_data.pickle')
~~~
## Data analysis and visualisation
- Analysis is then performed on the transformed and cleaned data to uncover relationships and information about the state of the loans and future projections to gain deeper insights into the data, enabling informed business decisions
- The data is queried to evaluate the current state of the loans and payments and visualise future projections
### Summarise the % of loans recovered against investor/total funding and visualise projected recovery up to 6 months in the future 
- The company wants to check what percentage of loans have been a loss to the company, loans marked as 'Charged Off' in the loan_status column represent a loss to the company.
- Recovered loans are defined as those where the outstanding principal is 0, percentage is calculated as a percentage of total loans issued
~~~
out_prncp_zeros = (loan_payments_df.out_prncp == 0.00).sum()  
loans_recov_against_total_funding = (out_prncp_zeros/(len(loan_payments_df)))*100
print(f"Percentage of the loans recovered against the investor funding and the total amount funded = {loans_recov_against_total_funding.round(2)} %")
~~~
- EDA revealed a 1:1 correlation between out_prncp (outstanding principal) and out_prncp_inv (outstanding investor principal), percentage recovered is therefore the same for both measures
- Results are visualised as a bar plot
![2_bar_chart](/Users/tigerdavies/Test/EDA_plots/2_bar_chart.png)

- The remaining balance of the loans is calculcated monthly up to 6 months in the future in order to project recovery
- The monthly installment is subtracted from the remaining balance to calculcate the remaining balance for each month
- The remaining balance is summed for each month to calculate the percentage recovery as month1_pc, month2_pc etc.
- This projection is visualised with a scatter plot
~~~
month_no = [1,2,3,4,5,6]
loans_recovered_pc = [month1_pc, month2_pc, month3_pc, month4_pc, month5_pc, month6_pc]
recovery_df = pd.DataFrame({'Month': month_no,'Recovery_percentage': loans_recovered_pc}) # create df to plot data 
fig2 = plt.figure(2)
sns.scatterplot(data=recovery_df, x='Month', y='Recovery_percentage') # scatter plot of data to visualise projection
~~~
## Installation instructions
Code was created using Python 3.11.4
The following libraries are used: datetime, matplotlib.pyplot, numpy, pyplot, pandas, pickle, plotly.express, scipy.stats, seaborn, sqlalchemy, yaml

## Usage instructions 
Files should be run in the following order:
1. db_utils.py
2. db_data_cleaning_and_analysis.ipynb

## File structure
### Core files
- db_utils.py - This file contains the code for extracting the data from the cloud into a csv file
- db_info.py - This file contains classes for obtaining descriptive statistics for columns in the dataframe
- db_datatransform.py - This file contains classes for transforming data types in the dataframe
- db_clean_data.py - This file contains classes for dealing with null values, skewed data, outliers, and overly correlated columns
- db_data_cleaning_and_analysis.ipynb - This is a jupyter notebook containing the code for data cleaning and transformation, EDA, and data analysis and visualisation. This is the main file for the execution of the project.

### Supplementary files
- db_data_analysis.py - This file contains the code for analysing the cleaned and transformed data
- db_familiarise.ipynb - This file contains code for familiarisation with the dataset, used as initial rough working
- license.txt - This file contains the infromation for the license applicable to this project
- data_dictionary.md - This file is a dictionary of all the columns in the data set and what data they refer to
- loan_payments.csv - This file is the original dataset
- loan_payments_transformed.csv - This file contains the dataset with data transformations
- cleaned_data.pickle - This file contains the fully cleaned and transformed dataset ready for analysis 

## License information
License is Apache License 2.0, full details can be found in license.txt