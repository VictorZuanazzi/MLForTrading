# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 21:45:26 2019
Coursera: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41890188580923
Lesson 15
@author: Victor Zuanazzi
"""


import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import time
import MLforTrading as ml #custom library
import scipy.optimize as spo
import portifolio as port #custom library
          
def test_run():
    """"Function called by test run"""
    
    #Define date range:
    start_date = "2010-01-01"
    end_date = "2010-12-31"
#    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    
    w = ml.df_4_trading(symbols, start_date, end_date)

    CAPM = {}
    
    print(w.df.head())
    for symbol in symbols:
        if symbol != "SPY":
            CAPM[symbol] = w.compare_scatter_daily_returns("SPY", 
                                                         symbol, 
                                                         start_date, 
                                                         end_date, 
                                                         plot = False)
    
    
    
    
    
    #symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
#    symbols = [ "AAPL","XOM", "GOOG", "GLD"]
#    symbols.sort() #not necessary, but helps in readbility.
#    
#    p = port.portfolio(symbols, start_date, end_date)
#    bla = p.optimize_allocation("2010-01-01", volume_allocated = 1)
#    print (bla)
#    print(p.allocation.head())
#    print(p.allocation.tail())
#    p.plot_stock_prices(p.allocation[["AAPL", "GLD", "Total"]])
#
#    spy = port.portfolio(["SPY"], start_date, end_date)
#    spy.allocate(["SPY"], {"SPY": 1,}, start_date)
#    spy.plot_stock_prices(spy.allocation["SPY"])
    

    
if __name__ == "__main__":
    test_run()