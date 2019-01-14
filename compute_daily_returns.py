# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 19:22:55 2019

Coursera: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41890188580923
Lesson 5, item 11 Daily returns

@author: Victor Zuanazzi
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import time
import MLforTrading as ml #custom library

def test_run():
    """"Function called by test run"""
    
    #Define date range:
    start_date = "2014-01-01"
    end_date = "2014-12-31"
    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    
    w = ml.df_4_trading(symbols, start_date, end_date)
    #w.plot_stock_prices(w.df["SPY"])
    df = w.df
    title = "daily returns"
    
    #compute daily returns
    daily_returns = df.copy()
    daily_returns[1:] = (df/df.shift(1)) -1
    daily_returns.iloc[0, :] = 0
    
    #ax = w.df["SPY"].plot(figsize=(20,15), fontsize = 15)
    daily_returns["2014-02-01":"2014-03-01"]["SPY"].plot(figsize=(20,15))
    plt.title(title, fontsize = 50)
    plt.ylabel("Price [$]", fontsize = 20)
    plt.xlabel("Dates", fontsize = 20)
    plt.legend(fontsize = 20)
    plt.show()

    
if __name__ == "__main__":
    test_run()