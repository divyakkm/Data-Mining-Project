from __future__ import division

#
# Naive Bayes.py
# Author: Divyakumar Menghani
# Description: This code  reads the dataset into pandas dataframes, builds a Naive Bayes Classifier, predicts labels for a subset of data. It also calculates metrics such as precision/recall/accuracy and F-Score after classification. The output is dumped in pickle files which are used later for visualization
#

import pickle
import sklearn
from sklearn.naive_bayes import *
import pandas as pd
import numpy as np
from sklearn import *
import os
from sklearn.metrics import *
from sklearn import metrics, preprocessing
from sklearn import svm, naive_bayes, neighbors, tree

#
# Function: createPickle()
# Description: This function will create a pickle file.
# Input: data structure that you want to pickle
# Output: a pickle file for the data structure. The file is stored in the
# same path the code is running from
#


def createPickle(data, filename):
    with open(filename, 'wb') as f:
            pickle.dump(data, f)
    print "Pickled", filename


# Global constants for this code
print "Setting constants..."

TRAINING_LINE_NUMBER = 8000000  # Number of lines to be read from input files
# List of years for training and testing
YEARS = ['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008']
INPUT_FILE_PATH = "/home/dmenghani/python/"  # Unix path
# INPUT_FILE_PATH = "C:\\data\\airline\\"  # Windows path
SKIP_FIRST_LINE = True  # To skip the first line, as its the header

