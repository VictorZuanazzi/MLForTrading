# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 22:59:15 2019
Coursera: https://classroom.udacity.com/courses/ud501/lessons/4156938722/concepts/41890188580923
Lesson 8

@author: Victor Zuanazzi
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import time
import MLforTrading as ml #custom library

class portifolio(ml.df_4_trading):
    
    def allocate(self, columns, percentage, date_of_allocation, volume_allocated=1):
        """"Creates a dataframe with the allocation for each stock.
        Input:
            columns: [["ABC","XYZ","GGG","LOVE"]] stocks where there is some 
                allocation;
            percentages: {"ABC": 0.1,"XYZ: 0.3","GGG": 0.2,"LOVE": 0.4} a dict 
                with the percentages for each stock.
            date_of_allocation: date in which the stocks were bought.
            volume_allocated: total ammount allocated, if not filled the 
                dataframe self.allocation shows the percentages of allocation.
        """
        self.date_of_allocation = date_of_allocation
        if sum(percentage.values()) != 1:
            print (f"Percentages sum up to {sum(percentages.values())} != 1.")
            print ("Please correct the percentages and call callocate again")

        else:
            self.allocation = self.normalize_data(self.df[date_of_allocation:self.end_date][columns].copy())
            for symbol in percentage:
                self.allocation[symbol] *= percentage[symbol]
            self.invested_dates = pd.date_range(date_of_allocation, self.end_date)
            total = pd.DataFrame(data = self.allocation.sum(axis=1), columns = ["Total"])
            self.allocation = self.allocation.join(total)
            self.allocation *=volume_allocated
            self.add_daily_return()
            
    def add_daily_return(self):
        daily_returns = pd.DataFrame(index = self.allocation.index)
        daily_returns["Daily R"] = self.allocation["Total"].copy()
                                     
        daily_returns["Daily R"].iloc[1:] = (self.allocation["Total"]/self.allocation["Total"].shift()) -1
        daily_returns["Daily R"].iloc[0] = 0

        self.allocation = self.allocation.join(daily_returns)
        
    def average_daily_return(self, date):
        return self.allocation[self.date_of_allocation:date]["Daily R"].mean()
    
    def std_daily_return(self,date):
        return self.allocation[self.date_of_allocation:date]["Daily R"].std()
    
    def cumulative_daily_return(self, date, symbol = "Total"):       
        dd = pd.date_range(date, periods=2, freq='D')
        return self.allocation[symbol].iloc[0]/self.allocation[dd[0]:dd[1]][symbol]
    
    def portifolio_statistics(self, date):
        
        cumulative_dr = self.cumulative_daily_return(date)
        
        average_dr = self.average_daily_return(date)
        
        std_dr = self.std_daily_return(date)
        
        #organizes everything in a nice dictionary
        p_stats = {"cumulative daily return": cumulative_dr,
                   "average daily return": average_dr,
                   "std_daly_return": std_dr
                   }
        
        return p_stats
          
def test_run():
    """"Function called by test run"""
    
    #Define date range:
    start_date = "2010-01-01"
    end_date = "2014-12-31"
    
    symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols.sort()
    
    p = portifolio(symbols, start_date, end_date)
    investments = {"HCP": 0.1, "IBM": 0.2, "AAPL":0.7}
    p.allocate(list(investments.keys()), investments, "2014-01-01", 100)

    print(p.allocation.head(10))
    print(p.allocation.tail(10))
    print(p.portifolio_statistics("2014-10-31"))
    print(p.cumulative_daily_return("2014-10-31"))
    

    
if __name__ == "__main__":
    test_run()