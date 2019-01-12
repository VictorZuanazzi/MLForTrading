# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 12:06:24 2019

@author: Victor Zuanazzi
"""

import pandas as pd


def get_mean_volume(symbol):
    """Return the mean volume for stock indicated by symbol.
    Note: Data for stock is stored in the same folder as this file.
    """
    df = pd.read_csv("{}.csv".format(symbol)) # read data as pandas dataframe.
    return df["Volume"].mean() # return mean
    
def test_run():
    """"Function called by test run"""
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    for s in symbols:
        print(f"Mean volume of {s}: ", get_mean_volume(s))
    
    
if __name__ == "__main__":
    test_run()