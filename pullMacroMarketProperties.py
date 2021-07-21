#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 20 19:10:08 2021

@author: brendanliang
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

Cs = ['b','g','r','c','m','y','k','tab:orange','tab:olive','indigo','aquamarine','tomato','navy','khaki','maroon','deepskyblue','forestgreen']

'----------------------------------------------------------------------------------------------------------------------------'

# Obtain all countries from the database
equities_countries = fd.show_options('equities', 'countries')

# Obtain all sectors from the database
equities_sectors = fd.show_options('equities', 'sectors')

# Obtain all industries from the database
equities_industries = fd.show_options('equities', 'industries')

# Obtain all countries + sectors + industries from the database
equities_all_categories = fd.show_options('equities')


COUN = 'United States'
INDUS = 'Biotechnology'


companylist = fd.select_equities(country=COUN, industry=INDUS)

companylist = {k:v for k,v in companylist.items() if not '.' in k}

'-----------------------------------------------------------------------------------------------------------------------------'
# can be deactivitaed if json file exists
fundamentals = {}
for symbol in companylist:
    fundamentals[symbol] = get_json("https://finance.yahoo.com/quote/" + symbol)

# stock_data = download(list(companylist))

fundamentals = {k:v for k,v in fundamentals.items() if not '.' in k}

with open(COUN + INDUS + '.json', 'w') as fp:
    json.dump(fundamentals, fp)

'------------------------------------------------------------------------------------------------------------------------------'

with open(COUN + INDUS + '.json', 'r') as fp:
    fundamentals = json.load(fp)

'---------------------------------------------------------------------------------------------------------------------------------'

defaultKey = ['beta', 'enterpriseToEbitda','enterpriseToRevenue','pegRatio','priceToBook','profitMargins','forwardPE']
financialData = ['currentRatio','debtToEquity','ebitdaMargins','quickRatio','profitMargins','operatingMargins']

for i in range(len(defaultKey)):
    item = defaultKey[i]

    housing = 'defaultKeyStatistics'

    long_name = []
    parameter = []
    
    for symbol in fundamentals:
        if len(fundamentals[symbol]) < 10:
            continue
        elif fundamentals[symbol][housing] is None:
            continue
        elif fundamentals[symbol][housing][item] is None:
            continue
        
        a = fundamentals[symbol][housing][item]
        b = fundamentals[symbol]['quoteType']['longName']
        long_name.append(b)
        parameter.append(a)
    
        if fundamentals is None:
            continue
    
    
    # long_name = list(dict.fromkeys(long_name))
    # parameter = list(dict.fromkeys(parameter))
    
    y_pos = np.arange(len(parameter))
    
    
    # Graphing Controls
    
    plt.barh(y_pos, parameter, color = Cs)
    plt.yticks(y_pos, long_name, rotation='horizontal')
    plt.tick_params(axis = 'y', labelsize = 4)
    plt.margins(0.2)
    plt.xlabel(item)
    plt.grid(b = True)
    plt.subplots_adjust(bottom=0.15)
    
    
    plt.tight_layout()
    plt.savefig(COUN + ' ' +  INDUS + ' ' + item + '.png', dpi=600)
    plt.show()
    
    # Export Data to csv
    Combined = pd.DataFrame({'long_name': long_name, item : parameter})
    Combined.to_csv(COUN + ' ' +  INDUS + ' ' + item + '.csv', index = False)













