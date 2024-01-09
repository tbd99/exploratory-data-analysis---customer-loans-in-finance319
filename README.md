# exploratory-data-analysis---customer-loans-in-finance319
Perform exploratory data analysis on the loan portfolio, using various statistical and data visualisation techniques to uncover patterns, relationships, and anomalies in the loan data.

## Project description
The aim of this project is to gain a comprehensive understanding of the loan portfolio data of a large financial instiution by performing exploratory data analysis (EDA) using various statistical and data visualistion methods, demonstrating a strong understanding and knowledge of these techniques. This will enable patterns, relationships and anomalies in the data to be revealed, thereby facilitating the improvement of the the performance and profitability of the loan portfolio. 

This project will be a practical application and demonstration of the various data analysis skills I have developed in the AiCore data analysis course.

The first section of the project is EDA for data cleaning and preparation. The process is as follows:
Columns in the dataframe are converted to the correct type
Missing/null values are handled on a case-by-case basis, and are either dropped, imputed or the whole variable is removed
Skewed columns are identified and handled by transformation
Outliers are identified and removed if appropriate
Overly correlated columns are identified and dropped

Analysis is then performed on the transformed and cleaned data to uncover relationships and information about the state of the loans and future projections

## Installation instructions
Code was created using Python 3.11.4
The following libraries are used: datetime, matplotlib.pyplot, numpy, pandas, pickle, plotly.express, scipy.stats, seaborn,sqlalchemy, yaml

## Usage instructions 
Files should be run in the following order:
1. db_utils.py
2. db_datatransform.py
3. db_info.py
4. db_clean_data.py
5. db_data_analysis.py

## File structure
db_utils.py - This file contains the code for extracting the data from the cloud into a csv file 
db_info.py - This file contains classes for obtaining descriptive statistics for columns in the dataframe
db_datatransform.py - This file contains classes for transforming data types in the dataframe
db_clean_data.py - This file contains classes for dealing with null values, skewed data, outliers, and overly correlated columns 
db_data_analysis.py - This file contains the code for analysing the cleaned and transformed data
db_familiarise.ipynb - This file contains code for familiarisation with the dataset, used as initial rough working
license.txt - This file contains the infromation for the license applicable to this project
data_dictionary.md - This file is a dictionary of all the columns in the data set and what data they refer to 
loan_payments.csv - This file is the original dataset 
loan_payments_transformed.csv - This file contains the dataset with data transformations
cleaned_data.pickle - This file contains the fully cleaned and transformed dataset ready for analysis 

## License information
License is Apache License 2.0, full details can be found in license.txt