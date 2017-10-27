# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 18:55:12 2017

@author: Connor
"""

import pandas as pd
import pdb
import re
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_html(r'filings.html')
df3 = df[3]

results = []
for x, row in df3.iterrows():
    i = 0
    if row[0] == 'Filed By:':
        filer = row[1]
    if row[0] == 'Filed Date:':
        date = row[1]            
    if row[0] == 'Accession No:':
        accNo = row[1]
    if row[0] == 'Description:':
        desc = row[1]
        i = 1
    if i == 1:
        results.append([filer, date, accNo, desc])    
        print(filer)        
            
dfFormatted = pd.DataFrame(results, columns = ['Filer', 'Date', 'Accession No.', 'Description'])

dfFormatted.to_csv(r'formatted_results.csv')
dfFormatted = pd.read_csv(r'formatted_results.csv')

uFilers = list(set(dfFormatted['Filer']))
uLFilers = [str.lower(x) for x in uFilers]
nukeFilers = []

for filingName in uLFilers:
    if 'nuclear' in filingName or 'uranium' in filingName:
        nukeFilers.append(filingName)
    #if 'uranium' in filingName:
    #    nukeFilers.append(phrase)
dfFormatted['datetime'] = pd.to_datetime(dfFormatted['Date'])
#dfFormatted = dfFormatted.sort_values('datetime', ascending=True)
uDates = list(set(dfFormatted['Date']))

dateFilings = []

for date in uDates:
    dfDate = dfFormatted[dfFormatted['Date'] == date]
    datetimeV = dfDate['datetime'].values[0]
    nFilings = len(dfDate)
    unFilings = len(list(set(dfDate['Filer'])))
    dateFilings.append([date, datetimeV, nFilings, unFilings])

dateFilings = pd.DataFrame(dateFilings, columns = ['Date', 'datetime', 'No of Filings', 'Unique Filers'])    
dateFilings = dateFilings.sort_values('datetime', ascending=True)    
ind = np.arange(0,len(dateFilings))
plt.style.use('ggplot')
plt.bar(ind, dateFilings['No of Filings'].values)
plt.xticks(ind, dateFilings['Date'].values, rotation= 'vertical')
plt.xlabel('Date')
plt.ylabel('Total Number of Daily Filings')
plt.title('Daily Number of Filings on RM18-1 (Resiliency NOPR)')
plt.tight_layout()
plt.savefig('dailyFilings.png', dpi=300)
plt.close()

ind = np.arange(0,len(dateFilings))
plt.bar(ind, dateFilings['Unique Filers'].values)
plt.xticks(ind, dateFilings['Date'].values, rotation= 'vertical')
plt.xlabel('Date')
plt.ylabel('Number of Daily Unique Filers')
plt.title('Daily Number of Unique Filers on RM18-1 (Resiliency NOPR)')
plt.tight_layout()
plt.savefig('dailyFilers.png', dpi=300)