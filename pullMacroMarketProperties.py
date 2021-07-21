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

fundamentals = {}
for symbol in companylist:
    fundamentals[symbol] = get_json("https://finance.yahoo.com/quote/" + symbol)

# stock_data = download(list(companylist))

fundamentals = {k:v for k,v in fundamentals.items() if not '.' in k}

# gh = pd.concat({k: pd.DataFrame(v).T for k, v in fundamentals.items()}, axis=0)

long_name = []
parameter = []

for symbol in fundamentals:
    if len(fundamentals[symbol]) < 10:
        continue
    elif fundamentals[symbol]['defaultKeyStatistics'] is None:
        continue
    elif fundamentals[symbol]['defaultKeyStatistics']['priceToBook'] is None:
        continue
    
    a = fundamentals[symbol]['defaultKeyStatistics']['priceToBook']
    b = fundamentals[symbol]['quoteType']['longName']
    long_name.append(b)
    parameter.append(a)

    if fundamentals is None:
        continue

# long_name = list(dict.fromkeys(long_name))
# parameter = list(dict.fromkeys(parameter))

y_pos = np.arange(len(parameter))


plt.barh(y_pos, parameter)
plt.yticks(y_pos, long_name, rotation='horizontal')
# Pad margins so that markers don't get clipped by the axes
plt.margins(0.2)
plt.xlabel('priceToBook')
plt.grid(b = True)
# Tweak spacing to prevent clipping of tick-labels
plt.subplots_adjust(bottom=0.15)


plt.show()


































