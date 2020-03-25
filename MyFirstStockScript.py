# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 22:17:04 2019

@author: bhatt
"""

import pandas as pd
import datetime
import pandas_datareader.data as web
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
from matplotlib import style

class StockRow:
    def __init__(self, transactionDate, highPrice, lowPrice, openPrice, closePrice, volume, adjClosePrice):
        self.TransactionDate = transactionDate
        self.High = highPrice
        self.Low = lowPrice
        self.Open = openPrice
        self.Close = closePrice
        self.Volume = volume
        self.AdjClose = adjClosePrice
        
class Stock:
    def __init__(self):
        self.Data = []
        
    def AddRow(self, row):
        self.Data.append(row)

class StockSimulator:
    def __init__(self, stock):
        self.Stock = stock
        self.CurrentDay = stock.Data[0].TransactionDate
        self.CurrentDayIndex = 0
        self.LastTradingIndex = len(stock.Data) - 1
        self.OwnedStocks = []
        self.SoldStocks = []
        self.MoneySpent = []
        
    def GoToNextDay(self):
        if(self.CurrentDayIndex == self.LastTradingIndex):
            return
        else:
            self.CurrentDayIndex += 1
            self.CurrentDay = stock.Data[self.CurrentDayIndex].TransactionDate
        
    def PurchaseStock(self, numOfStocks = 1):
        stockPrice = self.Stock.Data[self.CurrentDayIndex].Close
        for i in range(0, numOfStocks):
            self.OwnedStocks.append(stockPrice)
            self.MoneySpent.append(stockPrice)
            
    def SellAllStocks(self):
        stockPrice = self.Stock.Data[self.CurrentDayIndex].Close
        for i in range(0, len(self.OwnedStocks)):
            self.SoldStocks.append(stockPrice)
        self.OwnedStocks = []
        
    def GetCurrentStockPrice(self):
        stockPrice = self.Stock.Data[self.CurrentDayIndex].Close
        return stockPrice
        
    def IsLastTradingDay(self):
        return self.CurrentDayIndex == self.LastTradingIndex

if __name__ == "__main__":
    
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
    
    stock = Stock()
    for i in range(len(df)):
        transactionDate = pd.to_datetime(df['High'].index[i])
        highPrice = df['High'][i]
        lowPrice = df['Low'][i]
        openPrice = df['Open'][i]
        closePrice = df['Close'][i]
        volume = df['Volume'][i]
        adjClosePrice = df['Adj Close'][i]
    
        
        stockRow = StockRow(transactionDate, highPrice, lowPrice, openPrice, closePrice, volume, adjClosePrice)
        stock.AddRow(stockRow)
    
    x = []
    y = []
    
    curveX = []
    curveY = []
    
    ema = 0
    for i in range(1, len(stock.Data)):
        previousRow = stock.Data[i - 1]
        currentRow = stock.Data[i]
        x.append(currentRow.TransactionDate)
        y.append(currentRow.Close)
        
        alpha = 1.0
        if(i == 1):
            ema = previousRow.Close
            x.append(currentRow.TransactionDate)
            y.append(currentRow.Close)
            curveX.append(currentRow.TransactionDate)
            curveY.append(ema)
        else:
            ema = alpha * currentRow.Close + (1 - alpha) * ema
        
        curveX.append(currentRow.TransactionDate)
        curveY.append(ema)
        
    ss = StockSimulator(stock)
    ss.GoToNextDay()
    while(not ss.IsLastTradingDay()):
        ss.GoToNextDay()
        if(curveY[ss.CurrentDayIndex] > curveY[ss.CurrentDayIndex - 1] and curveY[ss.CurrentDayIndex - 2] > curveY[ss.CurrentDayIndex - 1]):
            print('Purchased one (1) stock for ', ss.GetCurrentStockPrice(), ' on ', ss.CurrentDay)
            ss.PurchaseStock()
        elif(curveY[ss.CurrentDayIndex] < curveY[ss.CurrentDayIndex - 1] and curveY[ss.CurrentDayIndex - 2] < curveY[ss.CurrentDayIndex - 1]):
            willSell = True
            for elem in ss.OwnedStocks:
                if elem > ss.GetCurrentStockPrice():
                    willSell = False
            if(willSell):
                print('Selling ', len(ss.OwnedStocks), ' stocks for ', ss.GetCurrentStockPrice(), ' each on ', ss.CurrentDay)
                ss.SellAllStocks()
    ss.SellAllStocks()
    
    moneySpent = 0
    moneyMade = 0
    for elem in ss.MoneySpent:
        moneySpent += elem
    for elem in ss.SoldStocks:
        moneyMade += elem
    
    print('Spent ', moneySpent, ' and made ', moneyMade)
    print('Total revenue was ', moneyMade - moneySpent)
    
    #plt.plot(x, y, '.')
    plt.plot_date(x, y, fmt = '.', xdate = True)
    plt.plot_date(curveX, curveY, fmt = '-', xdate = True)
        
    """
    close_px = df['Adj Close']
    #mavg = close_px.rolling(window=100).mean()
    
    close_px.plot(label='SPY')
    #mavg.plot(label='mavg')
    plt.legend()
    """
    