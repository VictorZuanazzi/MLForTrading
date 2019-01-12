# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 13:54:49 2019

@author: Victor Zuanazzi
"""

import pandas as pd
import matplotlib.pyplot as plt

def test_run():
    """"Function called by test run"""
    
    #Define date range:
    start_date = "2010-01-22"
    end_date = "2010-01-26"
    dates = pd.date_range(start_date, end_date)
    
    #Create an empty dataframe
    df1 = pd.DataFrame(index=dates)

    #Read SPY data into temporary dataframe
    dfSPY = pd.read_csv("SPY.csv",
                        index_col="Date",
                        parse_dates = True,
                        usecols = ["Date", "Adj Close"],
                        na_values= ["nan"])
    
    #Rename "Adj Close" column to "SPY" 
    dfSPY = dfSPY.rename(columns={"Adj Close":"SPY"})
    
    #Join the two dataframes
    df1 = df1.join(dfSPY, how = 'inner')

    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    for s in symbols:
        df_temp = pd.read_csv(f"{s}.csv",
                              index_col="Date",
                              parse_dates = True,
                              usecols = ["Date", "Adj Close"],
                              na_values= ["nan"])
        df_temp = df_temp.rename(columns={"Adj Close" : s})
        df1 = df1.join(df_temp)
    print(df1)
       
if __name__ == "__main__":
    test_run()