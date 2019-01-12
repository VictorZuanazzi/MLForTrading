# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 11:38:41 2019

@author: Victor Zuanazzi
"""

import pandas as pd

def test_run():
    """open a CSV file containing stock data and prints parts of it."""
    data_frame = pd.read_csv("HCP.csv")
    print (data_frame.head())
    print (data_frame[2:5])
    print (data_frame.tail())
    
    
if __name__ == "__main__":
    test_run()