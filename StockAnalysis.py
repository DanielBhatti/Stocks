# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:10:29 2020

@author: bhatt
"""

import pandas as pd

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
    # Data will contain StockRows in TransactionDate order
    def __init__(self):
        self.Data = []
        
    def InsertPandasDataFrame(self, df):
        for i in range(len(df)):
            transactionDate = pd.to_datetime(df['High'].index[i])
            highPrice = df['High'][i]
            lowPrice = df['Low'][i]
            openPrice = df['Open'][i]
            closePrice = df['Close'][i]
            volume = df['Volume'][i]
            adjClosePrice = df['Adj Close'][i]
            
            stockRow = StockRow(transactionDate, highPrice, lowPrice, openPrice, closePrice, volume, adjClosePrice)
            self.AddStockRow(stockRow)
        
        
    # Use to add data, each row of data must be later than all previous rows
    # This ensures that the data is always in date order
    def AddStockRow(self, stockRow):
        if(len(self.Data) > 0):
            lastStockRow = self.Data[-1]
            if(lastStockRow.TransactionDate < stockRow.TransactionDate):
                self.Data.append(stockRow)
            else:
                raise Exception("Can only add rows in order of transaction date.")
        else:
            self.Data.append(stockRow)
       
    # Input a datetime, returns the StockRow with the same datetime
    # Returns None if it can't find any
    def GetStockRowAtDateTime(self, dateTime):
        for i in range(len(self.Data)):
            stockRow = self.Data[i]
            if(stockRow.TransactionDate == dateTime):
                return stockRow
        return None
    
    # Input a datetime, returns an array of all StockRows with TransactionDates less than that datetime
    def GetStockRowsUntilDateTime(self, dateTime):
        data = []
        for i in range(len(self.Data)):
            stockRow = self.Data[i]
            if(stockRow.TransactionDate <= dateTime):
                data.append(stockRow)
            else:
                break
        return data
    
class StockSimulator:
    def __init__(self, stock):
        self.Stock = stock
        self.CurrentDay = stock.Data[0].TransactionDate
        self.CurrentDayIndex = 0
        self.CurrentStockRow = stock.Data[0]
        self.LastTradingIndex = len(stock.Data) - 1
        self.NumberOfOwnedStocks = 0
        self.PurchasedStocks = []
        self.SoldStocks = []
        
    def GoToNextDay(self):
        if(self.CurrentDayIndex == self.LastTradingIndex):
            return
        else:
            self.CurrentDayIndex += 1
            self.CurrentDay = self.Stock.Data[self.CurrentDayIndex].TransactionDate
            self.CurrentStockRow = self.Stock.Data[self.CurrentDayIndex]
            return self.CurrentDayIndex
        
    def PurchaseStock(self, numOfStocks = 1, currentPrice = None):
        if(currentPrice is None):
            currentPrice = self.CurrentStockRow.Close
        for i in range(0, numOfStocks):
            self.PurchasedStocks.append(currentPrice)
        self.NumberOfOwnedStocks += numOfStocks
        return currentPrice * numOfStocks
            
    def SellStock(self, numOfStocks = None, currentPrice = None):
        if(numOfStocks is None):
            numOfStocks = self.NumberOfOwnedStocks
        if(currentPrice is None):
            currentPrice = self.CurrentStockRow.Close
        if(self.NumberOfOwnedStocks >= numOfStocks):
            for i in range(0, numOfStocks):
                self.SoldStocks.append(currentPrice)
        self.NumberOfOwnedStocks -= numOfStocks
        return currentPrice * numOfStocks
        
    def IsLastTradingDay(self):
        return self.CurrentDayIndex == self.LastTradingIndex
    
class StockStrategy:
    def __init__(self, stockSimulator):
        self.StockSimulator = stockSimulator
        self.Money = 0
        
    def AddMoney(self, amountOfMoney):
        self.Money += amountOfMoney
        
    def PurchaseStock(self, numOfStocks = 1):
        self.Money -= self.StockSimulator.PurchaseStock(numOfStocks)
    
    def SellStock(self, numOfStocks = 1):
        self.Money += self.StockSimulator.SellStock(numOfStocks)
        
    def CanBuyStock(self, stockPrice):
        if(self.Money < stockPrice):
            return False
        else:
            return True
        
class StrategyA(StockStrategy):
    def __init__(self, stockSimulator):
        super().__init__(stockSimulator)
        
    def Execute(self, alpha = 0.5):
        ss = self.StockSimulator
        y = self.GetExponentialMeanAverageData(alpha)[1]
        while(not ss.IsLastTradingDay()):
            ss.GoToNextDay()
            if(y[ss.CurrentDayIndex] > y[ss.CurrentDayIndex - 1] and y[ss.CurrentDayIndex - 2] > y[ss.CurrentDayIndex - 1]):
                print('Purchased one (1) stock for ', ss.CurrentStockRow.Close, ' on ', ss.CurrentDay)
                ss.PurchaseStock()
            elif(y[ss.CurrentDayIndex] < y[ss.CurrentDayIndex - 1] and y[ss.CurrentDayIndex - 2] < y[ss.CurrentDayIndex - 1]):
                willSell = True
                for elem in ss.PurchasedStocks:
                    if elem > ss.CurrentStockRow.Close:
                        willSell = False
                if(willSell):
                    print('Selling ', len(ss.PurchasedStocks), ' stocks for ', ss.CurrentStockRow.Close, ' each on ', ss.CurrentDay)
                    ss.SellStock()
        ss.SellStock()
        
        moneySpent = 0
        moneyMade = 0
        for elem in ss.PurchasedStocks:
            moneySpent += elem
        for elem in ss.SoldStocks:
            moneyMade += elem
            
        print('Spent ', moneySpent, ' and made ', moneyMade)
        print('Total revenue was ', moneyMade - moneySpent)
        print('Total profit percentage was ', moneyMade/moneySpent)
        
    def GetExponentialMeanAverageData(self, alpha = 0.5):
        stockData = self.StockSimulator.Stock.Data
        emaDates = []
        emaPrices = []
        
        ema = stockData[0].Close
        emaDates.append(stockData[0].TransactionDate)
        emaPrices.append(stockData[0].Close)
        for i in range(1, len(stockData)):
            ema = alpha * stockData[i].Close + (1 - alpha) * ema
            emaDates.append(stockData[i].TransactionDate)
            emaPrices.append(ema)
            
        return [emaDates, emaPrices]