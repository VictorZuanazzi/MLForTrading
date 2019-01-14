# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 18:30:49 2019
Coursera: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41890188580923
Lesson 5, item 9 Bollinger Bands

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
    title = "Bollinger BAnds"
    window = 20
    
    #compute rolling mean using a 20-day window   
    moving_average = w.df["SPY"].rolling(window = window).mean()
    
    #compute rulling std using a 20-day window
    upper_band = moving_average + 2*w.df["SPY"].rolling(window = window).std()
    lower_band = moving_average - 2*w.df["SPY"].rolling(window = window).std()
    
    ax = w.df["SPY"].plot(figsize=(20,15), fontsize = 15)
    moving_average.plot(ax = ax, label = "mean")
    upper_band.plot(ax = ax, label = "upper band")
    lower_band.plot(ax = ax, label = "lower band")
    plt.title(title, fontsize = 50)
    plt.ylabel("Price [$]", fontsize = 20)
    plt.xlabel("Dates", fontsize = 20)
    plt.legend(fontsize = 20)
    plt.show()

    
if __name__ == "__main__":
    test_run()