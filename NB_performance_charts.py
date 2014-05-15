# This code builds some exploratory graphs to see how prediction accuracy
# of the Naive Bayes model varies by each variable used to build the model.


#  Importing various modules to  build graphs
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
from pylab import figure, show
from pandas import DataFrame, Series
import pandas as pd
import csv
import os
from bokeh.plotting import *
import seaborn as sns
from bokeh.objects import ColumnDataSource, Range1d
from math import floor
import bokeh as bokeh
import seaborn as sns
sns.set_context("talk")


# load 2008 test data into pandas
INPUT_FILE = "C:\\Users\\user\\Desktop\\INFO_290T\\Final Project\Visualizations\\SFO_OAK_data\\_dfTest2008.csv"

SKIP_FIRST_LINE = True

master = []
print "Reading into Pandas frame..."
try:
    dfPart = pd.read_csv(INPUT_FILE, skiprows=0, usecols=[  # nrows = 2000
                         u'Year', u'Month', u'DayofMonth', u'DayOfWeek', u'UniqueCarrier',
                         u'DepTime', u'TailNum', u'Origin', u'Dest', u'label', u'pred_label'
                         ])
    print len(dfPart)
    master.append(dfPart)
except Exception as e:
    print "Data import failed", e


dfMaster = pd.concat(master, ignore_index=True)
print "Total length: ", len(dfMaster)

# change data types to integers
dfMaster['Year'] = dfMaster['Year'].astype('int')
dfMaster['Month'] = dfMaster['Month'].astype('int')
dfMaster['DayofMonth'] = dfMaster['DayofMonth'].astype('int')
dfMaster['DepTime'] = dfMaster['DepTime'].astype('int')
dfMaster['UniqueCarrier'] = dfMaster['UniqueCarrier'].astype('int')
dfMaster['TailNum'] = dfMaster['TailNum'].astype('int')
dfMaster['Origin'] = dfMaster['Origin'].astype('int')
dfMaster['Dest'] = dfMaster['Dest'].astype('int')
dfMaster['label'] = dfMaster['label'].astype('int')
dfMaster['pred_label'] = dfMaster['pred_label'].astype('int')


df = dfMaster
print "Appneding new variables..."

# create a binary variable that indicates accuracy of prediction
# for each record
df['accurate'] = 0
df.accurate[df.label == df.pred_label] = 1
df.accurate[df.label <> df.pred_label] = 0


# discretize time of day variable and create a categorical variable
# that captures morning (from 7 am to 1 pm), afternoon (1 pm to 6 pm),
# and night (from 6 pm to 7 am)
df['dep_time'] = 0
df.dep_time[df.DepTime.isin(xrange(700, 1301))] = 1
df.dep_time[df.DepTime.isin(xrange(1300, 1801))] = 2
df.dep_time[df.DepTime.isin(xrange(1800, 2401))] = 3
df.dep_time[df.DepTime.isin(xrange(0, 701))] = 3

# compute accuracy rates for each variable
month_acc = dfMaster.groupby('Month').accurate.sum() / \
    dfMaster.groupby('Month').accurate.count()
df_month_acc = pd.DataFrame(month_acc, columns=[u'Accuracy'])


day_of_month_acc = dfMaster.groupby(
    'DayofMonth').accurate.sum() / dfMaster.groupby('DayofMonth').accurate.count()
df_day_of_month_acc = pd.DataFrame(day_of_month_acc, columns=[u'Accuracy'])

day_of_week_acc = dfMaster.groupby(
    'DayOfWeek').accurate.sum() / dfMaster.groupby('DayOfWeek').accurate.count()
df_day_of_week_acc = pd.DataFrame(day_of_week_acc, columns=[u'Accuracy'])

unique_carrier_acc = dfMaster.groupby(
    'UniqueCarrier').accurate.sum() / dfMaster.groupby('UniqueCarrier').accurate.count()
df_unique_carrier_acc = pd.DataFrame(
    unique_carrier_acc, columns=[u'Accuracy'])

tail_num_acc = dfMaster.groupby(
    'TailNum').accurate.sum() / dfMaster.groupby('TailNum').accurate.count()
df_tail_num_acc = pd.DataFrame(tail_num_acc, columns=[u'Accuracy'])

origin_acc = dfMaster.groupby('Origin').accurate.sum() / \
    dfMaster.groupby('Origin').accurate.count()
df_origin_acc = pd.DataFrame(origin_acc, columns=[u'Accuracy'])

dest_acc = dfMaster.groupby('Dest').accurate.sum() / \
    dfMaster.groupby('Dest').accurate.count()
df_dest_acc = pd.DataFrame(dest_acc, columns=[u'Accuracy'])

dep_time_acc = dfMaster.groupby('dep_time').accurate.sum() / \
    dfMaster.groupby('dep_time').accurate.count()
df_dep_time_acc = pd.DataFrame(dep_time_acc, columns=[u'Accuracy'])


# compute proportion of delays by each variable
month_delays = dfMaster.groupby(
    'Month').label.sum() / dfMaster.groupby('Month').label.count()
df_month_delays = pd.DataFrame(month_delays, columns=[u'Accuracy'])

day_of_month_delays = dfMaster.groupby(
    'DayofMonth').label.sum() / dfMaster.groupby('DayofMonth').label.count()
df_day_of_month_delays = pd.DataFrame(
    day_of_month_delays, columns=[u'Accuracy'])

day_of_week_delays = dfMaster.groupby(
    'DayOfWeek').label.sum() / dfMaster.groupby('DayOfWeek').label.count()
