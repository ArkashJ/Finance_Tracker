import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

class DataStore:
    def __init__(self, data, company_name):
        self.df = pd.DataFrame(data)
        self.company_name = company_name

    def pre_process_data(self):
        self.df = self.df.dropna()
        self.df.drop(columns=['date', 'cik', 'reportedCurrency', 'fillingDate', 'acceptedDate', 
                              'calendarYear', 'period', 'link', 'finalLink'], inplace=True)    

    def print_data(self):
        print(self.df)

    def describe_data(self):
        print(self.df.describe())

    def calculate_correlation(self, col1, col2):
        corr = self.df[col1].corr(self.df[col2])
        print(self.df[col1].corr(self.df[col2]))
        return corr

    def visualize_data(self, columns):
        for col in columns:
            plt.figure(figsize=(10,6))
            self.df[col].plot(kind='bar')
            plt.title(f'Bar plot for {col}')
            plt.ylabel(col)
            plt.xlabel(self.company_name)  # Use the company name as the x label
            plt.show()
