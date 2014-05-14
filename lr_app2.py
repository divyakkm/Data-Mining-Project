#
# lr_app2.py
# author: eunkwang joo
# description: Loading trimmed datasets stored as csv files, it runs logistic regression using pandas to calculate effective coefficients. Then, it predicts accuracy of the estimates using test dataset.
#

import pandas as pd
import statsmodels.api as sm
# import pylab as pl
import numpy as np
import sys
import random
import os
import pickle

# df = pd.read_csv('trimmed2_2001.csv')#sys.argv[1])


#
# function: reader()
# description: It loads dataset from csv file in dataframe format
# input: f= name of a csv file of dataset
# output: d= dataframe loaded from csv dataset
#

def reader(f):
    d = pd.read_csv(f, header=0)  # , axis=1)
    # d.columns = range(d.shape[1])
    return d


#
# function: shuffle()
# description: It shuffles data
# input: df= dataframe which holds data
#			n= number of shuffles
#			axis= shuffle in which axis
# output: df= shuffled dataframe
#

def shuffle(df, n=1, axis=0):
    df = df.copy()
    for _ in range(n):
        df.apply(np.random.shuffle, axis=axis)
    return df


# search for csv files
for dirpath, dirnames, filenames in os.walk('.'):
    pass

filenames = [f for f in filenames if '.csv' in f]
filenames.sort()
print filenames
# concatenate all csv files in one dataframe
#[1532189 rows x 6 columns]
df = pd.concat([reader(f) for f in filenames], keys=filenames)

print df.head()
print df.columns

# dumm1 = pd.get_dummies(df['carrier'], prefix='carrier')
# dumm2 = pd.get_dummies(df['dest'], prefix='dest')
# dumm3 = pd.get_dummies(df['origin'], prefix='origin')
# dumm4 = pd.get_dummies(df['tailNum'], prefix='tailNum')

cols = ['delay', 'dayOfWeek', 'depTime']

# data = df[cols].join(dumm1.ix[:, 'carrier_3.0':]).join(dumm2.ix[:, 'dest_6.0':]).join(dumm3.ix[:, 'origin_105.0':])
# data = df[cols].join(dumm1).join(dumm2).join(dumm3)
# data['intercept'] = 1.0
# print data.head() #[5 rows x 123 columns] including delay column

# data_delay = data[data['delay'] == 1]
# data_nodelay = data[data['delay'] == 0]

# get delayed data only
data_delay = df[df['delay'] == 1]
rows = random.sample(data_delay.index, len(data_delay))
data_delay_1 = data_delay.ix[rows]
data_delay_2 = data_delay.drop(rows)

# get not delayed data only
data_nodelay = df[df['delay'] == 0]
rows = random.sample(data_nodelay.index, len(data_delay))
data_nodelay = data_nodelay.ix[rows]
# get sample dataset of 50% delayed and 50% not delayed data
data_halfhalf = pd.concat([data_delay, data_nodelay])

rows = random.sample(data_nodelay.index, len(data_delay) / 2)
data_nodelay = data_nodelay.ix[rows]
data_halfhalf_2 = pd.concat([data_delay_2, data_nodelay])

# make dummy variables of carrier, dest, and origin
dumm1 = pd.get_dummies(data_halfhalf['carrier'], prefix='carrier')
dumm2 = pd.get_dummies(data_halfhalf['dest'], prefix='dest')
dumm3 = pd.get_dummies(data_halfhalf['origin'], prefix='origin')
data_halfhalf = data_halfhalf[cols].join(dumm1.ix[:, 'carrier_3.0':]).join(
    dumm2.ix[:, 'dest_6.0':]).join(dumm3.ix[:, 'origin_105.0':])
data_halfhalf['intercept'] = 1.0  # (552264, 117)
# data_halfhalf = shuffle(data_halfhalf)
# data_halfhalf.reindex(np.random.permutation(data_halfhalf.index))
print 'delay = ', len(data_delay), len(data_delay), len(data_halfhalf)


dumm1 = pd.get_dummies(data_halfhalf_2['carrier'], prefix='carrier')
dumm2 = pd.get_dummies(data_halfhalf_2['dest'], prefix='dest')
dumm3 = pd.get_dummies(data_halfhalf_2['origin'], prefix='origin')
data_halfhalf_2 = data_halfhalf_2[cols].join(dumm1.ix[:, 'carrier_3.0':]).join(
    dumm2.ix[:, 'dest_6.0':]).join(dumm3.ix[:, 'origin_105.0':])
