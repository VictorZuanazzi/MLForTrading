# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 17:27:12 2019
Coursera: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41890188580923
Lesson 5, item 4 Compute global Statistics

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
    start_date = "2010-01-01"
    end_date = "2014-12-31"
    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    
    w = ml.df_4_trading(symbols, start_date, end_date)
    #w.plot_normalized(["SPY","IBM"], "2010-01-01", "2011-01-01")
    print("Mean:")
    print(w.df.mean())
    print("Median:")
    print(w.df.median())
    print("std:")
    print(w.df.std())
    
    

    
if __name__ == "__main__":
    test_run()