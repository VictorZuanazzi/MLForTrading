# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 21:25:22 2019

Coursera: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41890188580923
Lesson 7, item 13 Scaterplots

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
    start_date = "2000-01-01"
    end_date = "2014-12-31"
    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    
    w = ml.df_4_trading(symbols, start_date, end_date)

    title = "daily returns"
    
    daily_returns = w.daily_returns(["SPY", "XOM", "PG", "CHK"], 
                                    start_date, 
                                    "2011-01-01", 
                                    plot= False) #compute daily returns
    
    beta, alpha = np.polyfit(daily_returns["SPY"], daily_returns["XOM"], 1)
    
    daily_returns.plot(kind="scatter", 
                       x="SPY", 
                       y = "XOM", 
                       figsize = (20,15))
    
    plt.plot(daily_returns["SPY"], 
             beta*daily_returns["SPY"]+alpha, 
             "-", 
             color = "r",
             label = f"{beta}*x + {alpha}")
    plt.title(title, fontsize = 50)
    plt.ylabel("Price [$]", fontsize = 20)
    plt.xlabel("Dates", fontsize = 20)
    plt.legend(fontsize = 20)
    plt.show()
    
    print(daily_returns.corr(method = "pearson"))

    
if __name__ == "__main__":
    test_run()