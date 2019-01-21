# -*- coding: utf-8 -*-
"""
Created on Mon Jan 21 22:04:30 2019
Source: https://classroom.udacity.com/courses/ud501/lessons/4351588706/concepts/43677793280923
Lesson 9, part 3: Minimizer in Python
@author: Victor Zuanazzi
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo

def f(X):
    """Given a scallar X, returm some real value"""
    Y = (X - 1.5)**2 + 0.5
    #print (f"X = {X}, Y = {Y}")
    return Y

def test_run():
    """"Function called by test run"""
    
    Xguess = np.random.uniform(low= -10, high = 10)
    min_result = spo.minimize(f, Xguess, method = "SLSQP", options={"disp": True})
    print (f"Xmin = {min_result.x}, Ymin = {min_result.fun}")

    #Plot functin values, mark minima
    Xplot = np.linspace(0.5, 2.5, 21)
    Yplot = f(Xplot)
    plt.plot(Xplot, Yplot)
    plt.plot(min_result.x, min_result.fun, 'ro')
    plt.title("Minima of an objective function")
    plt.show()
    
if __name__ == "__main__":
    test_run()