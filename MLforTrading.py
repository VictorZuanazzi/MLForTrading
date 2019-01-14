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
        
        self.df.fillna(method = "ffill", inplace = True)
        self.df.fillna(method = "bfill", inplace = True)
    
    def SMA(self, columns, window = 20):
        """Return the Simple Moving Average of the stocks."""
        return self.df[columns].rolling(window = window).mean()
    
    def rolling_std(self, columns, window = 20):
        """Return the Standard Deviation of the stocks."""
        return self.df[columns].rolling(window = window).std()
    
    def bollinger_bands(self, symbol, window = 20, plot = False):
        """Return a dataframe with the stock prices, mean and bands for the 
        columns given."""
        
        mean = self.SMA(symbol, window = window)           
        std = self.rolling_std(symbol, window = window)
        upper_band = mean + 2*std         
        lower_band = mean - 2*std
        
        bb_df = pd.DataFrame(index = self.dates)        
        bb_df = bb_df.join(self.df[symbol], how = "inner")  
        bb_df = bb_df.join(lower_band.rename(columns={symbol[0] : "Lower Band"}))  
        bb_df = bb_df.join(mean.rename(columns={symbol[0] : "Mean"}))   
        bb_df = bb_df.join(upper_band.rename(columns={symbol[0] : "Upper Band"})) 
        
        if plot:
            self.plot_stock_prices(bb_df, title = "Bollinger Bands")
        
        return bb_df
    
    def daily_returns(self, columns, start_date, end_date, plot = False):
        """Return a dataframe with the daily returns of the stocks.
        """
        
        daily_returns = self.df[start_date:end_date][columns].copy()
        daily_returns[1:] = (self.df[start_date:end_date][columns]/self.df[start_date:end_date][columns].shift()) -1
        daily_returns.iloc[0, :] = 0
        
        if plot:
            self.plot_stock_prices(daily_returns,
                                   title = "Daily Returns")
        
        return daily_returns
    
    def histogram_stats(self, df, plot = False):
        mean = df.mean()
        std = df.std()
        kurtosis = df.kurtosis()
        
        if plot:
            self.plot_hist(df)
        
        return mean, std, kurtosis
    
    def plot_hist(self, df, bins = 10):
        """Plot histogram"""
        df.hist(bins = 10, figsize = (20,15))
        mean = df.mean()
        plt.axvline(x=mean[0], color="w", linestyle = "dashed", linewidth = 2, label = "Mean")
        std = df.std()
        plt.axvline(std[0], color="r", linestyle = "dashed", linewidth = 2, label = "Standard Deviation")
        plt.axvline(-std[0], color="r", linestyle = "dashed", linewidth = 2)
        plt.legend(fontsize = 15)
        plt.show()
       
    def compare_hist_daily_returns(self, columns, start_date, end_date):
        """Compare histogram of daily returns of multiple stocks"""
        daily_returns =self.daily_returns(columns, start_date, end_date)
        
        for s in columns:
            daily_returns[s].hist(bins = 20, label = s, figsize = (20,15))
        
        plt.legend(fontsize = 20)
        plt.show()
        
        
    def cumulative_returns(self, columns, start_date, end_date, plot = False):
        """Return a dataframe with the cumulative returns starting at start_date"""
        c_df = self.normalize_data(self.df[start_date:end_date][columns])
        
        if plot:
            self.plot_normalized(columns, start_date, end_date)
        
        return c_df
        
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
        """"Plot normalized stock prices for the specified range of days and 
        symbos."""
        plt_df = self.normalize_data(self.df.loc[start_date:end_date][columns])
        self.plot_stock_prices(plt_df)
        
    def normalize_data(self, df_temp):
        """Normalize stock prices using the first row of the dataframe"""
        return df_temp/df_temp.iloc[0,:]
    
    def compare_plots(self, df_columns, start_date, end_date, external_data, title = "Stock prices"):
        """Plot external data together with stock prices"""
        ax = df_columns.plot(figsize=(20,15), fontsize = 15)
        external_data.plot(ax = ax)
        plt.title(title, fontsize = 50)
        plt.ylabel("Price [$]", fontsize = 20)
        plt.xlabel("Dates", fontsize = 20)
        plt.legend(fontsize = 20)
        plt.show()
        

def test_run():
    """"Function called by test run"""
    
    #Define date range:
    start_date = "2010-01-01"
    end_date = "2014-12-31"
    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    
    w = df_4_trading(symbols, start_date, end_date)
    #w.plot_normalized(["SPY","IBM"], "2010-01-01", "2011-01-01")
    dr = w.daily_returns(["SPY"], start_date, "2011-01-01", plot= False)
    
    #print(w.histogram_stats(dr, plot = True))
    w.compare_hist_daily_returns(["SPY", "IBM"],  start_date, end_date)
    
if __name__ == "__main__":
    test_run()