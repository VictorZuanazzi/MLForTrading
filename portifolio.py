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
import scipy.optimize as spo

class portfolio(ml.df_4_trading):
    
    def allocate(self, columns, percentage, date_of_allocation, volume_allocated=1, verbose = False):
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
        
        #percentages must sum up to 1!
        if sum(percentage.values()) != 1:
            if verbose:
                print (f"Percentages sum up to {sum(percentage.values())} != 1.")

            #Short cut to ensure sum of allocations add to one.
            #percentage[self.symbols[0]] += 1.0 - sum(percentage.values()) 

        
        #Step 1: normalize the data by the date_of_alocation
        self.allocation = self.normalize_data(self.df[date_of_allocation:self.end_date][columns].copy())
        
        #Step 2: multiply each investment by its percentage in the portfolio
        for symbol in percentage:
            self.allocation[symbol] *= percentage[symbol]
        
        #Step 3: Calculate the value of the portifolio for each day
        self.invested_dates = pd.date_range(date_of_allocation, self.end_date)
        total = pd.DataFrame(data = self.allocation.sum(axis=1), columns = ["Total"])
        self.allocation = self.allocation.join(total)
        
        #Step 4: Multiply the entire dataframe by the Total Amount invested.
        self.allocation *=volume_allocated
        
        #Step 5: Include daily returns
        self.add_daily_return()
            
    def add_daily_return(self):
        """Adds the daily return column to the portfolio"""
        
        daily_returns = pd.DataFrame(index = self.allocation.index)
        daily_returns["Daily R"] = self.allocation["Total"].copy()                                  
        daily_returns["Daily R"].iloc[1:] = (self.allocation["Total"]/self.allocation["Total"].shift()) -1
        daily_returns["Daily R"].iloc[0] = 0
        self.allocation = self.allocation.join(daily_returns)
        
    def average_daily_return(self, date):
        """return the average daily returns from the begining of the allocation 
        to the specified date"""
        return self.allocation[self.date_of_allocation:date]["Daily R"].mean()
    
    def std_daily_return(self,date):
        """return the standard deviation of the daily returns from the begining 
        of the allocation to the specified date"""
        return self.allocation[self.date_of_allocation:date]["Daily R"].std()
    
    def cumulative_daily_return(self, date, symbol = "Total"):     
        """return the cumulative return from the begining of the allocation to
        the specified date for the specified symbol"""
        dd = pd.date_range(date, periods=2, freq='D')
        return self.allocation[dd[0]:dd[1]][symbol][0]/self.allocation[symbol].iloc[0] - 1
    
    def daily_risk_free_rate(self, risk_free_rate = 0, year = 252):
        """returns the daily risk free rate"""
        return (1 + risk_free_rate)**(1/year) - 1
    
    def sharpe(self, date, risk_free_rate = 0):
        """returns the shape value for the application"""
        drfr = self.daily_risk_free_rate(risk_free_rate)
        av_dr = self.average_daily_return(date)
        std_dr = self.std_daily_return(date)
        return (av_dr + drfr)/std_dr
    
    def neg_sharpe(self, percentages, volume_allocated, risk_free_rate):
        investments = {self.symbols[i]: percentages[i] for i in range(len(percentages))}
        
        self.allocate(self.symbols, 
                      investments, 
                      self.date_of_allocation,
                      volume_allocated)
        
        date = self.end_date
        return -1*self.sharpe(date, risk_free_rate)
    
    def portfolio_statistics(self, date):
        """returns the cumulative return, average and standard deviation of 
        daily returns from the begining of the allocation to the specified date.
        Return type : dictionary"""
        
        cumulative_dr = self.cumulative_daily_return(date)
        
        average_dr = self.average_daily_return(date)
        
        std_dr = self.std_daily_return(date)
        
        s = self.sharpe(date)
        
        #organizes everything in a nice dictionary
        p_stats = {"cumulative daily return": cumulative_dr,
                   "sharpe": s,
                   "average daily return": average_dr,
                   "std_daly_return": std_dr                   
                   }
        
        return p_stats
    
    def optimize_allocation(self, date_of_allocation, volume_allocated = 1, risk_free_rate = 0):
        """Makes the optimal single bullet allocation.
        inputs:
            date_of_allocation: the date 
            volume_allocated:
        returns:
            a vector containing the percentages of allocation. 
            The portfolio is also made, but such is not returned"""
        
        self.date_of_allocation = date_of_allocation
        
        # constructs the dictionary to feed self.allocate()
        investments = {symbol: 1/len(self.symbols) for symbol in self.symbols}
       
        
        #One of the investments inicial guess is modified so the total sum is
        #ensured to be 1
        investments[self.symbols[0]] += (1 - sum(investments.values()))
        
        #cretes a list that spo.minimize can handle.
        #This only works because the list self.symbols does not change overtime.
        percentages = list(investments.values())
        
        #makes the first allocation.
        self.allocate(self.symbols, 
                      investments, 
                      self.date_of_allocation,  
                      volume_allocated)
        
        #error function
        error_func = self.neg_sharpe
        
        #bounds spo.minimze has to respect
        #the percentages have to be between 0 and 1
        zero_to_one = tuple([0,1] for i in range(len(investments)))
        
        #constraint spo.minize has to respect
        #the sum of all percentages must be 1
        sum_to_one = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0})
        
        #minimizer
        result = spo.minimize(error_func,
                              percentages, 
                              args = (volume_allocated, risk_free_rate),
                              method = "SLSQP",
                              options={"disp": False},
                              bounds = zero_to_one,
                              constraints = sum_to_one)
        return result.x
    
    def CAPM_error_function(self, w, status = False):
        
        #w = abs(w)
        total = w.dot(self.betas*self.signs)
        if status:
            print(w, sum(w))
        
        return total**2
    
    def CAPM_allocation(self, volume_allocated = 1):
        """Not completelly working yet, the sum of percentages do no add to 1"""
        
        CAPM = {}
        self.weights = np.zeros(len(self.symbols)-1)
        self.betas = np.zeros(len(self.symbols)-1)
        self.signs = np.zeros(len(self.symbols)-1)
        
        for i, symbol, in enumerate(self.symbols):
            if symbol != "SPY":
                CAPM[symbol] = list(self.compare_scatter_daily_returns("SPY", 
                                                                 symbol, 
                                                                 self.start_date, 
                                                                 self.end_date, 
                                                                 plot = False))
                
                
                self.betas[i] = CAPM[symbol][0]
                self.signs[i] = np.sign(CAPM[symbol][1])
                self.weights[i] = np.random.rand()*self.signs[i]

        if sum(self.weights) < 0:
            self.weights = np.where(self.weights>0,  #condition
                                    self.weights + abs(2*sum(self.weights)), #if true
                                    self.weights) #if false

        self.weights = self.weights/abs(sum(self.weights)) #normalize sum to 1
            
            
        error_func = self.CAPM_error_function
        sum_to_one = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1.0})
        neg_one_to_one = tuple([-1,1] for i in range(len(self.weights)))
        #minimizer
        result = spo.minimize(error_func,
                              self.weights,
                              method = "SLSQP",
                              options={"disp": False},
                              #bounds = neg_one_to_one,
                              constraints = sum_to_one)
        
        self.weights = np.concatenate((self.weights, np.zeros(1)))
        self.signs = np.concatenate((self.signs, np.zeros(1)))
        investments = {symbol: self.weights[i] for i, symbol in enumerate(self.symbols)}
        self.date_of_allocation = self.start_date      
        
        
        self.allocate(self.symbols, 
                      investments, 
                      self.date_of_allocation,  
                      volume_allocated)
        
        #print(self.allocation)
        
          
def test_run():
    """"Function called by test run"""
    
    #Define date range:
    start_date = "2010-01-01"
    end_date = "2010-12-31"
    
    #symbols = ["HCP", "STZ", "BBBY", "CHK", "AAPL", "IBM", "WMT", "PG", "XOM"]
    symbols = [ "AAPL","XOM", "GOOG"]
    symbols.sort() #not necessary, but helps in readbility.
    
    p = portfolio(symbols, start_date, end_date)
    
    p.CAPM_allocation()
    print(p.allocation.head())
    print(p.allocation.tail())
    
#    p = portfolio(symbols, start_date, end_date)
#    bla = p.optimize_allocation("2010-01-01", volume_allocated = 1)
#    print(bla)
#    
#    print(p.allocation.head())
#    print(p.allocation.tail())
#    p.plot_stock_prices(p.allocation[["AAPL", "GLD", "Total"]])
#
#    spy = portfolio(["SPY"], start_date, end_date)
#    spy.allocate(["SPY"], {"SPY": 1,}, start_date)
#    spy.plot_stock_prices(spy.allocation["SPY"])
    

    
if __name__ == "__main__":
    test_run()