# Creating the master data frame from all years.
master = []
print "Reading into Pandas frame..."
try:
    for year in YEARS:
        path = os.path.join(INPUT_FILE_PATH, '%d.csv' % int(year))
        print "\n", path
        dfPart = pd.read_csv(
            path, nrows=TRAINING_LINE_NUMBER, skiprows=0, usecols=[
                u'Year',
                u'Month',
                u'DayofMonth',
                u'DayOfWeek',
                u'UniqueCarrier',
                u'DepTime',
                u'TailNum',
                u'Origin',
                u'Dest',
                u'DepDelay',
                # u'ArrDelay',
                u'Cancelled',
                #                 u'ArrTime',
                #                 u'ArrDelay',
                #                 u'Distance'
            ])
        print len(dfPart)
        # Removing cancelled flights from each year
        dfPart = dfPart[dfPart['Cancelled'] == 0]
        rows = np.random.choice(
            np.random.permutation(dfPart.index.values), len(dfPart) // 3, replace=False)  # 33% sampling of training data
        print rows
        sampled_dfPart = dfPart.ix[rows]
        sampled_dfPart = dfPart
        master.append(sampled_dfPart)
        print
except Exception as e:
    print "Supplemental Data Import failed", e

# Building the master frame by concating it for all years
dfMaster = pd.concat(master, ignore_index=True)
master = []
dfPart = []

print "Total length - ", len(dfMaster)
del dfMaster['Cancelled']  # Column not needed

dfMaster.fillna(0, inplace=True)

# Converting to appropriate datatypes for numeric cols.
dfMaster['Year'] = dfMaster['Year'].astype('int')
dfMaster['Month'] = dfMaster['Month'].astype('int')
dfMaster['DayofMonth'] = dfMaster['DayofMonth'].astype('int')
dfMaster['DayOfWeek'] = dfMaster['DayOfWeek'].astype('int')
dfMaster['DepTime'] = dfMaster['DepTime'].astype('int')
dfMaster['DepDelay'] = dfMaster['DepDelay'].astype('int')

df = dfMaster

# Since we dont have a classification label in the data, we are creating
# one. Threshold of 5mins was chosen.
print "Calculating classification label..."
df['label'] = 0
df.label[df.DepDelay >= 5] = 1
df.label[df.DepDelay < 5] = 0
print "Actual delayed flights  -", np.sum(dfMaster['label']) / len(dfMaster['label'])

del df['DepDelay']

print "Dataframe shape - ", df.shape
print "Columns -", df.columns

# Converting categorical data to numeric for cols - TailNum,
# UniqueCarrier, Dest, Origin
print "Converting categorical data to numeric..."
for col in set(df.columns):
    if df[col].dtype == np.dtype('object'):
        print "Converting...", col
        if col == 'TailNum':
            s = np.unique(df[col].values)
            TailNum = pd.Series([x[0] for x in enumerate(s)], index=s)
        if col == 'UniqueCarrier':
            s = np.unique(df[col].values)
            UniqueCarrier = pd.Series([x[0] for x in enumerate(s)], index=s)
        if col == 'Dest':
            s = np.unique(df[col].values)
            Dest = pd.Series([x[0] for x in enumerate(s)], index=s)
        if col == 'Origin':
            s = np.unique(df[col].values)
            Origin = pd.Series([x[0] for x in enumerate(s)], index=s)

# Creating Pickle files for the list containing key-value pairs
createPickle(Dest, 'Dest_2008.pkl')
createPickle(Origin, 'Origin_2008.pkl')
createPickle(UniqueCarrier, 'UniqueCarrier_2008.pkl')
createPickle(TailNum, 'TailNum_2008.pkl')
print "Pickle completed."

#
# Function: getTailNum()
# Description: This function will convert the input categorical value to corresponding numeric key.
# Input: categorical value you want to convert
# Output: a numeric value corresponding to the value passed. It uses the list created previously for lookup.
#


def getTailNum(inTailNum):
    out = []
    for x, y in inTailNum.iteritems():
        out.append(TailNum.get_value(y))
    return out

#
# Function: getDest()
# Description: This function will convert the input categorical value to corresponding numeric key.
# Input: categorical value you want to convert
# Output: a numeric value corresponding to the value passed. It uses the list created previously for lookup.
#


def getDest(inDest):
    out = []
    for x, y in inDest.iteritems():
        out.append(Dest.get_value(y))
    return out

#
# Function: getOrigin()
# Description: This function will convert the input categorical value to corresponding numeric key.
# Input: categorical value you want to convert
# Output: a numeric value corresponding to the value passed. It uses the list created previously for lookup.
#


def getOrigin(inOrign):
    out = []
    for x, y in inOrign.iteritems():
        out.append(Origin.get_value(y))
    return out

#
# Function: getCarrier()
# Description: This function will convert the input categorical value to corresponding numeric key.
# Input: categorical value you want to convert
# Output: a numeric value corresponding to the value passed. It uses the list created previously for lookup.
#


def getCarrier(inCarrier):
    out = []
    for x, y in inCarrier.iteritems():
        out.append(UniqueCarrier.get_value(y))
    return out

# Converting TailNum
df['TailNum'] = getTailNum(df['TailNum'])
print "TailNum completed."

# Converting UniqueCarrier
df['UniqueCarrier'] = getCarrier(df['UniqueCarrier'])
print "UniqueCarrier completed."

# Converting Dest
df['Dest'] = getDest(df['Dest'])
print "Dest completed."

# Converting Origin
df['Origin'] = getOrigin(df['Origin'])
print "Origin completed."

print "Conversion to numeric completed."

# Building classifier
print "Begin cross validation..."

# Choosing features for classifier
features = df.columns[0:9]

# Creating lists for storing results for cross validation.
accuracy = {}
results = {}
matrix = {}
prec = {}
recall = {}

for year in YEARS:
    print "Testing on - ", year
    train = df[df['Year'] != int(year)]  # Test on 1year, train on other 7years
    test = df[df['Year'] == int(year)]
    # test = test[test['Origin'].isin([Origin['OAK'], Origin['SFO']])]
    print len(train), len(test)
    rows = np.random.choice(np.random.permutation(
                            test.index.values), len(test) // 2, replace=False)  # 50% sampling of test data to avoid memory errors faced.
    # print rows
    sampled_test = test.ix[rows]
    sampled_test = test
    # Putting the last column of Training data into a list
    trainTargets = np.array(train['label']).astype(int)

    # Putting the last column of Testing data into a list
    testTargets = np.array(sampled_test['label']).astype(int)
    print "Train length - ", len(train), "Test length -  ", len(sampled_test)
    print train['Year']
    print test['Year']
    print "Model fitting and prediction started..."
    # Building the classifier and fitting the train data
    gnb = GaussianNB()
    y_gnb = gnb.fit(train[features], trainTargets).predict(
        sampled_test[features])
    # Storing results in a new colum in the dataframe.
    sampled_test['pred_label'] = y_gnb
    print "Classification completed."
    # Creating pickle files with the classifier and the results of classifier
    createPickle(gnb, INPUT_FILE_PATH + "classifier_" + year + ".pkl")
    createPickle(y_gnb, INPUT_FILE_PATH + "label_" + year + ".pkl")
    sampled_test.to_csv(
        INPUT_FILE_PATH + "\dfTest" + year + ".csv", index=False)
# Calculating metrics using sklearn metrics functions
    print "\nCalculating metrcs..."
    accuracy[int(year)] = accuracy_score(sampled_test['label'], y_gnb)
    print "Accuracy score - ", accuracy[int(year)]
    prec[int(year)] = precision_score(
        sampled_test['label'], y_gnb, average='micro')
    print "Precision Score - ", prec[int(year)]
    recall[int(year)] = recall_score(
        sampled_test['label'], y_gnb, average='micro')
    print "Recall Score - ", recall[int(year)]
    print "Confusion matrix"
    matrix[int(year)] = metrics.confusion_matrix(
        sampled_test['label'], y_gnb)
    print matrix[int(year)]
    results[int(year)] = precision_recall_fscore_support(
        sampled_test['label'], y_gnb, average='micro')
    print "Precision, recall, F-Score, Support - ", results[int(year)]
    print "Classification report"
    print classification_report(np.array(sampled_test['label']), y_gnb,
                                target_names=target_names)
    print
    train = []
    test = []

print "Accuracy\n", accuracy
print "\nPrecision\n", prec
print "\nRecall\n", recall
print "\nMetrics\n", results
print "\nMatrix\n", matrix

# Finding mean of metrics
print "\nMean Cross validation Precision score", np.mean(pd.Series(prec))
print "\nMean Cross validation Recall score", np.mean(pd.Series(recall))
print "\nMean Cross validation Accuracy score", np.mean(pd.Series(accuracy))

# Pickling results
print "\nPickling stuff..."
createPickle(accuracy, 'accuracy.pkl')
createPickle(prec, 'prec.pkl')
createPickle(results, 'results.pkl')
createPickle(matrix, 'matrix.pkl')