data_halfhalf_2['intercept'] = 1.0  # (552264, 117)


# train dataset with logistic regression algorithm
train_cols = data_halfhalf.columns[1:]
logit = sm.Logit(data_halfhalf['delay'], data_halfhalf[train_cols])
result = logit.fit(maxiter=1000)

ff = open('halfhalf_sample_re3', 'w')
ff.write(str(result.summary()))
ff.close()
print result.summary()


# finally, we got theta - coefficient.
a = np.array(result.params)
pickle.dump(a, open('theta_half5', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
theta = pickle.load(open('theta_half5', 'rb'))


# now k-fold test

'''
df_test = pd.read_csv('trimmed2_2008.csv')
dumm_test1 = pd.get_dummies(df_test['carrier'], prefix='carrier')
dumm_test2 = pd.get_dummies(df_test['dest'], prefix='dest')
dumm_test3 = pd.get_dummies(df_test['origin'], prefix='origin')
data_test = df_test[cols].join(dumm_test1.ix[:, 'carrier_3.0':]).join(dumm_test2.ix[:, 'dest_6.0':]).join(dumm_test3.ix[:, 'origin_105.0':])
data_test['intercept'] = 1.0
data_test_cal = data_test.drop('delay', 1)
dot = np.dot(data_test_cal, theta)
'''

rows = random.sample(data_halfhalf.index, len(data_halfhalf) / 10)
df_10 = data_halfhalf.ix[rows]
# df_90 = data_halfhalf.drop(rows)
df_10_cal = df_10.drop('delay', 1)
dotProduct = np.dot(df_10_cal, theta)  # m x 122 * 122 x 1

# get reverse logit
reverseLogit = [np.exp(dot) / (1 + np.exp(dot)) for dot in dotProduct]
prob = [1 if rev >= 0.5 else 0 for rev in reverseLogit]

# predict with test dataset and measure accuracy, precision, and recall
y = df_10['delay']
tp, tn, fp, fn = 0., 0., 0., 0.
for i in range(len(prob)):
    if prob[i] == 1 and y[i] == 1:
        tp += 1
    elif prob[i] == 1 and y[i] == 0:
        fp += 1
    elif prob[i] == 0 and y[i] == 1:
        fn += 1
    elif prob[i] == 0 and y[i] == 0:
        tn += 1
    else:
        raise Exception('wtf!!!', prob[i], y[i])

print 'accuracy = ', (tp + tn) / (tp + fp + fn + tn)
print 'precision = ', tp / (tp + fp)
print 'recall = ', tp / (tp + fn)
print tp, tn, fp, fn

# >>> print 'accuracy = ', (tp + tn) / (tp + fp + fn + tn)
# accuracy =  0.60288632166
# >>> print 'precision = ', tp / (tp + fp)
# precision =  0.607973048849
# >>> print 'recall = ', tp / (tp + fn)
# recall =  0.586353790614
# >>> print tp, tn, fp, fn
# 16242.0 17053.0 10473.0 11458.0


# meaure ROC curve

rlsort = reverseLogit[:]
rlsort.sort()
diff = diff[51900]  # min([j-i for i, j in zip(rlsort[:-1], rlsort[1:])])

p = len([e for e in y if e == 1])
n = len([e for e in y if e == 0])
j = rlsort[0]
r = []
while j <= rlsort[-1]:
    prob = [1 if rev >= j else 0 for rev in reverseLogit]
    p1 = [x for x in prob if x == 1]
    # print p1
    # raw_input()
    tp, fp = 0., 0.
    for i in range(len(prob)):
        if prob[i] == 1 and y[i] == 1:
            tp += 1
        elif prob[i] == 1 and y[i] == 0:
            fp += 1
    r.append((fp / float(n), tp / float(p)))
    # print j, tp, fp, p, n
    j += 0.01

# plot ROC curve
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

r = pickle.load(open('roc.list', 'rb'))
fig = plt.figure()
plt.plot(*zip(*r), marker='o', color='r', ls='')
pp = PdfPages('foo.pdf')
pp.savefig(fig)
pp.close()
