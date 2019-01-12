# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 12:17:35 2019

@author: Victor Zuanazzi
"""

import pandas as pd
import matplotlib.pyplot as plt

def test_run():
    """"Function called by test run"""
    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "SPY", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    
    for s in symbols:
       df = pd.read_csv(f"{s}.csv")
       #plt.figure(figsize=(15,10))
       df[["Close", "Adj Close"]].plot()
       plt.title(f"{s}")
       plt.ylabel("price")
       plt.xlabel("days")
       
       plt.show()
       
if __name__ == "__main__":
    test_run()