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
### Loading the data 
- Credentials are loaded from a yaml file with the defined load_yaml function, database credentials are added to the .gitignore file in order to maintain security
- An instance of the RDSDatabaseConnector class is intiailised and the SQLAlchemy_initialiser method is called to initialise an engine
- A connection is initilised to the RDS database and the RDS data is loaded to a pandas DataFrame using the extract_to_pandas function
- The resulting dataframe is saved to a .csv file using the save_to_csv function and the connection to the RDS database is closed

## Exploratory data analysis (EDA) and data cleaning 
- Classes are created to facilitate EDA and data visualisation 
- Data is then cleaned and transformed after undergoing EDA
### Creating the DataFrameInfo class and functions
- The DataFrameInfo class is created containing functions get information and descriptive statistics from the pandas DataFrame being analysed
- These functions are used to gain insight into the data when performing EDA and enables the identification of outliers, nulls, incorrect data types etc.
- The following functions are created within this class:
- get_datatypes: returns the datatype of each column in the dataframe
- get_uniquevals: returns the unique values a specified column in the dataframe
- get_median: returns the median value of a specified column in the dataframe
- get_stdev: returns the standard deviation value of a specified column in the dataframe
- get_mean: returns the mean value of a specified column in the dataframe
- get_mode: returns the mode value of a specified column in the dataframe
- print_shape: prints the shape of the dataframe
- null_percentage: returns the percentage of null values in a specified column in the dataframe
- get_range: returns the range of values in a specified column in the dataframe
- get_normal_dist: returns the p value of the data in a specified column, giving the normal distribution
### Creating the DataTransform class and functions
- The DataTransform class is created containing functions to transform data types in the pandas DataFrame 
- These functions are used to convert columns to a more appropriate format to facilitate analysis and visualisation
- The following functions are created within this class:
- obj_to_datetime: this function converts obj/str datatype to datetime, a dataframe column is specified to be converted from str to datetime, the specific column and datetime format are arguments of the function. The dataframe is returned.
- obj_to_int: this function converts obj datatype to float, a dataframe column is specified to be converted from obj to float, the text is split to only obtain numerical values, which are then converted to float. Float type is chosen over int as it can accomoate NaN/null values in conversion. The dataframe is returned.
- obj_to_str: this function converts obj datatype to string, a dataframe column is specified to be converted from obj to string. The dataframe is returned.
- obj_to_cat: this function converts obj datatype to categorical, a dataframe column is specified to be converted from obj to categorical. The dataframe is returned.





### Creating the DataFrameTransform class and functions
### Creating the Plotter class and functions
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