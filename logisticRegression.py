# import matplotlib.pyplot as plt
import numpy as np
import random
import pickle
import sys
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key

pickle2001 = ['20140423-000818-data-2001',
	'20140423-000818-data-2001-2000000',
	'20140423-000818-data-2001-4000000']
pickle2002 = ['20140423-000818-data-2002',
	'20140423-000818-data-2002-2000000',
	'20140423-000818-data-2002-4000000']

def loadData(fileName):
	if os.path.exists(fileName) == False:
		print 'downloading', fileName, 'from s3'
		conn = S3Connection('KEY', 'private key')
		bucket = conn.get_bucket('i290-aero')
		k = Key(bucket)
		k.key = fileName
		k.get_contents_to_filename(fileName)
		print 'downloaded', fileName, 'from s3'

	print 'now unpickle...'
	x = pickle.load(open(fileName, "rb"))
	x = np.array(x)
	print 'x.shape = ', x.shape, x[:, -1:].shape
	y = x[:, -1:].copy() # last col is y value (delay or not)
	x[:, -1:] = 1.
	return x, y

def gradientDescent(x, y, numIterations, dimension, theta):
	# theta = np.zeros(dimension)[np.newaxis].transpose()
	for i in range(1, numIterations):
		randIdx = random.randint(0, len(x) - 1)
		xTrans = x[randIdx][np.newaxis].transpose()
		print theta.transpose(), xTrans
		u = 1 / (1 + np.exp(np.dot(theta.transpose() * (-1), xTrans)))
		loss = y[randIdx] - u
		gradient = np.dot(loss[0][0], xTrans)
		# update
		theta = theta + gradient / i
	return theta

def graph(formula, x_range):  
	x = np.array(x_range)  
	y = eval(formula)
	plt.plot(x, y)


# def getData(fileName):
# 	f = open(fileName, 'r')
# 	x = np.array([0,0,0])
# 	x0 = []
# 	x1 = []
# 	y = np.array([0])
# 	for line in f:
# 		arr = line.strip().split(' ')
# 		x = np.vstack((x, [float(arr[0]), float(arr[1]), 1.]))
# 		y = np.vstack((y, [float(arr[2])]))
# 		if arr[2] == '0':
# 			x0.append((float(arr[0]), float(arr[1])))
# 		else:
# 			x1.append((float(arr[0]), float(arr[1])))

# 	x = np.delete(x, 0, 0)
# 	y = np.delete(y, 0, 0)
# 	f.close()

# 	return x, x0, x1, y




def main():
	# arg = sys.argv
	# if len(arg) < 2:
	# 	print 'USE: $ python logisticRegression.py [dataset_file]'
	# 	return
	# x, y = loadData(arg[1])

	# x, x0, x1, y = getData('classification.dat')

	if os.path.exists('pickled_theta') == False:
		theta = None
		for elem in pickle2001:
			x, y = loadData(elem)
			if theta == None:
				theta = np.zeros(x.shape[1])[np.newaxis].transpose()
				print 'theta == None...... initialize..........', theta.shape
			theta = gradientDescent(x, y, 100000, x.shape[1], theta)
		print theta

		f = open('pickled_theta', 'wb')
		pickle.dump(theta, f, protocol=pickle.HIGHEST_PROTOCOL)
		f.close()

	theta = pickle.load(open('pickled_theta', 'rb'))

	for elem in pickle2002:
		x, y = loadData(elem)
		dotProduct = np.dot(x, theta)
		print '============= dot product ============='
		print dotProduct
		print '=============y ============='
		print y


	# graph('(-1) * theta[2][0] / theta[1][0] - (theta[0][0] / theta[1][0]) * x', range(-3, 5))
	print 'asdf'



if __name__ == '__main__':
	main()