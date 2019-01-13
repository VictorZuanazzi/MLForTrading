# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 01:44:33 2019

@author: Victor Zuanazzi
"""

import pandas as pd
import os
import matplotlib.pyplot as plt

class df_4_trading:
    
    def __init__(self, symbols, start_date, end_date):
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date
        self.dates = pd.date_range(start_date, end_date)
        self.create_data_frame()

    def symbol_to_path(self, symbol, base_dir=""):
        """"Return CSV file path given ticker symbol."""
        return os.path.join(base_dir, f"{str(symbol)}.csv")

    def get_df(self, symbol, columns, jhow = "left"):
        """Join the price info of the symbol in the dataframe"""
        path = self.symbol_to_path(symbol)
        df_temp = pd.read_csv(path,
                          index_col="Date",
                          parse_dates = True,
                          usecols = columns,
                          na_values= ["nan"])
        df_temp = df_temp.rename(columns={columns[1] : symbol})
        self.df = self.df.join(df_temp, how = jhow)

    def create_data_frame(self, use_col = "Adj Close"):
        """Read stock data (adjusted close) for given symbos from CSV files."""
        self.df = pd.DataFrame(index = self.dates)
        
        #"SPY" will always be added in the beggining as refference
        if "SPY" in self.symbols:
            #If SPY is already present, we delet it first to avoid duplicates.
            self.symbols.pop(symbols.index("SPY"))
        self.get_df("SPY", ["Date", use_col], jhow = "inner")
        
        #Add all symbols of the list to the dataframe
        for s in self.symbols:
            self.get_df(s, ["Date", use_col])

    def plot_stock_prices(self, df , title = "Stock prices"):
        """"Plot stock prices"""
        df.plot(figsize=(20,15), fontsize = 15)
        plt.title(title, fontsize = 50)
        plt.ylabel("Price [$]", fontsize = 20)
        plt.xlabel("Dates", fontsize = 20)
        plt.legend(fontsize = 20)
        plt.show()

    def plot_selected(self, columns, start_date, end_date):
        """"Plot stock prices for the specified range of days and symbos."""
        plt_df = self.df.loc[start_date:end_date][columns]
        self.plot_stock_prices(plt_df)
    
    def plot_normalized(self,columns, start_date, end_date):
        """"Plot normalized stock prices for the specified range of days and symbos."""
        plt_df = self.normalize_data(self.df.loc[start_date:end_date][columns])
        self.plot_stock_prices(plt_df)
        
    def normalize_data(self, df_temp):
        """Normalize stock prices using the first row of the dataframe"""
        return df_temp/df_temp.iloc[0,:]

def test_run():
    """"Function called by test run"""
    
    #Define date range:
    start_date = "2010-01-01"
    end_date = "2014-12-31"
    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    
    w = df_4_trading(symbols, start_date, end_date)
    w.plot_normalized(["SPY","IBM"], "2010-01-01", "2011-01-01")


    
if __name__ == "__main__":
    test_run()