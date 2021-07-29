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

'-----------------------------------------------------------------------------------------------------------------'

# Obtain all countries from the database
equities_countries = fd.show_options('equities', 'countries')
# Obtain all sectors from the database
equities_sectors = fd.show_options('equities', 'sectors')
# Obtain all industries from the database
equities_industries = fd.show_options('equities', 'industries')
# Obtain all countries + sectors + industries from the database
equities_all_categories = fd.show_options('equities')


COUN = 'United States'
INDUS = 'Aerospace & Defense'

companylist = fd.select_equities(country=COUN, industry=INDUS)

companylist = {k:v for k,v in companylist.items() if not '.' in k}


companyList = []
for symbol in companylist:
    companyList.append(symbol)
    
# companyList = ['AAPL','STEM','MP','BABA','TSM','CTXR','LMT','TSLA','C']

'--------------------------------------------------------------------------------------------------------------'

fundamentals = {}
for a in range(len(companyList)):
    fundamentals[companyList[a]] = get_json("https://finance.yahoo.com/quote/" + companyList[a])
    
fundamentals = {k: v for k, v in fundamentals.items() if len(v) != 0}

companyList = []
for symbol in fundamentals:
    companyList.append(symbol)


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
    
'-----------------------------------------------------------------------------------------------------------------------'
    
parameter = []
name = []

for i in range(len(companyList)):
    if globals()['%s' %companyList[i]].pegRatio is None:
        pass
    else:
        parameter.append(globals()['%s' %companyList[i]].pegRatio)
        name.append(globals()['%s' %companyList[i]].name)
        
constructBarH(parameter, name)

'----------------------------------------------------------------------------------------------------------------------'
# Collate DataFrame

name = []
sharePrice = []
marketCap = []
forwardPE = []
pegRatio = []
priceToBook = []
currentRatio = []
ebitdaMargins = []
quickRatio = []
profitMargins = []
debtToEquity = []
operatingMargins = []
earningsGrowth = []

for i in range(len(companyList)):
    if globals()['%s' %companyList[i]].name != None:
        name.append(globals()['%s' %companyList[i]].name)
    elif globals()['%s' %companyList[i]].name == None:
        name.append(0)
        
    if globals()['%s' %companyList[i]].sharePrice != None:
        sharePrice.append(globals()['%s' %companyList[i]].sharePrice)
    elif globals()['%s' %companyList[i]].sharePrice == None:
        sharePrice.append(0)
        
    if globals()['%s' %companyList[i]].marketCap != None:
        marketCap.append(globals()['%s' %companyList[i]].marketCap)
    elif globals()['%s' %companyList[i]].marketCap == None:
        marketCap.append(0)

    if globals()['%s' %companyList[i]].forwardPE != None:
        forwardPE.append(globals()['%s' %companyList[i]].forwardPE)
    elif globals()['%s' %companyList[i]].forwardPE == None:
        forwardPE.append(0)        
        
    if globals()['%s' %companyList[i]].pegRatio != None:
        pegRatio.append(globals()['%s' %companyList[i]].pegRatio)
    elif globals()['%s' %companyList[i]].pegRatio == None:
        pegRatio.append(0)

    if globals()['%s' %companyList[i]].priceToBook != None:
        priceToBook.append(globals()['%s' %companyList[i]].priceToBook)
    elif globals()['%s' %companyList[i]].priceToBook == None:
        priceToBook.append(0)
        
    if globals()['%s' %companyList[i]].currentRatio != None:
        currentRatio.append(globals()['%s' %companyList[i]].currentRatio)
    elif globals()['%s' %companyList[i]].currentRatio == None:
        currentRatio.append(0)
        
    if globals()['%s' %companyList[i]].ebitdaMargins != None:
        ebitdaMargins.append(globals()['%s' %companyList[i]].ebitdaMargins)
    elif globals()['%s' %companyList[i]].ebitdaMargins == None:
        ebitdaMargins.append(0)
        
    if globals()['%s' %companyList[i]].quickRatio != None:
        quickRatio.append(globals()['%s' %companyList[i]].quickRatio)
    elif globals()['%s' %companyList[i]].quickRatio == None:
        quickRatio.append(0)
        
    if globals()['%s' %companyList[i]].profitMargins != None:
        profitMargins.append(globals()['%s' %companyList[i]].profitMargins)
    elif globals()['%s' %companyList[i]].profitMargins == None:
        profitMargins.append(0)
        
    if globals()['%s' %companyList[i]].debtToEquity != None:
        debtToEquity.append(globals()['%s' %companyList[i]].debtToEquity)
    elif globals()['%s' %companyList[i]].debtToEquity == None:
        debtToEquity.append(0)
        
    if globals()['%s' %companyList[i]].operatingMargins != None:
        operatingMargins.append(globals()['%s' %companyList[i]].operatingMargins)
    elif globals()['%s' %companyList[i]].operatingMargins == None:
        operatingMargins.append(0)
        
    if globals()['%s' %companyList[i]].earningsGrowth != None:
        earningsGrowth.append(globals()['%s' %companyList[i]].earningsGrowth)
    elif globals()['%s' %companyList[i]].earningsGrowth == None:
        earningsGrowth.append(0)


data = {'Name': name,
        'sharePrice': sharePrice,
        'marketCap': marketCap,
        'forwardPE': forwardPE,
        'pegRatio': pegRatio,
        'priceToBook': priceToBook,
        'currentRatio': currentRatio,
        'ebitdaMargins': ebitdaMargins,
        'quickRatio': quickRatio,
        'profitMargins': profitMargins,
        'debtToEquity': debtToEquity,
        'operatingMargins': operatingMargins,
        'earningsGrowth': earningsGrowth
        }

Collated = pd.DataFrame(data)
    
    
    
    
