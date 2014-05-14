from __future__ import division
import numpy as np
import pandas as pd
import sklearn
from sklearn.naive_bayes import *
from sklearn.metrics import *
import os
import cPickle

# Setting up constants
print "Setting constants..."

TRAINING_LINE_NUMBER = 100
YEARS = ['2008', '2007']
# INPUT_FILE_PATH = "/home/dmenghani/python/"  # Unix path
INPUT_FILE_PATH = "C:\\data\\airline\\"  # Windows path
# YEARS = ['2008']

SKIP_FIRST_LINE = True  # To skip the first line, as its the header

master = []
print "Reading into Pandas frame..."
try:
    for year in YEARS:
        path = os.path.join(INPUT_FILE_PATH, '%d.csv' % int(year))
        print path
        dfPart = pd.read_csv(
            path, nrows=TRAINING_LINE_NUMBER, skiprows=0, usecols=[
                u'Year', u'Month', u'DayofMonth', u'DayOfWeek', u'UniqueCarrier',
                u'DepTime', u'TailNum', u'Origin', u'Dest', u'DepDelay', u'Cancelled'
            ])
        dfPart = dfPart[dfPart['Cancelled'] == 0]
        print len(dfPart)
        master.append(dfPart)
except Exception as e:
    print "Supplemental Data Import failed", e

dfMaster = pd.concat(master, ignore_index=True)
print "Total length - ", len(dfMaster)


dfMaster.fillna(0, inplace=True)
dfMaster['Year'] = dfMaster['Year'].astype('int')
dfMaster['Month'] = dfMaster['Month'].astype('int')
dfMaster['DayofMonth'] = dfMaster['DayofMonth'].astype('int')
dfMaster['DayOfWeek'] = dfMaster['DayOfWeek'].astype('int')
dfMaster['DepTime'] = dfMaster['DepTime'].astype('int')
dfMaster['DepDelay'] = dfMaster['DepDelay'].astype('int')

print "Length of pandas frame - ", len(dfMaster)
print "Dataframe columns - ", dfMaster.columns

df = dfMaster

print "Calculating classification label..."
df['label'] = 0
df.label[df.DepDelay >= 15] = 1
df.label[df.DepDelay < 15] = 0
del df['DepDelay']

print "Converting categorical data to numeric..."
for col in set(df.columns):
# print col, train[col].dtype
    if df[col].dtype == np.dtype('object'):
        print "Converting...", col
        if col == 'TailNum':
            s = np.unique(df[col].values)
            TailNum = pd.Series([x[0] for x in enumerate(s)], index=s)
#             print TailNum
        if col == 'UniqueCarrier':
            s = np.unique(df[col].values)
            UniqueCarrier = pd.Series([x[0] for x in enumerate(s)], index=s)
#             print UniqueCarrier
        if col == 'Dest':
            s = np.unique(df[col].values)
            Dest = pd.Series([x[0] for x in enumerate(s)], index=s)
#             print Dest
        if col == 'Origin':
            s = np.unique(df[col].values)
            Origin = pd.Series([x[0] for x in enumerate(s)], index=s)
#             print Origin


def getTailNum(inTailNum):
#     print "In...",type(inTailNum)
    out = []
    for x, y in inTailNum.iteritems():
#         print "x,y, out",x,y,TailNum.get_value(y)
        out.append(TailNum.get_value(y) + 1)
#     print "final out", out
    return out


def getDest(inDest):
    out = []
    for x, y in inDest.iteritems():
        out.append(Dest.get_value(y) + 1)
    return out


def getOrigin(inOrign):
    out = []
    for x, y in inOrign.iteritems():
        out.append(Origin.get_value(y) + 1)
    return out


def getCarrier(inCarrier):
    out = []
    for x, y in inCarrier.iteritems():
        out.append(UniqueCarrier.get_value(y) + 1)
    return out

df['TailNum'] = getTailNum(df['TailNum'])
print "TailNum completed."

df['Dest'] = getDest(df['Dest'])
print "Dest completed."

df['UniqueCarrier'] = getCarrier(df['UniqueCarrier'])
print "UniqueCarrier completed."

df['Origin'] = getOrigin(df['Origin'])
print "Origin completed."

print "Conversion to numeric completed."

print "Pickling converted data..."
df.to_pickle(INPUT_FILE_PATH + "\df.pkl")

print "Begin classification...75% training, 25% testing, randomly chosen"
arget_names = np.array(['Delayed', 'Not Delayed'])
# add columns to your data frame
df['is_train'] = np.random.uniform(0, 1, len(df)) <= 0.75
# define training and test sets
train = df[df['is_train'] == True]
test = df[df['is_train'] == False]
trainTargets = np.array(train['label']).astype(int)
testTargets = np.array(test['label']).astype(int)
features = df.columns[0:9]
print "Model fitting and prediction started..."
gnb = MultinomialNB()
# train model
y_gnb = gnb.fit(train[features], trainTargets).predict(test[features])
print "Classification completed."
print "Calculating metrcs..."
test['pred_label'] = y_gnb
test.head()
acc = zip(test['label'], test['pred_label'])
match_count = 0
for i in acc:
    if i[0] == - i[1]:
        match_count += 1
print "Matches - ", match_count
print "Total length - ", len(acc)
print "Accuracy:", float(match_count) / len(acc)
