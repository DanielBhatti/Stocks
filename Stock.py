# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:10:29 2020

@author: bhatt
"""

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
        
    # Use to add data, each row of data must be later than all previous rows
    # This ensures that the data is always in date order
    def AddStockRow(self, stockRow):
        if(len(self.Data) > 0):
            lastStockRow = self.Data[-1]
            if(lastStockRow.TransactionDate < stockRow.TransactionDate):
                self.Data.append(stockRow)
            else:
                raise Exception("Can only add rows in order of transaction date.")
       
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