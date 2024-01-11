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
- Classes are created to facilitate EDA and data visualisation 
- Data is then cleaned and transformed after undergoing EDA

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
- The following functions are created within this class, with some example code shown below::
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
### Handling null values
### Identification of skewed columns
### Handling of outliers
### Identification of overly correlated columns
Columns in the dataframe are converted to the correct type
Missing/null values are handled on a case-by-case basis, and are either dropped, imputed or the whole variable is removed
Skewed columns are identified and handled by transformation
Outliers are identified and removed if appropriate
Overly correlated columns are identified and dropped

### Data analysis and visualisation
Analysis is then performed on the transformed and cleaned data to uncover relationships and information about the state of the loans and future projections

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