df_day_of_week_delays = pd.DataFrame(
    day_of_week_delays, columns=[u'Accuracy'])

unique_carrier_delays = dfMaster.groupby(
    'UniqueCarrier').label.sum() / dfMaster.groupby('UniqueCarrier').label.count()
df_unique_carrier_delays = pd.DataFrame(
    unique_carrier_delays, columns=[u'Accuracy'])

tail_num_delays = dfMaster.groupby(
    'TailNum').label.sum() / dfMaster.groupby('TailNum').label.count()
df_tail_num_delays = pd.DataFrame(tail_num_delays, columns=[u'Accuracy'])

origin_delays = dfMaster.groupby(
    'Origin').label.sum() / dfMaster.groupby('Origin').label.count()
df_origin_delays = pd.DataFrame(origin_delays, columns=[u'Accuracy'])

dest_delays = dfMaster.groupby(
    'Dest').label.sum() / dfMaster.groupby('Dest').label.count()
df_dest_delays = pd.DataFrame(dest_delays, columns=[u'Accuracy'])

dep_time_delays = dfMaster.groupby(
    'dep_time').label.sum() / dfMaster.groupby('dep_time').label.count()
df_dep_time_delays = pd.DataFrame(dep_time_delays, columns=[u'Accuracy'])


############################################### BUILD GRAPHS ###########################################

# build accuracy by day of month variable
dfPlot = df_day_of_month_delays
dfPlot.reset_index(inplace=True)
dfPlot.columns
plt.show()
fig = plt.figure()
fig.suptitle('Accuracy by Day of Month', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.95)
ax.set_xlabel('Day of Month')
ax.set_ylabel('Accuracy')
ax.bar(dfPlot['DayofMonth'], dfPlot['Accuracy'], label="Label")
plt.xticks(dfPlot['DayofMonth'], xrange(1, 32), rotation=45)
plt.show()

# build accuracy by month variable
dfPlot = df_month_delays
dfPlot.reset_index(inplace=True)
dfPlot.columns
plt.show()
fig = plt.figure()
fig.suptitle('Accuracy by Month', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.95)
ax.set_xlabel('Month')
ax.set_ylabel('Accuracy')
ax.bar(dfPlot['Month'], dfPlot['Accuracy'], label="Label")
plt.xticks(dfPlot['Month'], xrange(1, 32), rotation=45)
plt.show()

# build accuracy by day of week variable
dfPlot = df_day_of_week_delays
dfPlot.reset_index(inplace=True)
dfPlot.columns
plt.show()
fig = plt.figure()
fig.suptitle('Accuracy by day of week', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.95)
ax.set_xlabel('Day of Week')
ax.set_ylabel('Accuracy')
ax.bar(dfPlot['DayOfWeek'], dfPlot['Accuracy'], label="Label")
plt.xticks(dfPlot['DayOfWeek'], xrange(1, 32), rotation=45)
plt.show()

# build accuracy by unique carrier variable
dfPlot = df_unique_carrier_delays
dfPlot.reset_index(inplace=True)
dfPlot.columns
plt.show()
fig = plt.figure()
fig.suptitle('Accuracy by unique carrier', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.95)
ax.set_xlabel('Unique carrier')
ax.set_ylabel('Accuracy')
ax.bar(dfPlot['UniqueCarrier'], dfPlot['Accuracy'], label="Label")
plt.xticks(dfPlot['UniqueCarrier'], xrange(1, 32), rotation=45)
plt.show()

# build accuracy by tail number variable
dfPlot = df_tail_num_delays
dfPlot.reset_index(inplace=True)
dfPlot.columns
plt.show()
fig = plt.figure()
fig.suptitle('Accuracy by tail number', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.95)
ax.set_xlabel('Tail number')
ax.set_ylabel('Accuracy')
ax.bar(dfPlot['TailNum'], dfPlot['Accuracy'], label="Label")
plt.xticks(dfPlot['TailNum'], xrange(1, 32), rotation=45)
plt.show()

# build accuracy by origin variable
dfPlot = df_origin_delays
dfPlot.reset_index(inplace=True)
dfPlot.columns
plt.show()
fig = plt.figure()
fig.suptitle('Accuracy by origin', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.95)
ax.set_xlabel('Origin airport')
ax.set_ylabel('Accuracy')
ax.bar(dfPlot['Origin'], dfPlot['Accuracy'], label="Label")
plt.xticks(dfPlot['Origin'], xrange(1, 32), rotation=45)
plt.show()

# build accuracy by destination variable
dfPlot = df_dest_delays
dfPlot.reset_index(inplace=True)
dfPlot.columns
plt.show()
fig = plt.figure()
fig.suptitle('Accuracy by destination', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.95)
ax.set_xlabel('Destination airport')
ax.set_ylabel('Accuracy')
ax.bar(dfPlot['Dest'], dfPlot['Accuracy'], label="Label")
plt.xticks(dfPlot['Dest'], xrange(1, 32), rotation=45)
plt.show()

# build accuracy by departure time variable
dfPlot = df_dep_time_delays
dfPlot.reset_index(inplace=True)
dfPlot.columns
plt.show()
fig = plt.figure()
fig.suptitle('Accuracy by departure time', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
fig.subplots_adjust(top=0.95)
ax.set_xlabel('Departure time')
ax.set_ylabel('Accuracy')
ax.bar(dfPlot['dep_time'], dfPlot['Accuracy'], label="Label")
plt.xticks(dfPlot['dep_time'], xrange(1, 32), rotation=45)
plt.show()
