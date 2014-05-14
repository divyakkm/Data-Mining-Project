#
# logisticRegression.py
# author: eunkwang joo
# description: Loading pickled dataset in several fragments, it runs logistic regression to calculate effective coefficients. Then, it predicts accuracy of the estimates using test dataset.
#

import numpy as np
import random
import pickle
import sys
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key


# Trimmed datasets are stroed in pickle format. Due to a memory problem, I
# pickled datasets in many files.

pickle2001 = ['20140428-190051-data-2001',
              '20140428-190051-data-2001-2000000',
              '20140428-190051-data-2001-4000000']
pickle2002 = ['20140428-190051-data-2002',
              '20140428-190051-data-2002-2000000',
              '20140428-190051-data-2002-4000000']
pickle2003 = ['20140428-190051-data-2003',
              '20140428-190051-data-2003-2000000',
              '20140428-190051-data-2003-4000000',
              '20140428-190051-data-2003-6000000']
pickle2004 = ['20140428-190051-data-2004',
              '20140428-190051-data-2004-2000000',
              '20140428-190051-data-2004-4000000',
              '20140428-190051-data-2004-6000000']
pickle2005 = ['20140428-190051-data-2005',
              '20140428-190051-data-2005-2000000',
              '20140428-190051-data-2005-4000000',
              '20140428-190051-data-2005-6000000']
pickle2006 = ['20140428-190051-data-2006',
              '20140428-190051-data-2006-2000000',
              '20140428-190051-data-2006-4000000',
              '20140428-190051-data-2006-6000000']
pickle2007 = ['20140428-190051-data-2007',
              '20140428-190051-data-2007-2000000',
              '20140428-190051-data-2007-4000000',
              '20140428-190051-data-2007-6000000']
pickle2008 = ['20140428-190051-data-2008',
              '20140428-190051-data-2008-2000000',
              '20140428-190051-data-2008-4000000',
              '20140428-190051-data-2008-6000000']

#
# function: loadData()
# description: It loads dataset from pickled files, and separates x variables (features) from y value (delay)
# input: fileName= name of a pickled file
# output: x and y matrices to be used for logistic regression
#


def loadData(fileName):
    if os.path.exists(fileName) == False:
        print 'downloading', fileName, 'from s3'
        conn = S3Connection(
            'AKIAJ3S6FFCVZ7NZPPPA', 'egDauV1C6HY3Q31tjpQg4IiMwSq/Sm4ATASYVl+7')
        bucket = conn.get_bucket('i290-aero')
        k = Key(bucket)
        k.key = fileName
        k.get_contents_to_filename(fileName)
        print 'downloaded', fileName, 'from s3'

    print 'now unpickle...'
    x = pickle.load(open(fileName, "rb"))
    x = np.array(x)
    print 'x.shape = ', x.shape, x[:, -1:].shape
    y = x[:, -1:].copy()  # last col is y value (delay or not)
    x[:, -1:] = 1.
    return x, y


#
# function: gradientDescent()
# description: Using gradient descent algorithm, it runs logistic regression and estimates coefficients.
# input: x= features to be used for logistic regression
#			y= ground truth value of delay
#			numIterations= number of iterations to take for logistic regression
#			dimension= dimension of x matrix
#			theta= coefficient we try to find
# output: theta= coefficient matrix we have found to predict delay
#

def gradientDescent(x, y, numIterations, dimension, theta):
    # theta = np.zeros(dimension)[np.newaxis].transpose()
    for i in range(1, numIterations):
        randIdx = random.randint(0, len(x) - 1)
        xTrans = x[randIdx][np.newaxis].transpose()
        # print theta.transpose(), xTrans
        u = 1 / (1 + np.exp(np.dot(theta.transpose() * (-1), xTrans)))
        loss = y[randIdx] - u
        gradient = np.dot(loss[0][0], xTrans)
        # update
        theta = theta + gradient / i
    return theta


def main():
    # arg = sys.argv
    # if len(arg) < 2:
    # 	print 'USE: $ python logisticRegression.py [dataset_file]'
    # 	return
    # x, y = loadData(arg[1])

    # x, x0, x1, y = getData('classification.dat')

    # train theta for 7 years of dataset
    if os.path.exists('pickled_theta') == False:
        theta = None
        for elem in pickle2001 + pickle2002 + pickle2003 + pickle2004 + pickle2005 + pickle2006 + pickle2008:
            x, y = loadData(elem)
            if theta == None:
                theta = np.zeros(x.shape[1])[np.newaxis].transpose()
                print 'theta == None...... initialize..........', theta.shape
            theta = gradientDescent(x, y, 100000, x.shape[1], theta)
            print 'finished gradientDescent of ', elem
        print 'theta', theta

        # pickle trained theta
        f = open('pickled_theta', 'wb')
        pickle.dump(theta, f, protocol=pickle.HIGHEST_PROTOCOL)
        f.close()

    # load pickled theta
    theta = pickle.load(open('pickled_theta', 'rb'))

    # predict with test dataset
    accu = 0.
    length = 0.
    tp, tn, fp, fn = 0., 0., 0., 0.
    for elem in pickle2007:
        if os.path.exists('dot-' + elem) == False or os.path.exists('y-' + elem) == False:
            x, y = loadData(elem)
            dotProduct = np.dot(x, theta)
            print '============= dot product ============='
            print dotProduct
            print '=============y ============='
            print y
            pickle.dump(
                dotProduct, open('dot-' + elem, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
            pickle.dump(
                y, open('y-' + elem, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)
        else:
            dotProduct = pickle.load(open('dot-' + elem, 'rb'))
            y = pickle.load(open('y-' + elem, 'rb'))

        reverseLogit = [np.exp(dot) / (1 + np.exp(dot)) for dot in dotProduct]
        prob = [1 if rev >= 0.5 else 0 for rev in reverseLogit]

        for i in range(len(prob)):
            if prob[i] == 1 and y[i] == 1:
                accu += 1
                tp += 1
            elif prob[i] == 1 and y[i] == 0:
                fp += 1
            elif prob[i] == 0 and y[i] == 1:
                fn += 1
            elif prob[i] == 0 and y[i] == 0:
                accu += 1
                tn += 1
            else:
                raise Exception('wtf!!!', prob[i], y[i])
        length += len(prob)
    # print accuracy, precision, and recall
    print 'accuracy = ', accu * 100 / length, (tp + tn) / (tp + fp + fn + tn)
    print 'precision = ', tp / (tp + fp)
    print 'recall = ', tp / (tp + fn)

    # graph('(-1) * theta[2][0] / theta[1][0] - (theta[0][0] / theta[1][0]) * x', range(-3, 5))
    print 'asdf'


if __name__ == '__main__':
    main()
