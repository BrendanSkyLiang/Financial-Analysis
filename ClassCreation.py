# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 09:13:23 2021

@author: brendanlia
"""

import FinanceDatabase as fd
import numpy as np
import xlsxwriter
import pandas as pd
import openpyxl
from openpyxl import load_workbook
import time
import sys
import os
import re
import io
import math
from yfinance.utils import get_json
from yfinance import download
import matplotlib.pyplot as plt
import json

class Company:
    def __init__(self, name, sharePrice, marketCap, forwardPE, pegRatio, priceToBook, currentRatio, ebitdaMargins, quickRatio, profitMargins, debtToEquity, operatingMargins, earningsGrowth):
        self.name = name
        self.sharePrice = sharePrice
        self.marketCap = marketCap
        self.forwardPE = forwardPE
        self.pegRatio = pegRatio 
        self.priceToBook = priceToBook
        self.currentRatio = currentRatio 
        self.ebitdaMargins = ebitdaMargins
        self.quickRatio = quickRatio
        self.profitMargins = profitMargins
        self.debtToEquity = debtToEquity
        self.operatingMargins = operatingMargins
        self.earningsGrowth = earningsGrowth
        
def constructBarH(parameter, name):
    y_pos = np.arange(len(name))
    plt.barh(y_pos, parameter)
    plt.yticks(y_pos, name, rotation='horizontal')

companyList = ['AAPL','STEM','MP','BABA','TSM','CTXR','LMT','TSLA','C']

fundamentals = {}
for a in range(len(companyList)):
    fundamentals[companyList[a]] = get_json("https://finance.yahoo.com/quote/" + companyList[a])
    
for i in range(len(companyList)):
    name = fundamentals[companyList[i]]['quoteType']['shortName']
    sharePrice = fundamentals[companyList[i]]['financialData']['currentPrice']
    marketCap =  fundamentals[companyList[i]]['summaryDetail']['marketCap']
    forwardPE = fundamentals[companyList[i]]['defaultKeyStatistics']['forwardPE']
    pegRatio = fundamentals[companyList[i]]['defaultKeyStatistics']['pegRatio']
    priceToBook = fundamentals[companyList[i]]['defaultKeyStatistics']['priceToBook']
    currentRatio = fundamentals[companyList[i]]['financialData']['currentRatio']
    ebitdaMargins = fundamentals[companyList[i]]['financialData']['ebitdaMargins']
    quickRatio = fundamentals[companyList[i]]['financialData']['quickRatio']
    profitMargins = fundamentals[companyList[i]]['financialData']['profitMargins']
    debtToEquity = fundamentals[companyList[i]]['financialData']['debtToEquity']
    operatingMargins = fundamentals[companyList[i]]['financialData']['operatingMargins']
    earningsGrowth = fundamentals[companyList[i]]['financialData']['earningsGrowth']
    globals()['%s' %companyList[i]] = Company(name, sharePrice, marketCap, forwardPE, pegRatio, priceToBook, currentRatio, ebitdaMargins, quickRatio, profitMargins, debtToEquity, operatingMargins, earningsGrowth)
    
    
forwardPE = []
for i in range(len(companyList)):
    forwardPE.append(globals()['%s' %companyList[i]].forwardPE)
    
constructBarH(forwardPE, companyList)
    
    
    
    
