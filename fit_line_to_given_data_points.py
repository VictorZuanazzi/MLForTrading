# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 22:29:14 2019

Source: https://classroom.udacity.com/courses/ud501/lessons/4351588706/concepts/43677793280923
Lesson 9, part 9: Fit Line to given data points

@author: Victor Zuanazzi
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo

def error(line, data):
    """Compute error between given line model and observed data.
    Input:
        line: (slope, Y-intercept)
        data: 2D array where each row is a point (x,y)
    Return: Summed Squared Y-axis error"""
    return np.sum((data[:,1] - (line[0] * data[:, 0] + line[1]))**2)


def fit_line(data, error_func):
    """Fit a line to given data, using a supplied error function
    Input:
        data: D array where each row is a point (x0,y)
        error_func: function that computes the error between a line and observed 
            data
    Return: line parameters that minimize the error function"""
    
    #Generate initial guess for line model
    #slope = 0, Y-intercept = mean of Y values
    end_idx = int(np.random.uniform(len(data)/2, len(data)))
    start_dx = int(np.random.uniform(0, end_idx/2))
    slope = (data[end_idx][1] - data[start_dx][1]) / (data[end_idx][0] - data[start_dx][0])
    y_intercept = np.mean(data[:, 1])/slope 
    l = np.float32([slope, y_intercept])
    
    #Plot initial guess
    x_ends = np.float32([0, 10])
    plt.plot(x_ends, l[0] * x_ends + l[1], "m--", linewidth = 2.0,
             label = "Initial Guess")
    
    #call optimizer to minimize error function
    result = spo.minimize(error_func, l, args =(data,), method = "SLSQP",
                          options={"disp": True})
    return result.x
        

def test_run():
    """"Function called by test run"""
    
    #Define original line
    l_orig = np.float32([4,2])
    print(f"Original line: C0 = {l_orig[0]}, C1 = {l_orig[1]}") 
    Xorig = np.linspace(0,10,21)
    Yorig = l_orig[0] * Xorig + l_orig[1]
    plt.plot(Xorig, Yorig, "b--", linewidth = 2.0, label = "Original line")
    
    #Generate noisy data points
    noise_sigma = 3.0
    noise = np.random.normal(0, noise_sigma, Yorig.shape)
    data = np.asarray([Xorig, Yorig + noise]).T
    plt.plot(data[:,0], data[:, 1], "go", label = "Data points")
    
    #Try to fit a line to this data
    l_fit = fit_line(data, error)
    print(l_fit)
    print(f"Fitted line: C0 = {l_fit[0]}, C1 = {l_fit[1]}") 
    plt.plot(data[:, 0], l_fit[0] * data[:, 0] + l_fit[1], "r--", 
             linewidth=2.0, label = "Line fit")
    
    plt.show()
    
if __name__ == "__main__":
    test_run()
    
