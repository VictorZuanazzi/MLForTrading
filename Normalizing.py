# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 01:37:19 2019
Coursera: https://classroom.udacity.com/courses/ud501/lessons/3975568860/concepts/41007385970923#
Lesson 3, item 19 - Normalizing
@author: Victor Zuanazzi
"""

import pandas as pd
import os
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir=""):
    """"Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, f"{str(symbol)}.csv")

def get_df(data_frame, symbol, columns, jhow = "left"):
    path = symbol_to_path(symbol)
    df_temp = pd.read_csv(path,
                          index_col="Date",
                          parse_dates = True,
                          usecols = columns,
                          na_values= ["nan"])
    df_temp = df_temp.rename(columns={columns[1] : symbol})
    data_frame = data_frame.join(df_temp, how = jhow)
    return data_frame

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbos from CSV files."""
    data_frame = pd.DataFrame(index = dates)
    
    #"SPY" will always be added in the beggining as refference
    if "SPY" in symbols:
        #If SPY is already present, we delet it first to avoid duplicates.
        symbols.pop(symbols.index("SPY"))
    data_frame = get_df(data_frame, "SPY", ["Date", "Adj Close"], jhow = "inner")
    
    #Add all symbols of the list to the dataframe
    for s in symbols:
        data_frame = get_df(data_frame, s, ["Date", "Adj Close"])
            
    return data_frame

def plot_data(df, title = "Stock prices"):
    """"Plot stock prices"""
    df.plot(figsize=(20,15), fontsize = 15)
    plt.title(title, fontsize = 50)
    plt.ylabel("Price [$]", fontsize = 20)
    plt.xlabel("Dates", fontsize = 20)
    plt.legend(fontsize = 20)
    plt.show()

def plot_selected(df, columns, start_date, end_date):
    plt_df = normalize_data(df.loc[start_date:end_date][columns])
    plot_data(plt_df)
    
def normalize_data(df):
    """Normalize stock prices using the first row of the dataframe"""
    return df/df.iloc[0,:]

def test_run():
    """"Function called by test run"""
    
    #Define date range:
    start_date = "2010-01-01"
    end_date = "2014-12-31"
    dates = pd.date_range(start_date, end_date)
    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    
    df1 = get_data(symbols, dates)
    plot_selected(df1,["SPY","IBM"], "2010-01-01", "2011-01-01")

    
    
if __name__ == "__main__":
    test_run()