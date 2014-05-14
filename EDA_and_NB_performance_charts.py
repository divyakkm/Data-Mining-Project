import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from IPython.core.display import HTML
from bokeh.plotting import *


# load data into pandas
INPUT_FILE = "C:\\data\\airline\\_dfTest2008.csv"

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

# change data types
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
df['accurate'] = 0
df.accurate[df.label == df.pred_label] = 1
df.accurate[df.label <> df.pred_label] = 0


df['dep_time'] = 0
df.dep_time[df.DepTime.isin(xrange(700, 1301))] = 1
df.dep_time[df.DepTime.isin(xrange(1300, 1801))] = 2
df.dep_time[df.DepTime.isin(xrange(1800, 2401))] = 3
df.dep_time[df.DepTime.isin(xrange(0, 701))] = 3

# compute accuracy rates
month_acc = dfMaster.groupby('Month').accurate.sum() / \
    dfMaster.groupby('Month').accurate.count()
df_month_acc = pd.DataFrame(month_acc, columns=[u'Month'])
# print df_month_acc

day_of_month_acc = dfMaster.groupby(
    'DayofMonth').accurate.sum() / dfMaster.groupby('DayofMonth').accurate.count()
df_day_of_month_acc = pd.DataFrame(day_of_month_acc, columns=[u'DayofMonth'])
# print df_day_of_month_acc

day_of_week_acc = dfMaster.groupby(
    'DayOfWeek').accurate.sum() / dfMaster.groupby('DayOfWeek').accurate.count()
df_day_of_week_acc = pd.DataFrame(day_of_week_acc, columns=[u'DayOfWeek'])
# print df_day_of_week_acc

unique_carrier_acc = dfMaster.groupby(
    'UniqueCarrier').accurate.sum() / dfMaster.groupby('UniqueCarrier').accurate.count()
df_unique_carrier_acc = pd.DataFrame(
    unique_carrier_acc, columns=[u'UniqueCarrier'])
# print df_unique_carrier_acc

tail_num_acc = dfMaster.groupby(
    'TailNum').accurate.sum() / dfMaster.groupby('TailNum').accurate.count()
df_tail_num_acc = pd.DataFrame(tail_num_acc, columns=[u'TailNum'])
# print df_tail_num_acc

origin_acc = dfMaster.groupby('Origin').accurate.sum() / \
    dfMaster.groupby('Origin').accurate.count()
df_origin_acc = pd.DataFrame(origin_acc, columns=[u'Origin'])
# print df_origin_acc

dest_acc = dfMaster.groupby('Dest').accurate.sum() / \
    dfMaster.groupby('Dest').accurate.count()
df_dest_acc = pd.DataFrame(dest_acc, columns=[u'Dest'])
# print df_dest_acc

dep_time_acc = dfMaster.groupby('dep_time').accurate.sum() / \
    dfMaster.groupby('dep_time').accurate.count()
df_dep_time_acc = pd.DataFrame(dep_time_acc, columns=[u'dep_time'])
# print dep_time_acc


# compute proportion of delays by each variable

month_delays = dfMaster.groupby(
    'Month').label.sum() / dfMaster.groupby('Month').label.count()
df_month_delays = pd.DataFrame(month_delays, columns=[u'Month'])
# print df_month_delays

day_of_month_delays = dfMaster.groupby(
    'DayofMonth').label.sum() / dfMaster.groupby('DayofMonth').label.count()
df_day_of_month_delays = pd.DataFrame(
    day_of_month_delays, columns=[u'DayofMonth'])
# print df_day_of_month_delays

day_of_week_delays = dfMaster.groupby(
    'DayOfWeek').label.sum() / dfMaster.groupby('DayOfWeek').label.count()
df_day_of_week_delays = pd.DataFrame(
    day_of_week_delays, columns=[u'DayOfWeek'])
# print df_day_of_week_delays

unique_carrier_delays = dfMaster.groupby(
    'UniqueCarrier').label.sum() / dfMaster.groupby('UniqueCarrier').label.count()
df_unique_carrier_delays = pd.DataFrame(
    unique_carrier_delays, columns=[u'UniqueCarrier'])
# print df_unique_carrier_delays

tail_num_delays = dfMaster.groupby(
    'TailNum').label.sum() / dfMaster.groupby('TailNum').label.count()
df_tail_num_delays = pd.DataFrame(tail_num_delays, columns=[u'TailNum'])
# print df_tail_num_delays

origin_delays = dfMaster.groupby(
    'Origin').label.sum() / dfMaster.groupby('Origin').label.count()
df_origin_delays = pd.DataFrame(origin_delays, columns=[u'Origin'])
# print df_origin_delays

dest_delays = dfMaster.groupby(
    'Dest').label.sum() / dfMaster.groupby('Dest').label.count()
df_dest_delays = pd.DataFrame(dest_delays, columns=[u'Dest'])
# print df_dest_delays

dep_time_delays = dfMaster.groupby(
    'dep_time').label.sum() / dfMaster.groupby('dep_time').label.count()
df_dep_time_delays = pd.DataFrame(dep_time_delays, columns=[u'dep_time'])
# print df_dep_time_delays


# bar charts to see where delays are more likely
df_day_of_month_delays.plot(kind='bar', color='grey', stacked=True)

# df_day_of_week_delays.plot(kind='bar', color='grey', stacked=True)

# df_unique_carrier_delays.plot(kind='bar', color='grey', stacked=True)

# df_tail_num_delays.plot(kind='bar', color='grey', stacked=True)

# df_origin_delays.plot(kind='bar', color='grey', stacked=True)

# df_dest_delays.plot(kind='bar', color='grey', stacked=True)

# df_dep_time_delays.plot(kind='bar', color='grey', stacked=True)

# df_month_delays.plot(kind='bar', color='grey', stacked=True)

plt.show()


# plot bar charts for accuracy measures
# df_month_acc.plot(kind='bar', color='grey', background_fill="#EAEAF2")

# df_day_of_month_acc.plot(
# kind='bar', color='grey', background_fill="#EAEAF2")

# df_day_of_week_acc.plot(kind='bar', color='grey')

# df_unique_carrier_acc.plot(kind='bar', color='grey')

# df_tail_num_acc.plot(kind='bar', color='grey')

# df_origin_acc.plot(kind='bar', color='grey')

# df_dest_acc.plot(kind='bar', color='grey')

# df_dep_time_acc.plot(kind='bar', color='grey')

plt.show()
