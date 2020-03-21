#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 11:34:48 2020
Miriam Stevens
@author: steve276

Code from tutorial Time Series Analysis with Pandas
"""
import pandas as pd
import numpy as np
from pandas import Series, DataFrame, Panel
pd.set_option('display.max_rows', 15)   # this limits maximum number of rows

pd.__version__    # check version of pandas is > 0.8.

!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii
# download file at the given link without opening the file

ao = np.loadtxt('monthly.ao.index.b50.current.ascii')

ao[0:2]  # show the 0th and 1st lines

ao.shape # describes shape of file: 842x3

#create range of dates for time series
dates = pd.date_range('1950-01', periods=ao.shape[0], freq='M')

dates.shape  # check number of dates

AO = Series(ao[:,2], index=dates)  #create series with dates as index
AO

AO.plot()                        #plot all the data
AO['1980':'1990'].plot()         #plot some of the data
AO['1980-05':'1981-03'].plot()
AO['2010':'2020'].plot() 


#reference specific values
AO[120]                          #by number

AO['1960-01']                    #by index

AO[841]                          #842th (last) entry

AO['1960']

AO[AO > 0]                       #all but the first one
AO[0:2]

#download NAO dataset
!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii

#create time series
nao = np.loadtxt('norm.nao.monthly.b5001.current.ascii')     #nao.shape = (841x3)
dates_nao = pd.date_range('1950-01', periods=nao.shape[0], freq='M')
NAO = Series(nao[:,2], index=dates_nao)

NAO.index   #nao has 1 less line than ao

#create DataFrame
aonao = DataFrame({'AO': AO, 'NAO': NAO})
aonao   #view dataframe
#the different lenghs results in the 842nd entry of NAO being NaN

aonao.plot(subplots=True)

aonao.head()     #view the first few entries
aonao['NAO']     #view only NAO portion of DataFrame
aonao.NAO        #view NAO portion as a method of the DataFrame variable, if the name of the variable is a valid python name

#add a column to the dataframe
aonao['Diff'] = aonao['AO'] - aonao['NAO']
aonao.head()

#delete the new column
del aonao['Diff']
aonao.tail()

#simple slicing
aonao['1981-01':'1981-03']

#complicated sliciing
import datetime
aonao.loc[(aonao.AO > 0) & (aonao.NAO < 0)
           & (aonao.index > datetime.datetime(1980,1,1))
           & (aonao.index < datetime.datetime(1989,1,1)),
           'NAO'].plot(kind='barh')
# chooses all NAO values for which AO is pos and NAO is neg and are between 1980 and 1989

#obtaining statistical information from elements of DataFrame. Default is column-wise
aonao.mean()

aonao.max()
aonao.min()

#row-wise statistics
aonao.mean(1)

#describe DataFrame elements
aonao.describe()

#Resampling to different time frequency
AO_mm = AO.resample("A").mean()         #resamples AO to get Annual("A") mean
AO_mm.plot(style='g--')

AO_mm = AO.resample("A").median()
AO_mm.plot()

AO_mm = AO.resample("3A").apply(np.max)    #resample time frequency is every 3 years, and finds max over timeframe
AO_mm.plot()

AO_mm = AO.resample("A").apply(['mean', np.min, np.max]) 
AO_mm['1900':'2020'].plot(subplots=True)
AO_mm['1900':'2020'].plot()

AO_mm

#moving(rolling) statistics
aonao.rolling(window=12, center=False).mean().plot(style='-g')   #moving average

aonao.AO.rolling(window=120).corr(other=aonao.NAO).plot(style='-g')   #moving correlation

aonao.corr()






