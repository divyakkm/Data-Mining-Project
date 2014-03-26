from __future__ import division

# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#!/usr/bin/env python

"""This file contains the code for the Data Mining Class. It uses the Airline dataset <<add link>>"""

__author__ = ""
__email__ = ""
__status__ = ""

# <codecell>

#  Importing various modules

import matplotlib.pyplot as plt
import numpy as np
from pylab import figure, show
from pandas import DataFrame, Series
import pandas as pd
import csv
import os
import statsmodels.formula.api as smf
import scipy.stats as stats
import statsmodels.api as sm

# <codecell>

#  Setting global constants. Please initialize this before running the code

TRAINING_LINE_NUMBER = 100000 # Number of lines to be read from the huge file, set to total file length while running for entire file
INPUT_FILE_PATH="C:\\data\\airline\\" # Path of the folder where you have placed your files
SKIP_FIRST_LINE = True # To skip the first line, as its the header
YEARS = ['2008'] # Add more years in this list and add the files in the INPUT_FILE_PATH

# <codecell>

# Setting the dataframes for Airline, Plane and Carriers

try:
    path = "C:\\data\\airline\\plane-data.csv"
    dfPlane = pd.read_csv(path)
    path = 'C:\\data\\airline\\airports.csv'
    dfAirport = pd.read_csv(path)
    path = 'C:\\data\\airline\\carriers.csv'
    dfCarrier = pd.read_csv(path)
except Exception as e:
    print "Supplemental Data Import failed", e

# <codecell>

# Readng the main file in a Pandas dataframe

try:
    for year in YEARS:
        path = os.path.join(INPUT_FILE_PATH, '%d.csv' % int(year))
        dfMaster = pd.read_csv(path, nrows=TRAINING_LINE_NUMBER,skiprows=0)
except Exception as e:
    print "Supplemental Data Import failed", e
dfMaster.head()

# <codecell>

dfMaster.fillna(0,inplace=True)

# <codecell>

# TODO: Do this for other dataframes as well

#  Convert all columns to respective datatypes

dfMaster['Year'] = dfMaster['Year'].astype('int')
dfMaster['Month'] = dfMaster['Month'].astype('int')
dfMaster['DayofMonth'] = dfMaster['DayofMonth'].astype('int')
dfMaster['DayOfWeek'] = dfMaster['DayOfWeek'].astype('int')
dfMaster['DepTime'] = dfMaster['DepTime'].astype('int')
dfMaster['CRSDepTime'] = dfMaster['CRSDepTime'].astype('int')
dfMaster['ArrTime'] = dfMaster['ArrTime'].astype('int')
dfMaster['CRSArrTime'] = dfMaster['CRSArrTime'].astype('int')
dfMaster['FlightNum'] = dfMaster['FlightNum'].astype('int')
dfMaster['ActualElapsedTime'] = dfMaster['ActualElapsedTime'].astype('int')
dfMaster['CRSElapsedTime'] = dfMaster['CRSElapsedTime'].astype('int')
dfMaster['AirTime'] = dfMaster['AirTime'].astype('int')
dfMaster['ArrDelay'] = dfMaster['ArrDelay'].astype('int')
dfMaster['DepDelay'] = dfMaster['DepDelay'].astype('int')
dfMaster['Distance'] = dfMaster['Distance'].astype('int')
dfMaster['TaxiIn'] = dfMaster['TaxiIn'].astype('int')
dfMaster['TaxiOut'] = dfMaster['TaxiOut'].astype('int')
dfMaster['Cancelled'] = dfMaster['Cancelled'].astype('int')
dfMaster['Diverted'] = dfMaster['Diverted'].astype('int')
print dfMaster.columns

# <codecell>

# for col in dfMaster.columns:
#     print 'dfMaster[\'',col,'\'] = dfMaster[\'',col,'\'].astype(\'int\')'

# <codecell>

results = sm.OLS.from_formula('DepDelay ~ ArrDelay', dfMaster).fit()
print results.summary()

# <codecell>

intercept, slope = results.params
r2 = results.rsquared
print slope, intercept, r2

plt.plot(dfMaster['DepDelay'], dfMaster['ArrDelay'], 'bo')
x = np.array([min(dfMaster['ArrDelay']), max(dfMaster['ArrDelay'])])
y = intercept + slope * x
plt.plot(x, y, 'r-')
plt.show()


from statsmodels.stats.anova import anova_lm

anova_lm(results)

