# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 23:44:09 2020

@author: bhatt
"""

import pandas as pd
import datetime
import pandas_datareader.data as web
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from matplotlib import style
import StockAnalysis

if(__name__ == "__main__"):
    start = datetime.datetime(1950, 1, 1)
    end = datetime.date.today()
    
    foundEarliestStartYear = False
    yearsSinceStart = 0
    while(not foundEarliestStartYear):
        try:
            web.DataReader("SPY", 'yahoo', start, end)
            foundEarliestStartYear = True
        except:
            yearsSinceStart += 1
            start = datetime.datetime(1950 + yearsSinceStart, 1, 1)
    
    # df is a dictionary
    # The keys are High, Low, Open, Close, Volume, Adj Close
    # To get the date for a given row, use df[key].index[rowNumber]
    # In other words, df[key].index[rowNumber] is the date for df[key][rowNumber]
    df = web.DataReader("SPY", 'yahoo', start, end)
    
    stock = StockAnalysis.Stock()
    stock.InsertPandasDataFrame(df)
    
    x = []
    y = []
    
    for i in range(0, len(stock.Data)):
        currentRow = stock.Data[i]
        x.append(currentRow.TransactionDate)
        y.append(currentRow.Close)
        
    alpha = 0.01
    stockSimulator = StockAnalysis.StockSimulator(stock)
    sA = StockAnalysis.StrategyA(stockSimulator)
    sA.Execute(alpha)
    curveX, curveY = sA.GetExponentialMeanAverageData(alpha)
        
    plt.plot_date(x, y, fmt = '.', xdate = True)
    plt.plot_date(curveX, curveY, fmt = '-', xdate = True)