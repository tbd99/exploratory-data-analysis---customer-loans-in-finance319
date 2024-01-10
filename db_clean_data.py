
from datetime import datetime 
from db_datatransform import DataTransform
from db_info import DataFrameInfo
from db_info import read_csv
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px 
import seaborn as sns
import pickle as pkl

class Plotter():
   '''
   This class contains functions to plot data
   Attributes:
    df (pd DataFrame): The dataframe to be evaluated 
   '''
   def __init__(self, df):
      self.dataframe = df 

   def plot_hist(self, column):
      '''
      This function plots a histogram of the specified column
      '''
      self.dataframe[column].hist(bins=100)
      title = str(column)
      plt.title(title)
      plt.show() 
   
   def plot_KDE(self, column):
      '''
      This function plots KDE plot of the specified column
      '''
      sns.histplot(data=self.dataframe, x=column, kde=True)
      sns.despine()
      title = str(column)
      plt.title(title)
      #plt.show()

   def plot_box_whiskers(self, column):
      '''
      This function plots a box and whisker plot for the specified column
      '''
      fig = px.box(self.dataframe, y=column,width=600, height=500, title=str(column))
      fig.show()
   
   def plot_corr_matrix(self):
      '''
      This funciton plots a correlation heatmap of the dataframe for numeric values
      '''
      sns.heatmap(self.dataframe.select_dtypes('number').corr(), annot=True, cmap='coolwarm', xticklabels=True, yticklabels=True)
      plt.show()
   
   def plot_bar_chart(self, my_data, x_axis, y_axis):
      '''
      This funciton plots a bar chart for a given dataset and specified axes
      '''
      sns.barplot(data=my_data, y=y_axis, x=x_axis)
      plt.show()
   
   def plot_countplot(self,column):
      '''
      This function plots a count plot for the specified column
      '''
      sns.countplot(self.dataframe[column]).set(title=column)
      #plt.show()
   
class DataFrameTransform():
   '''
   This class contains functions to remove null values from data and functions for data transformations 
   Attributes:
    df (pd DataFrame): The dataframe to be evaluated 
   '''
   def __init__(self, df):
      self.dataframe = df 
      
   def drop_column(self, column):
      '''
      This function drops the specified column from the dataframe
      '''
      self.dataframe = self.dataframe.drop(column, axis =1)
      return self.dataframe
   
   def drop_null_rows(self, column):
      '''
      This function deletes all rows containing null values in the specified column
      '''
      self.dataframe = self.dataframe.dropna(subset=[column])
      return self.dataframe
   
   def impute_na_with_mean(self, column):
      '''
      This function replaces null values in a specified column with the mean of the column
      '''
      self.dataframe[column] = self.dataframe[column].fillna(self.dataframe[column].median())
      return self.dataframe
   
   def impute_na_with_mode(self, column):
      '''
      This function replaces null values in a specified column with the mode of the column
      '''
      self.dataframe[column] = self.dataframe[column].fillna(self.dataframe[column].mode()[0])
      return self.dataframe
   
   def impute_na_with_median(self, column):
      '''
      This function replaces null values in a specified column with the median of the column
      '''
      self.dataframe[column] = self.dataframe[column].fillna(self.dataframe[column].median())
      return self.dataframe
   
   def log_transform(self, column):
      '''
      This function performs a log transform on the specified column, excluding 0 values
      '''
      self.dataframe[column] = self.dataframe[column].map(lambda i: np.log(i) if i > 0 else 0)
      return self.dataframe
   
   def sqrt_transform(self, column):
      '''
      This function performs a square root transform on the specified column, excluding negative values
      '''
      self.dataframe[column] = self.dataframe[column].map(lambda i: np.sqrt(i) if i >= 0 else i)
      return self.dataframe
   
   def cubrt_transform(self, column):
      '''
      This function performs a cube root transform on the specified column
      '''
      self.dataframe[column] = self.dataframe[column].map(lambda i: np.cbrt(i))
      return self.dataframe
   
   def box_cox_transform(self, column):
      '''
      This function performs a box cox transformation on the specified column 
      ''' 
      self.dataframe[column] = pd.Series((stats.boxcox(self.dataframe[column]))[0]) 
      return self.dataframe
   
   def yeo_johnson_transform(self, column):
      '''
      This function performs a yeo-johnson transformation on the specified column
      '''
      self.dataframe[column] = pd.Series((stats.yeojohnson(self.dataframe[column]))[0])
      return self.dataframe

   def remove_top_val(self, column):
      '''
      This function removes the row corresponding to the maximum value for the specified column
      '''
      max_val = self.dataframe[column].max()
      self.dataframe = self.dataframe.drop(self.dataframe[self.dataframe[column] == max_val].index)
      return self.dataframe
   
   def remove_negatives(self, column):
      '''
      This function removes rows containining negative values in the specified column
      '''
      self.dataframe = self.dataframe[self.dataframe[column] >= 0]
      return self.dataframe
