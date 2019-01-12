# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 00:02:10 2019
Coursera: https://classroom.udacity.com/courses/ud501/lessons/3975568860/concepts/41007385930923#
Lesson 3, item 12

@author: Victor Zuanazzi
"""

import pandas as pd
import os
import matplotlib.pyplot as plt

def symbol_to_path(symbol, base_dir=""):
    """"Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, f"{str(symbol)}.csv")

def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbos from CSV files."""
    data_frame = pd.DataFrame(index = dates)
    
    #"SPY" will always be added in the beggining as refference
    if "SPY" in symbols:
        #If SPY is already present, we delet it first to avoid duplicates.
        symbols.pop(symbols.index("SPY"))
    symbols.insert(0, "SPY")
    
    #Add all list of symbols to the dataframe
    for s in symbols:
        path = symbol_to_path(s)
        df_temp = pd.read_csv(path,
                              index_col="Date",
                              parse_dates = True,
                              usecols = ["Date", "Adj Close"],
                              na_values= ["nan"])
        df_temp = df_temp.rename(columns={"Adj Close" : s})
        if s == "SPY":
            data_frame = data_frame.join(df_temp, how = 'inner')
        else: 
            data_frame = data_frame.join(df_temp)
            
    return data_frame

def test_run():
    """"Function called by test run"""
    
    #Define date range:
    start_date = "2010-01-22"
    end_date = "2010-01-26"
    dates = pd.date_range(start_date, end_date)
    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    
    df1 = get_data(symbols, dates)
    
    print(df1)
       
if __name__ == "__main__":
    test_run()