# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 17:42:53 2019
Coursera: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41890188580923
Lesson 5, item 8 Compute rolling statistics

@author: Victor Zuanazzi
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import time
import MLforTrading as ml

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
    
    #compute rolling mean using a 20-day window   
    rolling_mean = w.df["SPY"].rolling(20).mean()
    
    #compute rulling std using a 20-day window
    rustd = rolling_mean + w.df["SPY"].rolling(20).std()
    rlstd = rolling_mean - w.df["SPY"].rolling(20).std()
    
    #plot rolling mean:
    w.compare_plots(w.df["SPY"], start_date, end_date, rolling_mean)
    
    
if __name__ == "__main__":
    test_run()