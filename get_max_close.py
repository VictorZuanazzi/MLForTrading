# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 11:49:49 2019

@author: Victor Zuanazzi
"""


import pandas as pd


def get_max_close(symbol):
    """Return the maximum closing value for stock indicated by symbol.
    Note: Data for stock is stored in the same folder as this file.
    """
    df = pd.read_csv("{}.csv".format(symbol)) # read data as pandas dataframe.
    return df["Close"].max() # return max
    
def test_run():
    """"Function called by test run"""
    symbols = ["HCP", "STZ", "BBBY", "CHK"]
    symbols.sort()
    for s in symbols:
        print(f"Max close of {s}: ", get_max_close(s))
    
    
if __name__ == "__main__":
    test_run()