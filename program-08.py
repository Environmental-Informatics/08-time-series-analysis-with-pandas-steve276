#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 14:17:40 2020
Miriam Stevens
@author: steve276

This program uses the pandas module to read USGS stremflow data into a DataFrame
and matplotlib to generate three summary plots.
"""

import pandas as pd
from pandas import Series, DataFrame, Panel
import numpy as np
import matplotlib.pyplot as plt


#data = pd.read_table('WabashRiver_DailyDischarge_20150317-20160324.txt',\
#              skip_blank_lines=True, header=0, infer_datetime_format=True,\
#              skiprows=26)

data = pd.read_table('WabashRiver_DailyDischarge_20150317-20160324.txt',\
              skip_blank_lines=True, header=None, infer_datetime_format=True,\
              skiprows=26)

type(data)   #confirm data type is DataFrame

data[0:2]

#convert DataFrame to array
df = pd.DataFrame(data)      
data_array = df.values

#check array shape and size
data_array.shape
type(data_array)

dates = pd.date_range('2015-03-17 00:00', periods=data_array.shape[0], freq='15T')

sf_values = data_array[:,4]

#create series of datetime elements and streamflow values
SF = Series(sf_values, index=dates)

#generate plots for submission

#Daily average streamflow
SF_daily = SF.resample('D').sum()    #resample to get total daily streamflow

plt.plot(SF_daily)
plt.xlabel('year-month')
plt.ylabel('cfs')
plt.savefig('Daily-streamflow-plot.pdf', bbox_inches='tight')



#10 days with highest flow on same time axis as full daily record
top_10 = SF_daily.nlargest(10)          #identify the 10 days with highest flow

plt.figure(figsize=(8,6))
plt.scatter(top_10.index,top_10, marker='D', facecolors='none', edgecolors='k')
plt.xlabel('year-month')
plt.ylabel('cfs')
#plt.plot(SF_daily, 'w')
plt.savefig('Highest-streamflow-days.pdf', bbox_inches='tight')


#Monthly average streamflow
SF_monthly = SF_daily.resample('M').mean()    #resample to get monthly average streamflow

plt.plot(SF_monthly)
plt.xlabel('year-month')
plt.ylabel('cfs')
plt.savefig('Monthly-avg-streamflow-plot.pdf', bbox_inches='tight')


