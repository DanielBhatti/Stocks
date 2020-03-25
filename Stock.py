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
    def __init__(self):
        self.Data = []
        
    def AddRow(self, row):
        self.Data.append(row)